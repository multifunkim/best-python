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
import bestpython

# Create a new instance of the wrapper
# You need to provide the path to the best-brainstorm root folder
matlab_wrapper = bestpython.MatlabWrapper("C:/PATH/OF/BEST-BRAINSTORM/ROOT/FOLDER")

# Define the mandatory options
mem_options = bestpython.MEMOptions(
    data_modality="MEG",
    time_segment = [0.04, 0.18],
    baseline_time = [0.04, 0.1]
)

# Call the solver
stc = matlab_wrapper.mem_solver(evoked, forward, noise_cov, MEMOptions=mem_options)

```

## Full example
You can find a full example in the `tests/test.py` file [link](https://github.com/multifunkim/best-python/blob/main/tests/test.py).


## License
BEst is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. BEst is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should receive a copy of the GNU General Public License along with BEst. If not, get it here.

minFunc. Schmidt M. see [license](http://www.di.ens.fr/~mschmidt/Software/copyright.html)



## References
The references to be acknowledged for each method are:

- **cMEM with stable clustering**. [MEG source localization of spatially extended generators of epileptic activity: comparing entropic and hierarchical bayesian approaches.](http://www.ncbi.nlm.nih.gov/pubmed/23418485) Chowdhury RA, Lina JM, Kobayashi E, Grova C. PLoS One. 2013;8(2):e55969

- **wMEM**. [Wavelet-based localization of oscillatory sources from magnetoencephalography data.](http://www.ncbi.nlm.nih.gov/pubmed/22410322) Lina J, Chowdhury R, Lemay E, Kobayashi E, Grova C. IEEE Trans Biomed Eng. 2012 Mar 6.

Additional technical references:

- **MEM**. [Biomagnetic source detection by maximum entropy and graphical models.](http://www.ncbi.nlm.nih.gov/pubmed/15000374) Amblard C, Lapalme E, Lina JM. IEEE Trans Biomed Eng. 2004 Mar;51(3):427-42.

- **MEM and Parcelization**. [Data-driven parceling and entropic inference in MEG.](http://www.ncbi.nlm.nih.gov/pubmed/16426867) Lapalme E, Lina JM, Mattout J. Neuroimage. 2006 Mar;30(1):160-71.

- **MSP**. [Multivariate source prelocalization (MSP): use of functionally informed basis functions for better conditioning the MEG inverse problem.](http://www.ncbi.nlm.nih.gov/pubmed/15907296) Mattout J, Pélégrini-Issac M, Garnero L, Benali H. Neuroimage. 2005 Jun;26(2):356-73.

Validation and applications:

- [Evaluation of EEG localization methods using realistic simulations of interictal spikes.](http://www.ncbi.nlm.nih.gov/pubmed/16271483) Grova C, Daunizeau J, Lina JM, Bénar CG, Benali H, Gotman J. Neuroimage. 2006 Feb 1;29(3):734-53.

- [Concordance between distributed EEG source localization and simultaneous EEG-fMRI studies of epileptic spikes.](http://www.ncbi.nlm.nih.gov/pubmed/17945511) Grova C, Daunizeau J, Kobayashi E, Bagshaw AP, Lina JM, Dubeau F, Gotman J. Neuroimage. 2008 Jan 15;39(2):755-74

- [Spatial correlation of hemodynamic changes related to interictal epileptic discharges with electric and magnetic source imaging.](http://www.ncbi.nlm.nih.gov/pubmed/24615912) Heers M, Hedrich T, An D, Dubeau F, Gotman J, Grova C, Kobayashi E. Hum Brain Mapp. 2014 Feb 24.

- [Optimal eye-gaze fixation position for face-related neural responses.](http://www.ncbi.nlm.nih.gov/pubmed/23762224) Zerouali Y, Lina JM, Jemel B. PLoS One. 2013 Jun 6;8(6):e60128.

- [Oscillatory activity in parietal and dorsolateral prefrontal cortex during retention in visual short-term memory: additive effects of spatial attention and memory load.](http://www.ncbi.nlm.nih.gov/pubmed/19384891) Grimault S, Robitaille N, Grova C, Lina JM, Dubarry AS, Jolicoeur P. Hum Brain Mapp. 2009 Oct;30(10):3378-92.
