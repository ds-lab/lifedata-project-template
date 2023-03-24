Hi there, {{cookiecutter.project_name}} fellow!
===============================================

This is the documentation for the {{cookiecutter.project_name}} project. {{cookiecutter.project_name}} 
is a concrete project instance of the lifedata cookiecutter.
It provides a simple dvc pipeline and template code for a data science project with optional active 
learning connectivity. 

What `{{cookiecutter.project_name}}` has to offer:

- Offers a simple data science project structure
- Offers a simple and expandable dvc pipeline for data science projects
- Provides an optional connection to the LIFEDATA framework code to annotate data.
- Provides a simple and expandable html sphinx documentation structure 


Getting started
---------------

To get a grasp for the {{cookiecutter.project_name}} project structure have a look at the 
:ref:`overview section <overview>`. To get a first glance of how to use 
{{cookiecutter.project_name}} follow the :ref:`README section <use>` and then 
jump over to the :ref:`tutorial section <tutorials>`. 
An insight into the project architecture is provided by the :ref:`architecture section <architecture>` 
and a short code description can be viewed in the :ref:`code documentation section <code>`

.. toctree::
   :maxdepth: 1
   :caption: Contents

   sphinx/overview

   sphinx/readme

   sphinx/tutorials

   sphinx/architecture

   sphinx/code

   sphinx/contact


The documentation is written and built using `Sphinx`_. The documentation is generated out of .rst 
and .py files and creates HTML files in the ``_build`` directory. To add further documentation sections
see `Sphinx`_. 

.. _Sphinx: https://www.sphinx-doc.org/


:ref:`genindex` | :ref:`modindex` | :ref:`search`