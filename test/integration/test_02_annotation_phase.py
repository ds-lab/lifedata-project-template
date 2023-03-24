import subprocess
from pathlib import Path
from test.conftest import dvc_repro
from test.conftest import get_file_hash

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None


def annotate(query_set, labeled_file, unlabeled_file):
    """
    Method to pseudoannotate a signals and change files `labeled.csv` and `unlabeled.csv`

    query_set: pandas.Dataframe of the `queryset.csv`
    TODO add param to configure how many samples should be annotated
    """

    # Read labeled and unlabeled set
    labeled_set = pd.read_csv(labeled_file)
    unlabeled_set = pd.read_csv(unlabeled_file)
    # Select last sample as to be annotated
    annotation_sample = query_set[-1:]
    # Annotate sample with random label
    annotation_sample["label"] = np.random.choice([0, 1])
    # Add annotated file to labeled set
    labeled_set = pd.concat([labeled_set, annotation_sample])
    # Remove annotated from unlabeled set
    unlabeled_set = unlabeled_set[
        unlabeled_set["sample_id"] != annotation_sample.sample_id.iloc[0]
    ]

    # Save changed files again
    labeled_set.to_csv(labeled_file)
    unlabeled_set.to_csv(unlabeled_file)


# Test that the `02_annotation_phase` user journey works as expected
def test_02_annotation_phase(environment_setup, project_setup, git_setup, dvc_setup):
    """
    With this test it is validated, that templates are in cookiecutter repository and data flow through the given dvc template pipeline
    and scripts.
    """

    from test.artifacts.alexlifedataproject import params

    # Define & Initialize paths
    dvc_lock_path = Path("dvc.lock")
    unlabeled_file = params.absolute_path(params.EXTERNAL_DATA.UNLABELED_FILE)
    labeled_file = params.absolute_path(params.EXTERNAL_DATA.LABELED_FILE)
    model_training_history = params.absolute_path(params.MODEL_TRAINING.HISTORY_FILE)
    queryset_file = params.absolute_path(params.QUERY.QUERY_SET_FILE)
    model_file = params.absolute_path(params.MODEL_TRAINING.MODEL_FILE)

    # Execute dvc stages
    dvc_repro("First repro")
    # Read files after first `dvc repro`
    with open(dvc_lock_path, "r") as f:
        state_first = f.readlines()
    unlabeled_first = pd.read_csv(unlabeled_file)
    labeled_first = pd.read_csv(labeled_file)
    model_history_first = pd.read_csv(model_training_history)
    query_first = pd.read_csv(queryset_file)
    model_hash_first = get_file_hash(model_file)

    # Pseudo annotate some signal
    annotate(query_first, labeled_file, unlabeled_file)

    # Execute dvc stages with new annotations
    dvc_repro("Second repro")
    # Read files after second `dvc repro`
    with open(dvc_lock_path, "r") as f:
        state_second = f.readlines()
    unlabeled_second = pd.read_csv(unlabeled_file)
    labeled_second = pd.read_csv(labeled_file)
    model_history_second = pd.read_csv(model_training_history)
    query_second = pd.read_csv(queryset_file)
    model_hash_second = get_file_hash(model_file)

    # Assert that tracked files changed
    assert state_first != state_second
    assert not labeled_first.equals(labeled_second)
    assert not unlabeled_first.equals(unlabeled_second)
    assert not model_history_first.equals(model_history_second)
    assert not query_first.equals(query_second)
    assert not model_hash_first == model_hash_second

    # Pseudo annotate another signal
    annotate(query_second, labeled_file, unlabeled_file)

    # Execute dvc stages
    dvc_repro("Third repro")

    # Read files after third `dvc repro`
    unlabeled_third = pd.read_csv(unlabeled_file)
    labeled_third = pd.read_csv(labeled_file)
    model_history_third = pd.read_csv(model_training_history)
    query_third = pd.read_csv(queryset_file)
    model_hash_third = get_file_hash(model_file)

    # Assert that tracked files changed
    assert not labeled_second.equals(labeled_third)
    assert not unlabeled_second.equals(unlabeled_third)
    assert not model_history_second.equals(model_history_third)
    assert not query_second.equals(query_third)
    assert not model_hash_third == model_hash_second

    # get logging output for all commits
    commit_texts = (
        subprocess.check_output(["git", "log"], stderr=subprocess.STDOUT)
        .decode("utf-8")
        .split("\n")
    )
    # filter for commit ids
    commits = [k for k in commit_texts if "commit " in k]
    commit_ids = [k.replace("commit ", "") for k in commits]
    # Checkout second commit-ID after first repro
    subprocess.run(f"git checkout {commit_ids[2]}", shell=True, capture_output=True)
    subprocess.run("dvc pull", shell=True, capture_output=True)

    # Read files after `dvc pull`
    unlabeled_fourth = pd.read_csv(unlabeled_file)
    labeled_fourth = pd.read_csv(labeled_file)
    model_history_fourth = pd.read_csv(model_training_history)
    query_fourth = pd.read_csv(queryset_file)
    model_hash_fourth = get_file_hash(model_file)

    # Assert the files are identical to the first `dvc repro`
    assert query_first.equals(query_fourth)
    assert labeled_first.equals(labeled_fourth)
    assert unlabeled_first.equals(unlabeled_fourth)
    assert model_history_first.equals(model_history_fourth)
    assert model_hash_first == model_hash_fourth
