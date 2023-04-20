import json
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import pandas as pd


def developer_profiles_clustering():
    with open("data/outputs/author_profiles.json") as project:
        clusters = json.load(project)
    with open("data/outputs/tactics.json") as project:
        groups = json.load(project)

    all_tactics = list(groups.keys())
    profiles = {}
    for tactic in groups.keys():
        for developer_profile in clusters.keys():
            profiles[tactic + "-" + developer_profile] = []

    print(profiles)
    for developer_profile, info in clusters.items():
        for developer in info['developers']:
            chunk = int(developer.split("_")[-1])
            repo = developer.split("_")[-2]
            active_tactic = get_tactic(repo, str(chunk))
            not_active_tactics = [item for item in all_tactics if item not in [active_tactic]]
            if active_tactic:
                profiles[active_tactic + '-' + developer_profile].append(1)
                for not_active_tactic in not_active_tactics:
                    profiles[not_active_tactic + '-' + developer_profile].append(0)

    data_dict = pd.DataFrame.from_dict(profiles, orient='index').transpose()
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


def project_profiles_clustering():
    with open("data/outputs/project_profiles.json") as project:
        clusters = json.load(project)
    with open("data/outputs/tactics.json") as project:
        groups = json.load(project)

    all_tactics = list(groups.keys())
    profiles = {}
    for tactic in groups.keys():
        for project_profile in clusters.keys():
            profiles[tactic + "-" + project_profile] = []

    for project_profile, info in clusters.items():
        print(project_profile)
        for project in info['projects']:
            chunk = int(project.split("_")[-1])
            repo = project.split("_")[-2]
            active_tactic = get_tactic(repo, str(chunk))
            not_active_tactics = [item for item in all_tactics if item not in [active_tactic]]

            if active_tactic:
                profiles[active_tactic + '-' + project_profile].append(1)
                for not_active_tactic in not_active_tactics:
                    profiles[not_active_tactic + '-' + project_profile].append(0)

    data_dict = pd.DataFrame.from_dict(profiles, orient='index').transpose()
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


def get_tactic(project_name, chunk):
    with open("data/outputs/tactics.json") as project:
        groups = json.load(project)
    for cluster, info in groups.items():
        for project, borders in info.items():
            for chunked, key in borders.items():
                if project == project_name and int(chunk) == int(key[1]):
                    return cluster
