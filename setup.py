from setuptools import setup, find_packages
import subprocess
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_matlab_version():
    """
    matlab -h command will ouput, in the last line : 
    Version: 24.1.0.2568132
    """
    try:
        output = subprocess.check_output(['matlab', '-batch', '"disp(version)"'])
        version = re.search(r'(\d+\.\d+)\.\d+\.\d+', output.decode('utf-8')).group(1)
        return version
    except Exception as e:
        print("MATLAB not found or error getting version:", e)
        return None

print("Getting MATLAB version... Please wait.")
matlab_version = get_matlab_version()

install_requires = [
    'numpy>=1.26.4',
    'mne>=1.6.1'
]

if matlab_version:
    major = int(matlab_version.split('.')[0])
    minor = int(matlab_version.split('.')[1])
    install_requires.append(f'matlabengine>={major}.{minor}.0,<{major+1}.0.0')
else:
    raise ValueError("MATLAB version not found. Please try to install MATLAB, the command 'matlab -h' should work. If the problem persists, please manually install the 'matlab.engine' dependency matching your MATLAB version.")

setup(
    name="bestpython",
    version="0.0.2",
    author="MultiFunkIm Lab",
    author_email="ilian@iazz.fr",
    description="A python wrapper for the MEM source method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ilianAZZ/best-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires
)
