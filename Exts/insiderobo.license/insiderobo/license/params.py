# parameters
import os

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the directory of the script file
script_directory = os.path.dirname(script_path)

LICENSE2PATH = {
    "kinova": os.path.join(script_directory, "licences", "KINOVA_LICENSE.txt"),
    "ufactory": os.path.join(script_directory, "licences", "UFACTORY_LICENSE.txt"),
    "digitalbotlab": os.path.join(script_directory, "licences", "DIGITALBOTLAB_EXTENDED_LICENSE.txt"),
    "universal_robot": os.path.join(script_directory, "licences", "UR_LICENESE_INFO.txt"),
    "franka": os.path.join(script_directory, "licences", "FRANKA_LICENSE.txt"),
}