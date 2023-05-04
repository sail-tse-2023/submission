
# Supplemental Materials

This repository contains the replication package for the paper "An Empirical Study of Refactoring Rhythms and Tactics in the Software Development Process".


## Introduction



We have organized the replication package into sevem folders:

1. data: this folder contains all the data required to run the experiments
2. appendix: this folder includes extra information about the paper, such as validation results and the refactoring types studied in this project
3. helpers: this folder contains the helper functions used by other parts of the package
4. code_smells_analysis: this folder includes scripts to measure the relationship between code smells and different refactoring rhythms and tactics
5. fetch_profiles: this folder includes the code to extract different developer and author profiles
6. rhythm_tactics_profiles: this folder includes the relationship of each refactoring rhythm and tactic with corresponding author and project profiles.
7. rhythms_tactics_identification: this folder includes the corresponding code for refactoring rhythm and tactics, including clustering.


Our code is based on the following packages and versions:
- matplotlib: 3.6.0
- scipy: 1.9.1
- pandas: 1.5.0
- sklearn: 0.0
- seaborn: 0.12.0
- rpy2: 3.5.5
- numpy: 1.23.3
- kmodes: 0.12.2
- tslearn: 0.5.2
- h5py: 3.7.0
- numba: 0.56.3

The following code can be used to install all packages in the environment.
```bash
  pip install -r requirements.txt
```

As r2py allows Python programs to interface with R, make sure to install R in your system:

https://www.r-project.org/


We recommend using Python version 3.8.1, R version 4.3.1, and every Python requirement should be met.

    
## Usage/Examples

We have the following codes and fucntions available:
- **Pre-Processing**:
    - fetch_profiles/author_profiles.py
        - author_profiles()
    - fetch_profiles/project_profiles.py
        - project_profiles()
- **Research Question 1**:
    - rhythms_tactics_identification/rhythms.py
        - kruskal_wallis_clustering()
    - rhythm_tactics_profiles/rhythm_profiles.py
        - developer_profiles_clustering()
        - project_profiles_clustering()
- **Research Question 2:**
    - rhythms_tactics_identification/tactics.py
        - dtw_clustering()
    - rhythm_tactics_profiles/tactic_profiles.py
        - developer_profiles_clustering()
        - project_profiles_clustering()
- **Research Question 3:**
    - code_smells_analysis.rhythm_smells.py
        - fetch_overall()
    - code_smells_analysis.tactic_smells.py
        - fetch_overall()

Below is an example of ho to run the functions in the root of the project
```javascript
import rhythms_tactics_identification.rhythms
rhythms_tactics_identification.rhythms.kruskal_wallis_clustering()
```


## Appendix

The results of the manual validation are stored in the "appendix/validation" folder, which includes the results of the first validator, the second validator, and the resolved conflicts. Additionally, the refactoring types studied in this work are stored in the "appendix/refactoring_types_rminer.csv" file.



