import hashlib
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_NAME = "alexlifedataproject"


def get_conda_windows_linux_bin_path_name():
    """
    Returns "Scripts" if on windows and "bin" if on Linux
    """
    if sys.platform == "win32":
        return "Scripts"
    elif sys.platform == "linux":
        return "bin"
    elif sys.platform == "darwin":
        return "bin"
    else:
        raise EnvironmentError("Operating System not known")


def conda_env_binaries_path():
    """
    Checks if a conda environment with `alexlifedataproject` in the path to it exists
    If so, returns path to that environment. Otherwise, returns None
    """
    output = subprocess.run("conda env list", shell=True, capture_output=True)

    std_out_str = str(output.stdout)

    # \S+alexlifedataproject\\n finds the project path such as `/home/user/miniconda3/envs/alexlifedataproject`
    # The `(\\n|.\.env)` allows both `/home/user/miniconda3/envs/alexlifedataproject` and `/mnt/c/code/lifedata-cookiecutter/.env`
    regex_result = re.search(r"\S+alexlifedataproject(\\n|.\.env)", std_out_str)

    if regex_result is None:
        return None
    else:
        # The last 2 chars can be `\n`, replace with empty
        env_root_dir = Path(regex_result.group().replace("\\n", ""))
        conda_env_bin_path = env_root_dir / get_conda_windows_linux_bin_path_name()
        assert conda_env_bin_path.exists()
        return conda_env_bin_path


def get_project_root() -> Path:
    """Returns absolute path to the root of lifedata-cookiecutter project"""
    project_path = Path(__file__).parents[1]
    return project_path.absolute()


def get_test_artifacts_path() -> Path:
    return get_project_root() / "test" / "artifacts"


@pytest.fixture(scope="session")
def environment_setup():
    """
    - checks if the conda environment with the name `alexlifedataproject` exists. If not, creates it
    - Activates the conda environment by prepending the binaries to the system path
    """

    logging.info("Environment setup called")

    conda_env_path = conda_env_binaries_path()

    logging.debug(
        "Activating conda environment by adding the site-packages directory to the system path"
    )
    os.environ["PATH"] = str(conda_env_path) + ":" + os.environ["PATH"]
    sys.path.insert(0, str(conda_env_path.parent / "lib/python3.8/site-packages"))

    logging.info(os.environ["PATH"])
    logging.info(sys.path)

    yield

    logging.info("Starting Environment-Setup-Teardown")

    logging.debug("Deactivating conda environment")
    # Replace the path to the environment and its separator with an empty string
    os.environ["PATH"] = os.environ["PATH"].replace(str(conda_env_path) + ":", "")
    # Remove the path to the environment
    sys.path.remove(str(conda_env_path.parent / "lib/python3.8/site-packages"))

    os.chdir(get_project_root())


@pytest.fixture
def project_setup():
    """
    - Initializes a project based on the cookiecutter
    - Changes the current working directory into the alexlifedataproject directory
    """
    TEST_ARTIFACTS_PATH = get_test_artifacts_path()
    # Create directory for artifacts of this test
    TEST_ARTIFACTS_PATH.mkdir(exist_ok=True)

    mylifedata_path = TEST_ARTIFACTS_PATH / PROJECT_NAME

    # Remove old instantiation of the cookiecutter, in case it exists from previous runs
    shutil.rmtree(mylifedata_path, ignore_errors=True)

    # Initialize alexlifedataproject with cookiecutter
    logging.info(f"Creating {PROJECT_NAME} from cookiecutter in {TEST_ARTIFACTS_PATH}")
    shell_run(
        f"cookiecutter --no-input -f {get_project_root()} -o {TEST_ARTIFACTS_PATH} project_name={PROJECT_NAME}"
    )

    # Navigate into the new project
    os.chdir(mylifedata_path)

    # For local debugging, ensure that the alexlifedataproject package is installed
    logging.debug(f"Pip-Installing {PROJECT_NAME}")
    shell_run("pip install -e .")

    yield {"mylifedata_path": mylifedata_path.absolute()}

    logging.info("Starting Project-Teardown")

    logging.debug(f"chdir into {get_project_root()} & remove {mylifedata_path}")
    os.chdir(get_project_root())
    shutil.rmtree(mylifedata_path, ignore_errors=True)


@pytest.fixture
def git_setup():
    """
    - Initializes the current directory as git repo
    - Creates a git remote in a neighboring directory
    - Configures the git repo to use the git remote by creating a first commit
    
    GIT_REMOTE_PATH = get_test_artifacts_path() / "git_remote"

    # Git init in the project
    shell_run("git init")
    shell_run("git config --local user.email 'Alex@your_domain.com'")
    shell_run("git config --local user.name 'Alex Datascientist'")

    # Create first git commit, necessary to push to remote below
    shell_run("git add .")
    shell_run("git commit -m 'Initial commit'")

    # Remove git remote folder
    shutil.rmtree(GIT_REMOTE_PATH, ignore_errors=True)
    # Create git remote folder
    GIT_REMOTE_PATH.mkdir(exist_ok=True)

    # Create and configure local git remote
    # Remote needs to be bare repo, see https://stackoverflow.com/a/11117928
    shell_run(f"git init --bare {GIT_REMOTE_PATH}")

    # Path needs to be absolute TODO the path isn't absolute? This comment was moved here, check if it still belongs here
    shell_run(f"git remote add local_git_remote {GIT_REMOTE_PATH}")
    # Configure local master to use local_git_remote
    shell_run("git push --set-upstream local_git_remote master")

    yield {"git_remote_path": GIT_REMOTE_PATH}

    # Teardown code starts below, see https://docs.pytest.org/en/stable/fixture.html#fixture-finalization-executing-teardown-code
    logging.info("Starting GIT-Teardown")

    # Remove remotes
    shutil.rmtree(GIT_REMOTE_PATH)
    """
    pass


@pytest.fixture
def dvc_setup():
    """
    Creates a dvc remote in a neighboring directory
    """
    DVC_REMOTE_PATH = get_test_artifacts_path() / "local_dvc_remote"

    # Remove dvc remote folder
    shutil.rmtree(DVC_REMOTE_PATH, ignore_errors=True)
    logging.info(f"Creating new dvc remote under{DVC_REMOTE_PATH}")
    DVC_REMOTE_PATH.mkdir(exist_ok=True)

    yield {"dvc_remote_path": DVC_REMOTE_PATH}

    # Teardown code starts below, see https://docs.pytest.org/en/stable/fixture.html#fixture-finalization-executing-teardown-code
    logging.info("Starting DVC-Teardown")
    # Remove remotes
    shutil.rmtree(DVC_REMOTE_PATH)


def dvc_repro(commit_msg):
    """
    Executes & git commits the complete dvc pipeline, pushes results to both git & dvc remote

    commit_msg : The git commit message
    """

    # Run the template pipeline
    TEST_ARTIFACTS_PATH = get_test_artifacts_path()
    import dvc.repo

    dvc_repo = dvc.repo.Repo(TEST_ARTIFACTS_PATH / PROJECT_NAME)
    dvc_repo.reproduce(all_pipelines=True)

    # Version the experiment results & push them
    shell_run("git add .")
    shell_run(f"git commit -m '{commit_msg}'")
    shell_run("git push")
    shell_run("dvc push")


def shell_run(cmd: str) -> subprocess.CompletedProcess:
    # runs the command and checks that the return code is 0 (that it executed without errors)
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, check=True)
    except subprocess.CalledProcessError as exc:
        logging.error(f"Command failed with exit code {exc.returncode}")
        # Try to decode outputs for better printing
        try:
            stdout = exc.stdout.decode("utf-8")
            stderr = exc.stderr.decode("utf-8")
        except UnicodeDecodeError:
            stdout = exc.stdout
            stderr = exc.stderr
        logging.error(f"stdout:\n{stdout}")
        logging.error(f"stderr:\n{stderr}")
        raise


def get_file_hash(path: Path) -> str:
    """
    Returns md5 hash of a file at path
    """

    hasher = hashlib.md5()

    # Read file as binary
    with path.open(mode="rb") as file_reader:

        while True:
            file_buffer = file_reader.read()
            # Detect the end of the file
            if not file_buffer:
                break

            # Add the buffer to the hasher
            hasher.update(file_buffer)

    # Calculate the hash of the complete file
    return hasher.hexdigest()
