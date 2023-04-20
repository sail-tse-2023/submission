from helpers.helper import FileManager
import json
import pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri


def fetch_overall():
    print('fetch overall')
    with open("data/outputs/rhythms.json") as project:
        groups = json.load(project)
    border_lines = FileManager.read_json("data/border_lines.json")

    with open("data/designite.json") as project:
        designite = json.load(project)

    headers = ['sum', 'rhythm']
    overall = [headers]

    smells_headers = list(designite['accumulo']['0-1'].keys())
    smells_headers.append('rhythm')
    seperate = [smells_headers]

    for rhythm, repo_time_windows in groups.items():
        for repo_time_window in repo_time_windows:

            try:
                repo = repo_time_window.split('_')[0]
                current_time_window = str(int(repo_time_window.split('_')[1]) - 1) + "-" + str(
                    int(repo_time_window.split('_')[1]))
                previous_time_window = str(int(repo_time_window.split('_')[1]) - 2) + "-" + str(
                    int(repo_time_window.split('_')[1]) - 1)

                # Calculate code churns in before and current stage for normalization
                code_metrics_before = border_lines[repo][previous_time_window]
                code_churn_before = (code_metrics_before['insertions'] + code_metrics_before['deletions'])
                before_loc = code_metrics_before['insertions'] - code_metrics_before['deletions']

                code_metrics_current = border_lines[repo][current_time_window]
                code_churn_current = (code_metrics_current['insertions'] + code_metrics_current['deletions'])
                current_loc = code_metrics_current['insertions'] - code_metrics_current['deletions']

                stage_churn = code_churn_current - code_churn_before

                # Normalize smells based on the calculated code churn
                smells_before = {k: v / before_loc for k, v in
                                 designite[repo][previous_time_window].items()}
                smells_current = {k: v / current_loc for k, v in
                                  designite[repo][current_time_window].items()}
                smell_difference = {
                    key: smells_current[key] - smells_before.get(key, 0) / (stage_churn / current_loc) for key in
                    smells_current}

                overall.append([sum(smell_difference.values()), rhythm])
                list_smells = list(smell_difference.values())
                list_smells.append(rhythm)
                seperate.append(list_smells)

            except:
                continue

    # Prepare for scottKnottESD overall
    data_dict = {}
    for key, value in overall[1:]:
        if value not in data_dict:
            data_dict[value] = []
        data_dict[value].append(round(key, 5))

    data_dict = pd.DataFrame.from_dict(data_dict, orient='index').transpose()
    means = data_dict.mean().to_dict()
    print(means)
    pandas2ri.activate()
    sk = importr('ScottKnottESD')
    r_sk = sk.sk_esd(data_dict)

    r_sk = str(r_sk)
    print(r_sk)
    tactics = r_sk.split()[1:4]
    groups = r_sk.split()[4:7]
    r_sk_result = {tactics[i]: groups[i] for i in range(len(tactics))}
    print(r_sk_result)
    exit()
