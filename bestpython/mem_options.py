class MEMOptions():
    
    def __init__(self, *args, **kwargs):
        # If data contains MEG or EEG data
        self.data_modality = None
        
        # Selected pipeline : cMEM, wMEM or rMEM
        self.pipeline = "cMEM"
        
        # If noise covariance is recomputed. If defined to "False", a noise covariance matrix must be given
        self.noise_cov = []
        self.noise_cov_recompute = True
        
        # Optional parameters
        self.active_mean_method = 2
        self.alpha_method = 3
        self.alpha_threshold = 0
        self.initial_lambda = 1
        self.depth_weigth_MNE = 0
        self.depth_weigth_MEM = 0
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def get_defined_mandatory(self):
        errors = []
        if self.data_modality is None:
            errors.append("data_modality can't be None")
        else:
            if self.data_modality.upper() not in ["MEG", "EEG"]:
                errors.append("data_modality must be in ['MEG', 'EEG']")
            self.data_modality = self.data_modality.upper()
        
        if self.pipeline not in ["cMEM", "wMEM", "rMEM"]:
            errors.append("pipeline must be in ['cMEM', 'wMEM', 'rMEM']")

        if self.noise_cov == [] and self.noise_cov_recompute is False:
            errors.append("If noise_cov_recompute defined to false, noise_cov can't be empty")
            
        return errors