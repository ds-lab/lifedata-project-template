from pathlib import Path

root = Path(__file__).parent.absolute()

RANDOM_STATE = 123

LABELS = [1, 2, "label_3"]


def absolute_path(relative_path: str) -> Path:
    return root / relative_path


class RAW_DATA:
    FOLDER = "data/raw"


class DATA_SET_REPORT:
    FOLDER = "reports/data_set_report/"
    ANALYSIS_REPORT_FILE = "reports/data_set_report/report.csv"


class EXTERNAL_DATA:
    UNLABELED_FILE = "data/label_state/unlabeled.csv"
    LABELED_FILE = "data/label_state/labeled.csv"


class TRAIN_TEST:
    FOLDER = "data/data_dvc/train_test_split/"
    TEST_SPLIT_FILE = "data/data_dvc/train_test_split/test.csv"
    TRAIN_SPLIT_FILE = "data/data_dvc/train_test_split/train.csv"
    # possible options for TRAIN_TEST_STRATEGY: 'proportional', 'static', 'proportional_labeled'
    TRAIN_TEST_STRATEGY = "static"
    # percentage (float) of complete data for proportional train-test-split
    # count of samples (int) per class for static train-test-split
    # Debug Test Size: 1 or 0.1
    # Default Test Size: 30 or 0.2
    TEST_SIZE = 1


class PREPROCESS:
    FOLDER = "data/data_dvc/preprocess/"
    MULTIPLICATION_FACTOR = 2
    ADDITION_FACTOR = 1


class MODEL_TRAINING:
    FOLDER = "data/data_dvc/model_training/"
    MODEL_FILE = "data/data_dvc/model_training/model.checkpoint"
    HISTORY_FILE = "data/data_dvc/model_training/history.csv"
    BATCH_SIZE = 3
    EPOCHS = 3
    LEARNING_RATE = 0.001
    # ExampleModelTF, ExampleModelTorch
    MODEL_ARCHITECTURE = "ExampleModelTorch"


class QUERY:
    FOLDER = "data/data_dvc/query/"
    QUERY_SET_FILE = "data/data_dvc/query/queryset.csv"
    QUERY_SET_SIZE = 5
    # available options: random, uncertainty
    # How to use multiple query strategies:
    # LIST_QS_STRATEGIES = ["uncertainty", "random"]
    # LIST_QS_WEIGHTS = [1, 4]
    # This would result in a mix of uncertainty and random selected samples,
    # with a ratio of 1 uncertainty for every 4 random
    LIST_QS_STRATEGIES = ["uncertainty", "random"]
    LIST_QS_WEIGHTS = [1,1]


class SEMI_SUPERVISED:
    FOLDER = "data/data_dvc/pseudo_labels/"
    PSEUDOLABEL_SET_FILE = "data/data_dvc/pseudo_labels/pseudo_labels.csv"
    SEMI_SUPERVISED_METHOD = "random"
    SEMI_SUPERVISED_SET_SIZE = 10


class EVALUATION:
    FOLDER = "data/data_dvc/evaluation/"
    METRICS_FILE = "data/data_dvc/evaluation/evaluation.yaml"


class EXPLAIN:
    FOLDER = "data/data_dvc/explain/"
    METRICS_FILE = "data/data_dvc/explain/explain.yaml"
    EXPLAINABILITY_METHOD = "None"
    SAMPLES_TO_EXPLAIN = ["test"]
