.. _overview:

Overview
========

Folder structure
----------------

The project consists of 4 folders. The description follows in the below sections.

{{cookiecutter.project_name}} folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This folder contains the scripts that are used when running the dvc pipeline. 
As a developer you need to make changes to these scripts. Where and which changes 
have to be made is marked and described with `TODO` in the code. 


data folder
^^^^^^^^^^^

**data_dvc**

In this folder the outputs of the dvc pipeline stages are stored. 

**label_state**

For an active learning pipeline this folder contains the information 
about which samples are already annotated and which still have to be annotated. 

**raw**

This folder contains the raw samples.


docs folder
^^^^^^^^^^^

This folder contains files that are used for the html documentation structure. 
Furthermore, architecture diagrams can be stored here. If changes or extensions 
to the html documentation are required, these are made in this folder. 


reports folder
^^^^^^^^^^^^^^

Reports that are created during the execution of the dvc pipeline are stored in this folder. 