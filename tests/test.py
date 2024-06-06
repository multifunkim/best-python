import os
import sys
import mne
from mne.datasets import sample

# Add the path to the src folder
p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.append(p)
import best_python

# Load data
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
matlab_wrapper = best_python.MatlabWrapper("C:/Users/Ilian/Documents/MATLAB/best-brainstorm")
stc = matlab_wrapper.mem_solver(evoked, forward, noise_cov, depth=0.8, loose=0.0)
###############

# Display results
initial_time = -0.1
brain_cmem = stc.plot(
    subjects_dir=subjects_dir,
    initial_time=initial_time,
    smoothing_steps=7,
    hemi='both',
)
brain_cmem.add_text(0.1, 0.9, "cMEM", "title", font_size=14)