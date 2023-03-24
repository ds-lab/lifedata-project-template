from test.conftest import dvc_repro


def test_01_project_setup(environment_setup, project_setup, git_setup, dvc_setup):
    """
    # NOTE: The user has so setup git manually with ´git init´. Cookiecutter template contains an instantiated DVC project
    """
    # Execute dvc stages and push results to git & dvc remotes
    dvc_repro("First repro")
