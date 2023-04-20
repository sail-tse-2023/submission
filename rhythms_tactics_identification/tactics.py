from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series_dataset
import json
import matplotlib.pyplot as plt
import matplotlib


def dtw_clustering():
    """
    This method calculates the refactoring tactics using Dynamic Time Warping(DTW algorithm.
    """
    new_data = []
    with open("data/stagely.json") as json_file:
        densities = json.load(json_file)

    lenghts = []
    keys = []
    for repo, timeline in densities.items():
        for zone, series in timeline.items():
            if len(series) > 2:
                keys.append(str(repo) + "$" + str(zone))
                lenghts.append(len(series))
                new_data.append(series)
    random_s = 24
    data = to_time_series_dataset(new_data)

    km_dba = TimeSeriesKMeans(n_clusters=4, metric="dtw", random_state=random_s).fit(data)
    tmp = 0
    matplotlib.use('TkAgg')
    for i in km_dba.cluster_centers_:
        plt.ylim(0, 1)
        plt.plot(i)
        plt.title("Cluster Number: " + str(tmp), fontsize=16)
        plt.ylabel('Refactoring Density', fontsize=16)
        plt.xlabel('Life-Cycle (Weeks)', fontsize=16)
        plt.show()
        tmp = tmp + 1

    info = {}
    info['keys'] = keys
    labels = list(km_dba.labels_)
    labels = [str(i) for i in labels]
    info['values'] = labels

    # Refine the results into a readable json file on project stages
    groups = info
    first_refine = {
        'projects': {},
    }
    for repo_info in groups['keys']:
        repo_name = list(repo_info.split('$'))[0]
        chunk = list(repo_info.split('$'))[1]
        if repo_name not in first_refine['projects']:
            first_refine['projects'][repo_name] = {
                'borders': [],
                'keys': []
            }
        first_refine['projects'][repo_name]['borders'].append(chunk)

    for project, info in first_refine['projects'].items():
        tmp = []
        for i in range(0, len(info['borders'])):
            tmp.append([i, i + 1])
        first_refine['projects'][project]['keys'] = tmp

    second_refine = {}
    for project, info in first_refine['projects'].items():
        second_refine[project] = {}
        for i in range(0, len(info['borders'])):
            second_refine[project][info['borders'][i]] = info['keys'][i]

    results = {}
    for i in range(0, len(groups['keys'])):
        repo_name = list(groups['keys'])[i].split('$')[0]
        chunk = list(groups['keys'])[i].split('$')[1]
        cluster_id = list(groups['values'])[i]
        if cluster_id not in results:
            results[cluster_id] = {}
        if repo_name not in results[cluster_id]:
            results[cluster_id][repo_name] = {}
        results[cluster_id][repo_name][chunk] = second_refine[repo_name][chunk]

    out_file = open("data/outputs/tactics.json", "w")
    json.dump(results, out_file, indent=4)
    out_file.close()


