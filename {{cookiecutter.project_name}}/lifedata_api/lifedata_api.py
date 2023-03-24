from pathlib import Path
from typing import List
from typing import Optional

import dvc.repo
import pandas as pd
from lifedata.annotations.annotation import Annotation
from lifedata.annotations.queriedsample import QueriedSample
from lifedata.annotations.sample import Sample
from lifedata.annotations.skip import Skip
from lifedata.lifedata_api import AnnotationQueue
from lifedata.lifedata_api import SampleView
from lifedata.lifedata_api import UiStringDefinition
from loguru import logger

try:
    # NOTE: This import is needed for lifedata framework
    import params
except:  # noqa: E722
    # NOTE: This import is needed for lifedata pipeline with annotations
    from {{cookiecutter.project_name}} import params  # type: ignore

# dvc_repo = dvc.repo.Repo(params.root)
PROJECT_ROOT = Path(__file__).parent

# Project Instance => Lifedata


# API for UI
def get_sample_view() -> SampleView:
    """
    Configure how to display sample data in the annotation ui. You can
    provide your own implementation. Find a working example in
    ``examples/csv-sampleview`` in the lifedata framework repository.
    """

    # When implementing your own you can specify the URL to a development
    # server during development, which enables features like live reloading:
    # return SampleView(
    #     url="http://localhost:3010",
    #     # Optional arguments passed into the component.
    #     args={},
    # )

    # Or use a static build once you're done with development and created a
    # build of the frontend code:
    return SampleView(
        directory=Path(__file__).parent / "sampleview" / "build",
        # Optional arguments passed into the component.
        args={},
    )

    # Alternatively use one of the pre-built sample views by providing the name
    # here.
    # return SampleView(name="image-by-url")


def get_label_metadata() -> dict:
    """
    TODO: Use your own label definition in return value labels
    TODO: Determine if your annotation project needs ["single_label", "multi_label", "segmentation"] and change return parameter label_type to it

    Provide the list of valid labels and the label strategy.

    Supported label_type: "multi_label", "segmentation", "single_label", allows custom extensions
    Supported data_type, like "time-sequence", sequence allows custom extensions but needs implementation in "ui/image_display.js"

    Returns:
        dict: With defined labels, label type and datatype of samples
    """

    # NOTE: It is possible to us a external file for label definition but output must have described format
    labels = params.LABELS

    label_definitions = [
        {
            "unique_code": "labels",
            "name_en": "Labels",
            "criterias": "Criterias",
            "children": [
                {
                    "unique_code": labels[0],
                    "name_en": labels[0],
                    "criterias": "Find a definition for the criteria here",
                    "children": [],
                },
                {
                    "unique_code": labels[1],
                    "name_en": labels[1],
                    "criterias": "Find a definition for the criteria here",
                    "children": [],
                },
            ],
        }
        # NOTE: Following is the definition of a subclass as example:
        # {
        #     "unique_code": "subclass labels",
        #     "name_en": "Subclass labels",
        #     "criterias": "Subclass definition",
        #     "children": [
        #         {
        #             "unique_code": labels[2],
        #             "name_en": labels[2],
        #             "criterias": "Find a definition for the criteria here",
        #             "children": [],
        #         },
        #     ],
        # },
    ]

    return {
        "labels": label_definitions,
        "label_type": "single_label",
        "data_type": "image",
    }


def get_annotation_queues_config() -> List[AnnotationQueue]:
    """
    TODO: Define a list of button functions for the framework.
    To configure a button use {"queue_name":"This is written to the DB", "short_description":"This is displayed in the UI button"}
    """
    return [
        {"queue_name": "request_second_opinion", "short_description": "Second view requested"},
    ]


def get_string_definitions() -> dict:
    """
    TODO: Define your own UI strings
    Method to define strings for UI display
    """
    return UiStringDefinition(
        # Project title that will be displayed in the headerbar
        project_title="{{cookiecutter.project_name}}",
        # Text in front of the sample name
        sample_title="Sample-ID",
        # Labeling question
        label_request_text="Which labels match to the displayed sample?",
        # Label selection instruction
        label_request_text_2="Select matching labels. It is possible to select multiple labels",
        # Text that is displayed while a new sample is loaded
        sample_loading_message="New sample is loading...",
        # Text that is displayed when a sample does not exist locally
        sample_not_found_message="No file was found for the actual sample id",
        # Text that is displayed when a sample cannot be loaded (corrupted file or issues in load method)
        sample_not_loaded_message="Sample could not be loaded",
        # Message displayed when all samples have been annotated
        all_samples_annotated="Congratulation, all samples were annotated",
        # Help text that is displayed for the skip button when hovering
        skip_button_hover_text="Skip an annotation if you are not sure about the label.",
        # Text used in the skip button
        skip_button_text="Skip Annotation",
        # Text used in the button to save an annotation
        annotate_button_text="Store annotation",
        # Text displayed in the search field for label search
        label_search_bar_text="Search for labels",
        # Text displayed over the selected samples
        selected_labels="Selected labels",
        # Text that is displayed when no samples are found in the database
        no_initial_samples="Found no samples to annotate!",
        # Text that is displayed when an annotation was successfully saved
        annotation_stored_text="Annotation saved",
        # Text that is displayed when an annotation could not be saved
        annotation_storage_failed_text="The annotation could not be saved. Please try again.",
        # Text that is displayed when a consulting was successfully saved
        consulting_text="Annotation saved, and second opinion requested",
        # Text that is displayed when a consulting could not be saved
        consulting_failed_text="The annotation could not be saved. Please try again.",
        # Text that is displayed when a skip was successfully saved
        sample_skipped_text="Annotation skipped",
        # Text that is displayed when a skip could not be saved
        sample_skipped_fail_text="The skip could not be saved. Please try again.",
        # Text that is displayed when a logout was executed
        logout_text="You have successfully logged out"
    )


# API samples
def get_all_sample_ids() -> List[str]:
    """
    TODO: Describe and implement your own method to get all sample ids here
    e. g. Search samples with your file extension (e. g. .mat, .img, .png, .jpeg)
    or implement your own method to get all sample ids for LIFEDATA Framework

    Looks for all files with a csv extension in the path with raw data

    Returns:
        List[str]: List of sample ids that can be found in your dataset
    """

    return [path.stem for path in params.absolute_path(params.RAW_DATA.FOLDER).glob("**/*.csv")]


def get_labeled_state() -> List[Annotation]:
    """
    TODO: Define your own method to get labeled samples
    Get labeled state for initial database setup

    Yields:
        List[Annotation]: Iterator of Annotation objects that include annotations
    """
    ids_to_use_for_UI = get_all_sample_ids()

    annotations = []
    if (params.absolute_path(params.EXTERNAL_DATA.LABELED_FILE)).exists():
        labeled_samples = pd.read_csv(params.absolute_path(params.EXTERNAL_DATA.LABELED_FILE))
        for sample_id, annotator_id, label, created in zip(
            labeled_samples.sample_id,
            labeled_samples.annotator_id,
            labeled_samples.label,
            labeled_samples.created,
        ):
            if sample_id in ids_to_use_for_UI:
                annotations.append(
                    Annotation(
                        sample_id=sample_id,
                        annotator_id=str(annotator_id),
                        labels=[label],
                        created=created,
                    )
                )

    logger.info(annotations)

    return annotations


def get_queryset() -> List[QueriedSample]:
    """
    TODO: Check method for your own queryset definition

    Return items that should be used as new queryset for annotation

    Returns:
        List[QueriedSample]: List of QueriedSample used to write it to LIFEDATA database
    """
    if not params.absolute_path(params.QUERY.QUERY_SET_FILE).exists():
        return []

    queryset = pd.read_csv(params.absolute_path(params.QUERY.QUERY_SET_FILE))

    return [
        QueriedSample(sample_id=queryset_sample, query_index=idx)
        for idx, queryset_sample in zip(list(queryset.index), list(queryset.sample_id))
    ]


def read_sample_for_display(sample_id: str) -> pd.DataFrame:
    """
    TODO: Implement your own method to read samples and encode samples for LIFEDATA

    Read samples and encode samples for LIFEDATA

    Args:
        sample_id (str): Filename of the file to be read

    Returns:
        pd.DataFrame: Dataframe with read features from csv files
    """

    return pd.read_csv(
        params.absolute_path(params.RAW_DATA.FOLDER) / (sample_id + ".csv"), index_col=0
    ).to_markdown()


# Lifedata => Project Instance

# API ML pipeline
def get_training_progress() -> Optional[bool]:
    """
    Return some form of training status
    This method should return:
    - True if a training is running
    - None if no training is in progress
    - True if a training should not be executed automatically after queryset is empty

    NOTE: If the query set has been annotated, random unlabeled samples are displayed until the query set is updated.
    """
    logger.info("A training progress check was requested")
    if not Path(".dvc/tmp/rwlock").exists():
        return None

    with open(".dvc/tmp/rwlock", "r") as f:
        data = f.read()
    if data == "{}":
        return None
    else:
        return True


def write_label_state(
    labeled_list: List[Annotation], unlabeled_list: List[Sample], skipped_list: List[Skip]
) -> None:
    """
    TODO: Write your own method to write output from LIFEDATA in a label state

    Writes labelstate for ML pipeline

    Args:
        labeled_list (List[Annotation]): List with annotation objects queried from LIFEDATA's database that represent labeled samples
        unlabeled_list (List[Sample]): List with annotation objects queried from LIFEDATA's database that represent unlabeled samples
        skipped_list (List[Skip]): List with Skipped objects queried from LIFEDATA's database that represent skipped samples
    """
    logger.info("Handle label state was triggered")

    # NOTE: labeled_list always returns a list with Annotations. In the first iteration they are empty and will lead to an error if we don't catch this case here.
    if labeled_list[0].sample_id is None:
        labeled_df = pd.DataFrame(columns=["sample_id", "label", "annotator_id", "created"])
    else:
        # Make single line out of every annotation made
        single_annotations = []
        for annotation in labeled_list:
            for label in annotation.labels:
                single_annotations.append([annotation.sample_id, label, annotation.annotator_id, ""])

        labeled_df = pd.DataFrame(
            single_annotations, columns=["sample_id", "label", "annotator_id", "created"]
        )

    labeled_df.to_csv(params.absolute_path(params.EXTERNAL_DATA.LABELED_FILE), index=False)
    unlabeled_df = pd.DataFrame([sample.id for sample in unlabeled_list], columns=["sample_id"])
    unlabeled_df.to_csv(params.absolute_path(params.EXTERNAL_DATA.UNLABELED_FILE), index=False)


def recreate_queryset():
    """
    TODO: Use your own pipeline definition if you don't want to use dvc as pipeline tool

    Run Machine Learning Pipeline till Stage 'Query Strategy' to create a new `queryset.csv` file.
    """

    logger.info("A recreation of the queryset was triggered")
    dvc_repo = dvc.repo.Repo(PROJECT_ROOT)
    dvc_repo.reproduce(all_pipelines=True)
