import os
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(os.path.abspath(__file__)).parents[1] / "artifacts"))


def test_get_label_metadata(environment_setup, project_setup):
    from lifedata.lifedata_api.load_lifedata_api import load_project_api
    from lifedata.lifedata_api.label_config import LabelConfig

    project = load_project_api()

    label_definitions = [
        {
            "unique_code": "labels",
            "name_en": "Labels",
            "criterias": "Criterias",
            "children": [
                {
                    "unique_code": 1,
                    "name_en": 1,
                    "criterias": "Find a definition for the criteria here",
                    "children": [],
                },
                {
                    "unique_code": 2,
                    "name_en": 2,
                    "criterias": "Find a definition for the criteria here",
                    "children": [],
                },
            ],
        }
    ]

    expected_labeldata = LabelConfig(
        labels=label_definitions, label_type="single_label", data_type="image"
    )

    labeldata_out = project.get_label_metadata()

    assert labeldata_out.labels == expected_labeldata.labels
    assert labeldata_out.label_type == expected_labeldata.label_type
    assert labeldata_out.data_type == expected_labeldata.data_type


def test_get_all_sample_ids(environment_setup, project_setup):
    from lifedata.lifedata_api.load_lifedata_api import load_project_api

    project = load_project_api()

    expected_samples = [
        "Sample_1",
        "Sample_2",
        "Sample_3",
        "Sample_4",
        "Sample_5",
        "Sample_6",
        "Sample_7",
        "Sample_8",
        "Sample_9",
        "Sample_10",
        "Sample_11",
        "Sample_12",
        "Sample_13",
    ]

    samples_found = project.get_all_sample_ids()

    assert samples_found.sort() == expected_samples.sort()


def test_read_sample_id(environment_setup, project_setup):
    from lifedata.lifedata_api.load_lifedata_api import load_project_api

    project = load_project_api()

    samples_found = project.get_all_sample_ids()
    samples_found.sort()
    sample_id = samples_found[0]

    expected_output = pd.DataFrame(
        {"feature1": [0.1], "feature2": [0.3], "feature3": [0.6], "feature4": [0.1]}
    ).to_markdown(index=False)

    read_output = project.read_sample_for_display(sample_id)

    assert expected_output == read_output


def test_active_learning_tasks(environment_setup, project_setup, git_setup, dvc_setup):
    # NOTE: Tests if active learning pipeline functions run without error
    # NOTE: Import packages after alexlifedata environment was created and activated
    from lifedata.lifedata_api.load_lifedata_api import load_project_api

    project = load_project_api()
    # test_execution of ml pipeline
    try:
        project.recreate_queryset()
        assert 1
    except BrokenPipeError:
        pytest.fail("Machine learning pipeline could not be executed without errors")


def test_get_queryset(environment_setup, project_setup, git_setup, dvc_setup):
    from lifedata.lifedata_api.load_lifedata_api import load_project_api

    project = load_project_api()

    project.recreate_queryset()

    queryset_output = project.get_queryset()

    # NOTE: The overannotated samples in queryset are random selected
    minimal_queryset_for_uncertainty = 3
    assert len(queryset_output) >= minimal_queryset_for_uncertainty


def test_get_notebooks():
    pass


def test_write_label_state(environment_setup, project_setup, git_setup, dvc_setup):
    # NOTE: Import packages after alexlifedata environment was created and activated
    from lifedata.annotations.annotation import Annotation
    from lifedata.annotations.sample import Sample
    from lifedata.annotations.skip import Skip

    from lifedata.lifedata_api.load_lifedata_api import load_project_api

    project = load_project_api()

    project.recreate_queryset()

    annotated = [
        Annotation(
            sample_id="Sample_1",
            annotator_id="Testannotator_1",
            labels=["Label1"],
            created="",
        ),
        Annotation(
            sample_id="Sample_2",
            annotator_id="Testannotator_1",
            labels=["Label2"],
            created="",
        ),
        Annotation(
            sample_id="Sample_3",
            annotator_id="Testannotator_2",
            labels=["Label1", "Label2"],
            created="",
        ),
    ]

    skipped = [Skip]

    sample_ids_labeled = [
        [annotation.sample_id, annotation.labels, annotation.annotator_id, ""]
        for annotation in annotated
    ]
    expected_wrote_labeled = pd.DataFrame(
        sample_ids_labeled, columns=["sample_id", "label", "annotator_id", "created"]
    )
    expected_wrote_labeled = expected_wrote_labeled.explode("label", ignore_index=True)

    unannotated = [Sample("Sample_20"), Sample("Sample_21")]

    sample_ids_unlabeled = [sample.id for sample in unannotated]
    expected_wrote_unlabeled = pd.DataFrame(sample_ids_unlabeled, columns=["sample_id"])

    project.write_label_state(annotated, unannotated, skipped)

    assert Path("data/label_state/labeled.csv").exists()
    assert Path("data/label_state/unlabeled.csv").exists()

    wrote_labeled = pd.read_csv(Path("data/label_state/labeled.csv")).fillna("")
    wrote_unlabeled = pd.read_csv(Path("data/label_state/unlabeled.csv"))

    pd.testing.assert_frame_equal(wrote_unlabeled, expected_wrote_unlabeled)
    pd.testing.assert_frame_equal(wrote_labeled, expected_wrote_labeled)


def test_write_empty_label_state(
    environment_setup, project_setup, git_setup, dvc_setup
):
    # NOTE: Import packages after alexlifedata environment was created and activated
    from lifedata.annotations.annotation import Annotation
    from lifedata.annotations.sample import Sample
    from lifedata.annotations.skip import Skip

    from lifedata.lifedata_api.load_lifedata_api import load_project_api

    project = load_project_api()

    project.recreate_queryset()

    annotated = [
        Annotation(
            sample_id=None,
            annotator_id=None,
            labels=[None],
            created="",
        )
    ]

    skipped = [Skip]

    expected_wrote_labeled = pd.DataFrame(
        columns=["sample_id", "label", "annotator_id", "created"]
    )

    unannotated = [Sample("Sample_20"), Sample("Sample_21")]

    sample_ids_unlabeled = [sample.id for sample in unannotated]
    expected_wrote_unlabeled = pd.DataFrame(sample_ids_unlabeled, columns=["sample_id"])

    project.write_label_state(annotated, unannotated, skipped)

    assert Path("data/label_state/labeled.csv").exists()
    assert Path("data/label_state/unlabeled.csv").exists()

    wrote_labeled = pd.read_csv(Path("data/label_state/labeled.csv"))
    wrote_unlabeled = pd.read_csv(Path("data/label_state/unlabeled.csv"))

    pd.testing.assert_frame_equal(wrote_unlabeled, expected_wrote_unlabeled)
    pd.testing.assert_frame_equal(wrote_labeled, expected_wrote_labeled)
