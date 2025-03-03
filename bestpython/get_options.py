import matlab

def GetHeadModel(G, VertexConnectivityMatrix, PyMemOptions):
    """Generate the MEM "HeadModel" struct

    Parameters
    ----------
    G : np_array, shape (n_channels, n_dipoles)
        The gain matrix a.k.a. the forward operator. The number of locations
        is n_dipoles / n_orient. n_orient will be 1 for a fixed orientation
        constraint or 3 when using a free orientation model.
    VertexConnectivityMatrix : sparse_matrix, shape (n_dipoles, n_dipoles)
        The adjacency matrix of the source space.
    PyMemOptions : MEMOptions
        Contains all MEM options

    Returns
    -------
    HeadModel : dict
    """
    HeadModel = {}
    HeadModel["Gain"] = {
        "matrix":  matlab.double(G.tolist()),
        "modality": PyMemOptions.data_modality,
    }
    HeadModel["vertex_connectivity"] =  matlab.double(VertexConnectivityMatrix.toarray().tolist())

    return HeadModel


def GetMEMOptions(default_pipeline, M, DataTimes, NoiseCov, PyMemOptions):
    """Generate the MEM "HeadModel" struct

    Parameters
    ----------
    M : np_array, shape (n_channels, n_times)
        The whitened data.
    DataTimes : np_array, shape (n_times,)
        The time points of the data.
    NoiseCov : np_array, shape (n_channels, n_channels)
        The noise covariance matrix.
    PyMemOptions : MEMOptions
        Contains all MEM options

    Returns
    -------
    MEMOptions : dict
    """
    MEMOptions = default_pipeline

    MEMOptions["mandatory"] = {} 
    MEMOptions["mandatory"]["DataTime"] = matlab.double(DataTimes.tolist())
    MEMOptions["mandatory"]["Data"] = matlab.double(M.tolist())
    
    MEMOptions["mandatory"]["ChannelTypes"] = [PyMemOptions.data_modality] * M.shape[0]
    MEMOptions["mandatory"]["DataTypes"] = [PyMemOptions.data_modality]
    MEMOptions["mandatory"]["pipeline"] =  PyMemOptions.pipeline


    MEMOptions["optional"]["DataFile"] = ""
    MEMOptions["optional"]["HeadModelFile"] = ""
    # NoiseCov can be empty if Baseline is defined
    MEMOptions["optional"]["BaselineHistory"] = ["within"],
    # MEMOptions["optional"]["Baseline"] = matlab.double(M[:,:10].tolist())
    MEMOptions["optional"]["BaselineTime"] = matlab.double(PyMemOptions.baseline_time)
    MEMOptions["optional"]["TimeSegment"] = matlab.double(PyMemOptions.time_segment)
    MEMOptions["optional"]["Channel"] = []
    MEMOptions["optional"]["ChannelFlag"] = []

    # MEMOptions["solver"]["NoiseCov"] = matlab.double(NoiseCov.tolist())
    MEMOptions["solver"]["NoiseCov"] = PyMemOptions.noise_cov
    MEMOptions["solver"]["NoiseCov_recompute"] = PyMemOptions.noise_cov_recompute


    # Default parameters
    MEMOptions["optional"]["active_mean_method"] = PyMemOptions.active_mean_method
    MEMOptions["optional"]["alpha_method"] = PyMemOptions.alpha_method
    MEMOptions["optional"]["alpha_threshold"] = PyMemOptions.alpha_threshold
    MEMOptions["optional"]["initial_lambda"] = PyMemOptions.initial_lambda
    MEMOptions["optional"]["depth_weigth_MNE"] = PyMemOptions.depth_weigth_MNE
    MEMOptions["optional"]["depth_weigth_MEM"] = PyMemOptions.depth_weigth_MEM

    # Specify the output form
    MEMOptions["output"] = {} 
    MEMOptions["output"]["save_factor"] = 0

    return MEMOptions