import json
import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

def developer_profiles_clustering():
    with open("data/outputs/author_profiles.json") as project:
        clusters = json.load(project)
    with open("data/outputs/rhythms.json") as project:
        groups = json.load(project)

    all_rhythms = list(groups.keys())
    profiles = {}
    for rhythm in groups.keys():
        for developer_profile in clusters.keys():
            profiles[rhythm + "-" + developer_profile] = []

    for developer_profile, info in clusters.items():
        for developer in info['developers']:
            chunk = int(developer.split("_")[-1])
            repo = developer.split("_")[-2]
            active_rhythm = get_rhythm(repo + "_" + str(chunk))
            not_active_rhythms = [item for item in all_rhythms if item not in [active_rhythm]]

            profiles[active_rhythm + '-' + developer_profile].append(1)
            for not_active_rhythm in not_active_rhythms:
                profiles[not_active_rhythm + '-' + developer_profile].append(0)

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
        with open("data/outputs/rhythms.json") as project:
            groups = json.load(project)

        all_rhythms = list(groups.keys())
        profiles = {}
        for rhythm in groups.keys():
            for project_profile in clusters.keys():
                profiles[rhythm+"-"+project_profile] = []

        for project_profile, info in clusters.items():
            for project in info['projects']:
                chunk = int(project.split("_")[-1])
                repo = project.split("_")[-2]
                active_rhythm = get_rhythm(repo + "_" + str(chunk))
                not_active_rhythms = [item for item in all_rhythms if item not in [active_rhythm]]

                profiles[active_rhythm+'-'+project_profile].append(1)
                for not_active_rhythm in not_active_rhythms:
                    profiles[not_active_rhythm +'-'+project_profile].append(0)

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


def get_rhythm(project_name):
    with open("data/outputs/rhythms.json") as project:
        groups = json.load(project)
    for rhythm, projects in groups.items():
        for project in projects:
            if project == project_name:
                return rhythm