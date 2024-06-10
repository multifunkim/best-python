import os
import sys
import mne
from mne.datasets import sample
import bestpython

# Load data from MNE
data_path = sample.data_path()
meg_path = data_path / "MEG" / "sample"
fwd_fname = meg_path / "sample_audvis-meg-eeg-oct-6-fwd.fif"
ave_fname = meg_path / "sample_audvis-ave.fif"
cov_fname = meg_path / "sample_audvis-shrunk-cov.fif"
subjects_dir = data_path / "subjects"
condition = "Left Auditory"

# Prepare data
noise_cov = mne.read_cov(cov_fname)
evoked = mne.read_evokeds(ave_fname, condition=condition, baseline=(None, 0))
evoked.crop(tmin=0.04, tmax=0.18)
evoked = evoked.pick(picks="meg", exclude="bads")
forward = mne.read_forward_solution(fwd_fname)
forward = mne.convert_forward_solution(forward, force_fixed=True, surf_ori=True)

###############
# Call solver
matlab_wrapper = bestpython.MatlabWrapper("C:/Users/Ilian/Documents/MATLAB/best-brainstorm")
mem_options = bestpython.MEMOptions(data_modality="MEG")
stc = matlab_wrapper.mem_solver(evoked, forward, noise_cov, depth=0.8, loose=0.0, MEMOptions=mem_options)
###############

# Display results
initial_time = -0.1
brain = mne.viz.plot_source_estimates(
    stc,
    subject='sample',
    subjects_dir=subjects_dir,
    initial_time=initial_time,
    smoothing_steps=7,
    hemi='both',
    brain_kwargs={"block":True}
)
brain.add_text(0.1, 0.9, "cMEM", "title", font_size=14)