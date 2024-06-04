function run_MEM(data, options_file)
    rng("shuffle")
    
    fprintf('Using ')
    system('hostname');
    disp('')
    fprintf('Data file : %s \n', data)
    fprintf('Option file : %s \n', options_file)


    % addpath(genpath('~/.brainstorm/plugins/nirstorm/nirstorm-master/bst_plugin/'));
    % addpath(genpath('~/.brainstorm/plugins/brainentropy/best-brainstorm-master/best'));
    % addpath(genpath('/NAS/home/edelaire/Documents/software/brainstorm3'))
    
    addpath(genpath('./nirstorm-master/bst_plugin'));
    addpath(genpath("C:/Users/Ilian/Documents/MATLAB/best-brainstorm/best"));
    addpath(genpath('C:/Users/Ilian/Documents/dev/brainstorm3'))

    sOption = load(data).sOutput;
    output_file = strrep(data,'in','out');
    output_folder = fileparts(output_file);
    if ~exist(output_folder)
        mkdir(output_folder)
    end
    
    % Loading options 
    ChannelMat = sOption.ChannelMat;
    cortex = sOption.cortex;
    nirs_head_model = sOption.nirs_head_model;
    OPTIONS = jsondecode(fileread(options_file));
    OPTIONS.DataFile = sOption.OPTIONS.DataFile;
    OPTIONS.DataTypes = sOption.OPTIONS.DataTypes;
    OPTIONS.ResultFile = sOption.OPTIONS.ResultFile;
    OPTIONS.HeadModelFile = sOption.OPTIONS.HeadModelFile;
    OPTIONS.Comment       =  sOption.OPTIONS.Comment;
    sStudy = sOption.OPTIONS.sStudy; 
    sDataIn = sOption.sDataIn;
    fprintf('Data  : %s \n', sDataIn.Comment)
    fprintf('--------------------------------\n')

    nb_nodes = size(cortex.Vertices, 1);
    nb_samples = length(sDataIn.Time);
    nb_wavelengths  = length(ChannelMat.Nirs.Wavelengths);

    HM.SurfaceFile = nirs_head_model.SurfaceFile;
    
    % try to start parralel port
    
    if isempty(gcp('nocreate'))
        try
            local_cluster = parcluster('Processes');

            % Modify the JobStorageLocation to $SLURM_TMPDIR
            slurm_tmp_dir = fullfile('./', char(floor(26*rand(1, 10)) + 65));
            if ~exist(slurm_tmp_dir)
                mkdir(slurm_tmp_dir)
            end
            local_cluster.JobStorageLocation = slurm_tmp_dir;
            disp(' MEM > Starting parpool')

            parpool(local_cluster,  16);

        catch
            disp(' MEM > FAILED TO OPEN PARALLEL PORT ! THX CRAPPY perform')
            OPTIONS.MEMpaneloptions.solver.parallel_matlab = 0;
        end
    end

    % define the reconstruction FOV
    thresh_dis2cortex       = OPTIONS.thresh_dis2cortex / 100;
    valid_nodes             = nst_headmodel_get_FOV(ChannelMat, cortex, thresh_dis2cortex,sDataIn.ChannelFlag );


    % estimate the neighborhood order (goal: # of clusters ~= # of good channels) 
    fprintf('MEM > Estimating neighborhood order\n'); 
    if OPTIONS.auto_neighborhood_order
        swl = ['WL' num2str(ChannelMat.Nirs.Wavelengths(1))];
        n_channel = sum(strcmpi({ChannelMat.Channel.Group}, swl) & (sDataIn.ChannelFlag>0)');
    
        nbo = process_nst_cmem('estimate_nbo',cortex, valid_nodes, n_channel, 1 );
        fprintf('MEM > Using a NBO of %d\n', nbo); 
        OPTIONS.MEMpaneloptions.clustering.neighborhood_order = nbo;
    end


    OPTIONS.MEMpaneloptions.optional.cortex_vertices = cortex.Vertices; %(valid_nodes, :); 
    HM.vertex_connectivity = cortex.VertConn; %(valid_nodes, valid_nodes);

    dOD_sources = zeros(nb_nodes, nb_wavelengths, nb_samples);
    diagnosis   = [];

    for iwl=1:nb_wavelengths
        
        swl = ['WL' num2str(ChannelMat.Nirs.Wavelengths(iwl))];
        selected_chans = strcmpi({ChannelMat.Channel.Group}, swl) & (sDataIn.ChannelFlag>0)';
        fprintf('MEM > Computing MEM for wavelength %s\n', swl); 

        OPTIONS.GoodChannel     = ones(sum(selected_chans), 1);
        OPTIONS.ChannelFlag     = ones(sum(selected_chans), 1);
        OPTIONS.Channel         = ChannelMat.Channel(selected_chans);
        OPTIONS.DataTime        = round(sDataIn.Time,6);
        OPTIONS.Data            = sDataIn.F(selected_chans,:);
    
        gain = nst_headmodel_get_gains(nirs_head_model,iwl, ChannelMat.Channel, find(selected_chans));
        
        % Remove 0 from the gain matrixHeadModel.Gain(1).matrix
        tmp = gain(:,valid_nodes);
        tmp(tmp == 0) = min(tmp(tmp > 0));
    
        HM.Gain(1).matrix = tmp;
        HM.Gain(1).modality = 'NIRS';


        %% launch MEM (cMEM only in current version)
        MEMoptions = prepOptions(OPTIONS);
        [Results, O_updated] = be_main_call(HM, MEMoptions);

        %cMEM results
        grid_amp = zeros(nb_nodes, nb_samples); 
        grid_amp(valid_nodes,:) = Results.ImageGridAmp;
        
        dOD_sources(:, iwl, :)  = grid_amp;
        Results.MEMoptions.automatic.valid_nodes = valid_nodes;
        diagnosis          = [diagnosis Results.MEMoptions.automatic];
    end

    hb_extinctions = nst_get_hb_extinctions(ChannelMat.Nirs.Wavelengths);
    hb_extinctions = hb_extinctions ./10;% mm-1.mole-1.L

    Hb_sources = zeros(nb_nodes, 3, nb_samples);
    for idx=1:length(valid_nodes)
        inode = valid_nodes(idx);
        Hb_sources(inode, 1:2, :) = pinv(hb_extinctions) * ...
                                    squeeze(dOD_sources(inode, :, :));
    
    end
    Hb_sources(:,3,:) = squeeze(sum(Hb_sources, 2));

    save(output_file, 'sStudy', 'OPTIONS', 'dOD_sources','Hb_sources', 'diagnosis');
end


function MEMoptions = prepOptions(OPTIONS)

    Def_OPTIONS = be_main_call();
    MEMoptions = be_struct_copy_fields( Def_OPTIONS, OPTIONS.MEMpaneloptions, [],1 );
    
    % mandatory
    MEMoptions.mandatory.DataTime                       =   OPTIONS.DataTime;
    MEMoptions.mandatory.DataTypes                      =   OPTIONS.DataTypes;
    MEMoptions.mandatory.ChannelTypes                   =   {OPTIONS.Channel.Type};
    MEMoptions.mandatory.Data                           =   OPTIONS.Data;
    % optional
    MEMoptions.optional.Channel                         =   OPTIONS.Channel;
    MEMoptions.optional.ChannelFlag                     =   OPTIONS.ChannelFlag;
    MEMoptions.optional.DataFile                        =   OPTIONS.DataFile;
    MEMoptions.optional.ResultFile                      =   OPTIONS.ResultFile;
    MEMoptions.optional.HeadModelFile                   =   OPTIONS.HeadModelFile;
    MEMoptions.optional.Comment                         =   OPTIONS.Comment;
    MEMoptions.optional.normalization                   =   'fixed';

    % automatic
    MEMoptions.automatic.stand_alone                    =   1;
    MEMoptions.automatic.GoodChannel                    =   OPTIONS.GoodChannel;
    MEMoptions.automatic.Comment                        =   OPTIONS.Comment;

    MEMoptions.wavelet.selected_scales                  =   MEMoptions.wavelet.selected_scales'; 
    MEMoptions.wavelet.single_box                       =   0;
    
    % solver
    MEMoptions.solver.NoiseCov = []; 

end


run_MEM("C:/Users/Ilian/Documents/dev/python-brainstorm/data_sim_240417_1128.mat", "C:/Users/Ilian/Documents/dev/python-brainstorm/wMEM_options.json")