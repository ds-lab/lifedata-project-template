# README - {{cookiecutter.project_name}}


## 🔧 Setup

Follow the steps described in your console after creating a LIFEDATA project instance.

or 

```bash
conda env create --file <project instance path>/environment.yml

conda activate {{cookiecutter.project_name}}

### Configure git 

git config --local user.email 'Example@example_solutions.com'
git config --local user.name 'Alex Datascientist'

#### Remote repository
git remote add git_remote <repo url>

git add .
git commit -m "Initial commit"

git push --set-upstream git_remote main

#### Local repository
git init --bare <Path to local repository>
git remote add local_git_remote <Path to local repository>

git add .
git commit -m "Initial commit"

git push --set-upstream local_git_remote main
```


## 🧑‍🎨 Usage

### Using Annotation User Interface and Active Learning: 

Setup yarn for UI via `lifedata webui install`

Start database and WebUI via `lifedata start` for an example UI.

### Customization

To adjust the LIFEDATA configuration, start coding in the `lifedata_api` to use your data and logic in the Annotation UI.


### Machine Learning Service

Execute `dvc repro` to run a ML-pipeline with example data

### ML-Pipeline

The folder {{cookiecutter.project_name}} contains a example ML-pipeline. You can implement your own ML code. Appropriate places are marked with TODO in the python files.

To track the data versions with git, run:

```bash
git add dvc.lock data/raw.dvc

git commit -m <your message>

git push
```

#### Remove Stages

If you want to remove a stage from the ML-pipeline, e.g. if you don't want to use Active Learning with the `query`-stage, just remove the related code from the `dvc.yaml` file. A stage is defined similar to the following code:

```
  query:
    cmd: python {{cookiecutter.project_name}}/query/query.py
    deps:
    - data/label_state/
    - data/data_dvc/model_training/model.h5
    - {{cookiecutter.project_name}}/query/query.py
    outs:
    - data/data_dvc/query/queryset.csv
    params:
    - QUERY
```

#### Add Stages

To add a stage you can adjust the [dvc.yaml](dvc.yaml) in the same way. Additionally a folder and a script must be implemented in [{{cookiecutter.project_name}} ]({{cookiecutter.project_name}}) which executes the functions of the stage. For further informations see https://dvc.org/


#### ML Pipeline Configuration

The ML pipeline code in this project template is designed to run parameterized. To change the configuration, adjust the [params.py](params.py). Here you will find the appropriate parameters for each stage of the ML pipeline (e.g. the number of `EPOCHS` in the stage `MODEL_TRAINING`).


## 📔 Documentation

If you want to create a documentation in your lifedata project, you can run below commands (in the `./docs` folder):

### Create a html documentation

```bash
make html
```

### Open html documentation

```bash
start _build/html/index.html
```

### Clean html documentation

```bash
make clean
```

## 🦥 LIFEDATA

Found additional information about LIFEDATA in its [Github Repository](https://github.com/ds-lab/lifedata).

Have fun with that lifedata project template. Happy Coding!
