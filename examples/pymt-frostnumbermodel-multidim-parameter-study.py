"""An example of using Dakota as a component with PyMT.

This example requires a WMT executor with PyMT installed, as well as
the CSDMS Dakota interface and FrostNumberModel installed as
components.

"""
import os
from pymt.components import MultidimParameterStudy, FrostNumberModel
from dakotathon.utils import configure_parameters


c, d = FrostNumberModel(), MultidimParameterStudy()

parameters = {
    "component": type(c).__name__,
    "descriptors": ["T_air_min", "T_air_max"],
    "partitions": [3, 3],
    "lower_bounds": [-20.0, 5.0],
    "upper_bounds": [-5.0, 20.0],
    "response_descriptors": [
        "frostnumber__air",
        "frostnumber__surface",
        "frostnumber__stefan",
    ],
    "response_statistics": ["median", "median", "median"],
}

parameters, substitutes = configure_parameters(parameters)

parameters["run_directory"] = c.setup(os.getcwd(), **substitutes)

cfg_file = "frostnumber_model.cfg"  # get from pymt eventually
parameters["initialize_args"] = cfg_file
dtmpl_file = cfg_file + ".dtmpl"
os.rename(cfg_file, dtmpl_file)
parameters["template_file"] = dtmpl_file

d.setup(parameters["run_directory"], **parameters)

d.initialize("dakota.yaml")
d.update()
d.finalize()
