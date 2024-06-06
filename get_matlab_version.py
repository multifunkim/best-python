import re 
import subprocess

def get_matlab_version():
    """
    matlab -h command will ouput, in the last line : 
    Version: 24.1.0.2568132
    """
    try:
        output = subprocess.check_output(["matlab", "-batch", "\"disp(version)\""])
        return output
    except Exception as e:
        print("MATLAB not found or error getting version:", e)
        return None

if __name__ == "__main__":
    print("Getting MATLAB version... Please wait.")
    matlab_version = get_matlab_version()
    
    major_version = re.search(r"(\d+\.\d+)\.\d+\.\d+", matlab_version.decode("utf-8")).group(1)
    
    if matlab_version:
        print("MATLAB version found:", matlab_version)
        print("Run the following command in the terminal to install the required version:")
        major = int(major_version.split(".")[0])
        minor = int(major_version.split(".")[1])
        print(f"pip install matlabengine>={major}.{minor}.0,<{major+1}.0.0")
    else:
        print("MATLAB version not found. " +
            "\nIf The command \"matlab -h\" does not work, " +
            "\n\t- Matlab not installed, " +
            "\n\t- Matlab not in the PATH, " +
            "\nIf the command \"matlab -h\" works, " +
            "\nIssue with this code, please report it and get the version in the matlab \"Help\" menu.")
