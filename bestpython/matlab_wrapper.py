import matlab.engine
from .solver import _mem_solver

class MatlabWrapper():
    def __init__(self, matlab_path):
        self.eng = matlab.engine.start_matlab("-desktop")
        self.eng.eval(f"addpath(genpath('{matlab_path}'))", nargout=0)
        
    def mem_solver(self, evoked, forward, noise_cov, MEMOptions=None):
        return _mem_solver(self.eng, evoked, forward, noise_cov, MEMOptions)