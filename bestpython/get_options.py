import matlab

def GetHeadModel(G, VertexConnectivityMatrix):
    """Generate the MEM "HeadModel" struct

    Parameters
    ----------
    G : np_array, shape (n_channels, n_dipoles)
        The gain matrix a.k.a. the forward operator. The number of locations
        is n_dipoles / n_orient. n_orient will be 1 for a fixed orientation
        constraint or 3 when using a free orientation model.
    VertexConnectivityMatrix : sparse_matrix, shape (n_dipoles, n_dipoles)
        The adjacency matrix of the source space.
        
    Returns
    -------
    HeadModel : dict
    """
    HeadModel = {}
    HeadModel["Gain"] = {
        "matrix":  matlab.double(G.tolist()),
        "modality": "MEG",
    }
    HeadModel["vertex_connectivity"] =  matlab.double(VertexConnectivityMatrix.toarray().tolist())

    return HeadModel


def GetMEMOptions(default_pipeline, M, DataTimes, NoiseCov, ChannelTypes, DataTypes):
    """Generate the MEM "HeadModel" struct

    Parameters
    ----------
    M : np_array, shape (n_channels, n_times)
        The whitened data.
    DataTimes : np_array, shape (n_times,)
        The time points of the data.
    NoiseCov : np_array, shape (n_channels, n_channels)
        The noise covariance matrix.
    ChannelTypes : list of str (n_channels,)
        The type of each channel.
    DataTypes : str
        The type of the data ("MEG" or "EEG").

    Returns
    -------
    MEMOptions : dict
    """
    MEMOptions = default_pipeline

    MEMOptions["mandatory"] = {} 
    MEMOptions["mandatory"]["DataTime"] = matlab.double(DataTimes.tolist())
    MEMOptions["mandatory"]["Data"] = matlab.double(M.tolist())
    
    MEMOptions["mandatory"]["ChannelTypes"] = ChannelTypes
    MEMOptions["mandatory"]["DataTypes"] = DataTypes
    MEMOptions["mandatory"]["pipeline"] =  "cMEM"


    MEMOptions["optional"]["DataFile"] = ""
    MEMOptions["optional"]["HeadModelFile"] = ""
    # NoiseCov can be empty if Baseline is defined
    MEMOptions["optional"]["Baseline"] = matlab.double(M[:,:10].tolist())
    MEMOptions["optional"]["BaselineTime"] = matlab.double([DataTimes[0], DataTimes[10]])
    MEMOptions["optional"]["TimeSegment"] = matlab.double([DataTimes[0], DataTimes[10]])
    MEMOptions["optional"]["Channel"] = []
    MEMOptions["optional"]["ChannelFlag"] = []

    # MEMOptions["solver"]["NoiseCov"] = matlab.double(NoiseCov.tolist())
    MEMOptions["solver"]["NoiseCov"] = []
    MEMOptions["solver"]["NoiseCov_recompute"] = 1


    # Default parameters
    MEMOptions["optional"]["active_mean_method"] = 2
    MEMOptions["optional"]["alpha_method"] = 3
    MEMOptions["optional"]["alpha_threshold"] = 0
    MEMOptions["optional"]["initial_lambda"] = 1
    MEMOptions["optional"]["depth_weigth_MNE"] = 0
    MEMOptions["optional"]["depth_weigth_MEM"] = 0

    return MEMOptions