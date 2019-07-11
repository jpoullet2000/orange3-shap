[![Build Status](https://travis-ci.org/jpoullet2000/orange3-shap.svg?branch=master)](https://travis-ci.org/jpoullet2000/orange3-shap)

Orange3-Shap
============

Orange add-on for explaining Random Forest output with Shapley method.

**License: CC-BY-NC-3.0**

Package documentation: http://orange3-shap.readthedocs.io/

Installing
----------

### With Anaconda

The easiest way to install Orange3-Shap on a non-GNU/Linux system is
with [Anaconda] distribution for your OS (Python version >=3.6).
In your Anaconda Prompt, first add conda-forge to your channels:

    conda config --add channels conda-forge

Then install Orange3:

    conda install orange3

This will install the latest release of Orange. Then install Orange3-Shap:
  
    pip install orange3-shap

Run:

    orange-canvas

to open Orange and check if everything is installed properly.


[Anaconda]: https://www.continuum.io/downloads

### From source

To install the add-on from source

    # Clone the repository and move into it
    git clone https://github.com/jpoullet2000/orange3-shap.git
    cd orange3-shap

    # Install corresponding wheels for your OS:
    pip install some-wheel.whl

    # Install Orange3-Shap in editable/development mode.
    pip install -e .

To register this add-on with Orange, run

    python setup.py install
