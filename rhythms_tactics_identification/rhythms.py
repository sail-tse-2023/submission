import json
from scipy.stats import kruskal

def kruskal_wallis_clustering():
    """
    This function first calculates project stages with the all-day refactoring rhythms (same distribution),
    then it calculates the project stages with work-day refactoring rhythms (same on workdays after excluding the
    project stages with all-day rhythm).
    """
    results = {
        'all-day': [],
        'work-day': [],
        'other': []
    }
    with open("data/daily_densities.json") as project:
        history = json.load(project)

    # Identify projects with all-day refactoring rhythm
    for repo, time_windows in history.items():
        for time_window, daily_ratios in time_windows.items():
            daily_ratio_list = list(daily_ratios.values())
            try:
                stat, p = kruskal(*daily_ratio_list)
            except ValueError as e:
                continue

            alpha = 0.05
            if p > alpha:
                results['all-day'].append(repo + '_' + time_window.split('-')[1])
                print('Statistics=%.3f, p=%.3f' % (stat, p))
                print('Same distributions (fail to reject H0)')

    # Identify projects with work-day only refactoring rhythm
    for repo, time_windows in history.items():
        for time_window, daily_ratios in time_windows.items():
            if repo + '_' + time_window.split('-')[1] not in results['all-day']:
                daily_ratios.pop('Saturday', None)
                daily_ratios.pop('Sunday', None)
                daily_ratio_list = list(daily_ratios.values())
                try:
                    stat, p = kruskal(*daily_ratio_list)
                except ValueError as e:
                    continue
                alpha = 0.05
                if p > alpha:
                    results['work-day'].append(repo + '_' + time_window.split('-')[1])
                    print('Statistics=%.3f, p=%.3f' % (stat, p))
                    print('Same distributions (fail to reject H0)')
                else:
                    results['other'].append(repo + '_' + time_window.split('-')[1])

    out_file = open("data/outputs/rhythms.json", "w")
    json.dump(results, out_file, indent=4)
    out_file.close()
