import json
from kmodes.kmodes import KModes
from pandas import DataFrame


def project_profiles():
    """
    This function generates project profiles based on authors mods identified by author metrics
    """
    with open("data/project_mods.json") as json_file:
        details = json.load(json_file)

    # remove the ones with {}
    empties = []
    for repo, info in details.items():
        if not info:
            empties.append(repo)
    for empty in empties:
        details.pop(empty, None)

    redundants = ['code', 'comment', 'issues']
    for project in details.keys():
        for redundant in redundants:
            details[project].pop(redundant, None)

    headers = list(list(details.values())[0].keys())

    data = []
    for repo, item in details.items():
        if item:
            if len(list(item.values())) == 7:
                data.append(list(item.values()))
            else:
                print("error")
                print(repo, item)
    df = DataFrame(data)

    random_state = 0
    k = 4

    km = KModes(n_clusters=k, init='Huang', random_state=random_state, n_init=5, verbose=1)
    km.fit_predict(df)

    for centroid in km.cluster_centroids_:
        for i in range(0, len(centroid)):
            print(centroid[i] + " " + headers[i], end=" and ")
        print("")

    # Save to file
    results = {}
    for i in range(0, len(details.keys())):
        project_name = list(details.keys())[i]
        label = km.labels_[i]
        if label not in results:
            results[int(label)] = {
                'details': {},
                'projects': []
            }
        results[label]['projects'].append(project_name)

    for cluster_id in range(0, len(km.cluster_centroids_)):
        print(cluster_id)
        for i in range(0, len(headers)):
            results[int(cluster_id)]['details'][headers[i]] = km.cluster_centroids_[cluster_id][i]

    out_file = open("data/outputs/project_profiles.json", "w")
    json.dump(results, out_file, indent=4)
    out_file.close()
