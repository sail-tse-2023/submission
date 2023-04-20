from helpers.helper import FileManager
import json
import csv
import pandas as pd
import helpers.statics
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri


def fetch_overall():
    with open("data/outputs/tactics.json") as project:
        groups = json.load(project)

    border_lines = FileManager.read_json("data/border_lines.json")

    with open("data/designite.json") as project:
        designite = json.load(project)

    headers = ['sum', 'tactic']
    overall = [headers]

    smells_headers = list(designite['accumulo']['0-1'].keys())
    smells_headers.append('tactic')
    seperate = [smells_headers]

    for tactic, repos in groups.items():
        for repo, time_windows in repos.items():
            for time_window in time_windows:

                try:
                    current_time_window = time_window
                    previous_time_window = str(int(time_window.split('-')[0]) - 1) + "-" + str(
                        int(time_window.split('-')[1]) - 1)

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
                        key: smells_current[key] - smells_before.get(key, 0) / (stage_churn / current_loc) for key
                        in
                        smells_current}

                    overall.append([sum(smell_difference.values()), tactic])
                    list_smells = list(smell_difference.values())
                    list_smells.append(tactic)
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

    pandas2ri.activate()
    sk = importr('ScottKnottESD')
    r_sk = sk.sk_esd(data_dict)

    r_sk = str(r_sk)
    print(means)
    print(r_sk)
    tactics = r_sk.split()[1:5]
    groups = r_sk.split()[5:9]
    r_sk_result = {tactics[i]: groups[i] for i in range(len(tactics))}
    print(r_sk_result)

    # Scott-Knott-ESD on the seperate

    seperate_to_csv = []

    seperate_df = pd.DataFrame(seperate[1:], columns=seperate[0])
    for code_smell in helpers.statics.code_smell_types:
        tactics = seperate_df['tactic']
        changes = list(seperate_df[code_smell])
        code_smell_dict = {}
        for i in range(len(tactics)):
            if tactics[i] not in code_smell_dict:
                code_smell_dict[tactics[i]] = []
            code_smell_dict[tactics[i]].append(changes[i])

        tactic_names = list(set(tactics))
        try:
            data_dict = pd.DataFrame.from_dict(code_smell_dict, orient='index').transpose()
            # print(data_dict)
            sk = importr('ScottKnottESD')
            r_sk = sk.sk_esd(data_dict)

            r_sk = str(r_sk)
            tactics = r_sk.split()[1:5]
            groups = r_sk.split()[5:9]
            r_sk_result = {tactics[i]: groups[i] for i in range(len(tactics))}
        except:
            # For the case that all means are 0
            tactics = tactic_names
            groups = ['1', '1', '1', '1']
            r_sk_result = {tactics[i]: groups[i] for i in range(len(tactics))}

        row = [code_smell]
        for key, value in r_sk_result.items():
            column = key + "(" + value + ")"
            row.append(column)

        seperate_to_csv.append(row)

    with open('data/outputs/seperate.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(seperate_to_csv)
