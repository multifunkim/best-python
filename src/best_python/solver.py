import numpy as np
import mne

from .get_options import GetHeadModel, GetMEMOptions

def _solver(eng, head_model, mem_options):
    """Run L2 penalized regression and keep 10 strongest locations.

    Parameters
    ----------
    head_model : dict
        The head model, as returned by GetHeadModel.
    mem_options : dict
        The options for the MEM solver, as returned by GetMEMOptions.
    Returns
    -------
    X : array, (n_active_dipoles, n_times)
        The time series of the dipoles in the active set.
    active_set : array (n_dipoles)
        Array of bool. Entry j is True if dipole j is in the active set.
        We have ``X_full[active_set] == X`` where X_full is the full X matrix
        such that ``M = G X_full``.
    """
    # # Transfer M and G to MATLAB workspace
    eng.workspace['HeadModel'] = head_model
    eng.workspace['MEMOptions'] = mem_options

    # Prepare and call the MATLAB function using the variables in the workspace
    (Results, OPTIONS) = eng.eval("be_main_call(HeadModel, MEMOptions)", nargout=2)

    ImageGridAmp_np = np.array(Results["ImageGridAmp"])

    # TODO : Extract the active set, do not create a np.ones array
    return ImageGridAmp_np, np.ones(len(head_model["vertex_connectivity"][1]), dtype=bool)

def _mem_solver(eng, evoked, forward, noise_cov, loose=0.0, depth=0.8):
    """Call a custom solver on evoked data.

    This function does all the necessary computation:

    - to select the channels in the forward given the available ones in
      the data
    - to take into account the noise covariance and do the spatial whitening
    - to apply loose orientation constraint as MNE solvers
    - to apply a weigthing of the columns of the forward operator as in the
      weighted Minimum Norm formulation in order to limit the problem
      of depth bias.

    Parameters
    ----------
    eng: matlab.engine
        The MATLAB engine.
    evoked : instance of mne.Evoked
        The evoked data
    forward : instance of Forward
        The forward solution.
    noise_cov : instance of Covariance
        The noise covariance.
    head_model : dict
        The head model, as returned by GetHeadModel.
    memOptions : dict
        The options for the MEM solver, as returned by GetMEMOptions.
    loose : float in [0, 1] | 'auto'
        Value that weights the source variances of the dipole components
        that are parallel (tangential) to the cortical surface. If loose
        is 0 then the solution is computed with fixed orientation.
        If loose is 1, it corresponds to free orientations.
        The default value ('auto') is set to 0.2 for surface-oriented source
        space and set to 1.0 for volumic or discrete source space.
    depth : None | float in [0, 1]
        Depth weighting coefficients. If None, no depth weighting is performed.

    Returns
    -------
    stc : instance of SourceEstimate
        The source estimates.
    """
    # Import the necessary private functions
    from mne.inverse_sparse.mxne_inverse import (
        _make_sparse_stc,
        _prepare_gain,
        _reapply_source_weighting,
        is_fixed_orient,
    )

    all_ch_names = evoked.ch_names

    # Handle depth weighting and whitening (here is no weights)
    forward, gain, gain_info, whitener, source_weighting, mask = _prepare_gain(
        forward,
        evoked.info,
        noise_cov,
        pca=False,
        depth=depth,
        loose=loose,
        weights=None,
        weights_min=None,
        rank=None,
    )

    # Select channels of interest 
    channel_names = forward['sol']['row_names']
    indices_meg = [i for i, name in enumerate(channel_names) if name.startswith('MEG')]
    # indices_meg.pop()
    gain = gain[indices_meg, :]

    # Select channels of interest
    sel = [all_ch_names.index(name) for name in gain_info["ch_names"]]
    M = evoked.data[sel]

    data_type = ["MEG"]
    channel_types = [name.split(" ")[0] for name in channel_names]
    
    ####### SOLVER
    vertex_connectivity_matrix = mne.spatial_src_adjacency(forward['src'])

    default_cmem_pipeline_options = eng.be_cmem_pipelineoptions()
    
    head_model = GetHeadModel(gain, vertex_connectivity_matrix)
    mem_options = GetMEMOptions(default_cmem_pipeline_options, M, evoked.times, noise_cov, channel_types, data_type)

    X, active_set = _solver(eng, head_model, mem_options)
    # X = _reapply_source_weighting(X, source_weighting, active_set)

    stc = _make_sparse_stc(
        X, active_set, forward, tmin=evoked.times[0], tstep=1.0 / evoked.info["sfreq"]
    )

    return stc
