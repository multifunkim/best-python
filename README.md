# best-python

The goal of this project is to provide a way to use the best-brainstorm Matlab solvers in Python, compatible with MNE-Python.

For now, the project is using matlab.engine to call the best-brainstorm functions from Python, so you need to have Matlab installed on the computer.

## Entry point
File is : [call_mem_with_mne_data.ipynb](call_mem_with_mne_data.ipynb)

## Requirements
- Python 3.6 or higher (with pip)
- Matlab
- Python "matlab.engine" module, compatible with the installed Matlab version
- best-brainstorm ~~[Github repo](https://github.com/multifunkim/best-brainstorm)~~

/!\ On May 14, 2024, the code is not compatible with the current version of best-brainstorm, please use the version provided in the link above.

[Github repo](https://github.com/Edouard2laire/best-brainstorm/tree/wMEM) with the branch `wMEM` contains the compatible version of best-brainstorm.

[Direct Download link](https://github.com/Edouard2laire/best-brainstorm/archive/refs/heads/wMEM.zip)

## Installation
- Please make sure that (look for "HERE" in the code):
    - You have installed the correct matlab engine package version, depending on your installed Matlab software version
    - Add the path to the best-brainstorm folder in the Matlab path