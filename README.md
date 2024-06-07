# best-python

The goal of this project is to provide a way to use the best-brainstorm Matlab solvers in Python, compatible with MNE-Python.

For now, the project is using matlab.engine to call the best-brainstorm functions from Python, so you need to have Matlab installed on the computer.

## Installation
### Matlab and matlabengine package installation
You need to have Matlab installed on your computer. Then, you can install the matlabengine package matching the Matlab version you have installed.

You can run the `get_matlab_version.py` script to get the version of Matlab installed on your computer.
```bash
python get_matlab_version.py
```

It should return something like:
```
Getting MATLAB version... Please wait.
MATLAB version found: 24.1.0.123456
Run the following command in the terminal to install the required version:
pip install matlabengine>=24.1.0,<25.0.0
```

Then, you can install the matlabengine package with the version found:
```bash
pip install matlabengine>=24.1.0,<25.0.0
```

After that, you can install the best-python package:
```bash
pip install best-python
```

### Best-brainstorm installation
As the best-python package is using the best-brainstorm functions, you need to have the best-brainstorm toolbox downloaded on your computer.

You can download the best-brainstorm toolbox from the [best-brainstorm github](https://github.com/multifunkim/best-brainstorm).

## Usage
You can use the functions from the best-python package like this:
```python
import best_python

# Create a new instance of the wrapper
# You need to provide the path to the best-brainstorm root folder
matlab_wrapper = best_python.MatlabWrapper("C:/PATH/OF/BEST-BRAINSTORM/ROOT/FOLDER")

# Call the solver
stc = matlab_wrapper.mem_solver(evoked, forward, noise_cov, depth=0.8, loose=0.0)
```

## Full example
You can find a full example in the `tests/test.py` file [link](./tests/test.py).
