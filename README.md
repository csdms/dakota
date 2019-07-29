[![Build Status](https://travis-ci.org/csdms/dakotathon.svg?branch=master)](https://travis-ci.org/csdms/dakotathon)
[![Code Health](https://landscape.io/github/csdms/dakotathon/master/landscape.svg?style=flat)](https://landscape.io/github/csdms/dakotathon/master)
[![Coverage Status](https://coveralls.io/repos/csdms/dakotathon/badge.svg?branch=master)](https://coveralls.io/r/csdms/dakotathon?branch=master)
[![Documentation Status](https://readthedocs.org/projects/csdms-dakota/badge/?version=latest)](https://readthedocs.org/projects/csdms-dakota/?badge=latest)
[![Anaconda-Server Badge](https://anaconda.org/csdms-stack/dakotathon/badges/version.svg)](https://anaconda.org/csdms-stack/dakotathon)
[![Anaconda-Server Badge](https://anaconda.org/csdms-stack/dakotathon/badges/platforms.svg)](https://anaconda.org/csdms-stack/dakotathon)
[![Anaconda-Server Badge](https://anaconda.org/csdms-stack/dakotathon/badges/downloads.svg)](https://anaconda.org/csdms-stack/dakotathon)

# Dakotathon

Dakotathon provides
a [Basic Model Interface](https://bmi.readthedocs.io)
and a Python API for a subset of the methods
included in the [Dakota](https://dakota.sandia.gov/)
iterative systems analysis toolkit,
including:

* [vector_parameter_study](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-vector_parameter_study.html),
* [centered_parameter_study](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-centered_parameter_study.html),
* [multidim_parameter_study](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-multidim_parameter_study.html),
* [psuade_moat](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-psuade_moat.html),
* [sampling](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-sampling.html),
* [polynomial_chaos](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-polynomial_chaos.html), and
* [stoch_collocation](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-stoch_collocation.html).

Dakotathon is currently beta-level software
supported on Linux and macOS.
API documentation is available at http://csdms-dakota.readthedocs.io.

## Installation

Install Dakotathon into an Anaconda Python distribution with

    $ conda install -c csdms-stack dakotathon

or install from source with

	$ git clone https://github.com/csdms/dakotathon.git
	$ cd dakotathon
	$ python setup.py install

Dakotathon requires Dakota 6.1 or greater.
Install Dakota through conda with

    $ conda install -c csdms-stack -c conda-forge dakota

or, follow the instructions on the Dakota website
for [downloading](https://dakota.sandia.gov/download.html) and
[installing](https://dakota.sandia.gov/content/install-linux-macosx)
a precompiled Dakota binary for your system.

## Execution: standalone

Import Dakotathon into a Python session with:

	>>> from dakotathon import Dakota

Create a `Dakota` instance,
specifying a Dakota analysis method:

	>>> d = Dakota(method='vector_parameter_study')

To run a sample case,
create a Dakota input file
from the default vector parameter study
and call Dakota:

	>>> d.write_input_file()
	>>> d.run()

Dakota output is written to two files,
**dakota.out** (run information)
and
**dakota.dat** (tabular output),
in the current directory.

For more in-depth examples of using Dakotathon
as a standalone Python package,
see the Jupyter Notebooks
in the [examples](./examples) directory
of this repository.


### Note

If you're using Anaconda IPython on macOS,
include the `DYLD_LIBRARY_PATH` environment variable
in your session before calling the `run` method with:

```python
>>> from dakotathon.utils import add_dyld_library_path
>>> add_dyld_library_path()
```

See https://github.com/csdms/dakotathon/issues/17 for more information.

## Execution: in PyMT

Dakotathon can also be called as a component in
[PyMT](https://github.com/csdms/pymt).
For example,
to perform a centered parameter study on the Hydrotrend component,
start with imports:

```python
import os
from pymt.components import CenteredParameterStudy, Hydrotrend
from dakotathon.utils import configure_parameters
```

then create instances of the Hydrotrend and Dakota components:

```python
h, c = Hydrotrend(), CenteredParameterStudy()
```

Next,
set up a dict of parameters for the experiment:

```python
experiment = {
  'component': type(c).__name__,
  'run_duration': 10,                # years
  'auxiliary_files': 'HYDRO0.HYPS',  # the default Waipaoa hypsometry
  'descriptors': ['starting_mean_annual_temperature',
                  'total_annual_precipitation'],
  'initial_point': [15.0, 2.0],
  'steps_per_variable': [2, 5],
  'step_vector': [2.5, 0.2],
  'response_descriptors': ['channel_exit_water_sediment~suspended__mass_flow_rate',
                           'channel_exit_water__volume_flow_rate'],
  'response_statistics': ['median', 'mean']
}
```

and use a helper function
to format the parameters for Dakota and for Hydrotrend:

```python
cparameters, hparameters = configure_parameters(experiment)
```

Set up the Hydrotrend component:

```python
cparameters['run_directory'] = h.setup(os.getcwd(), **hparameters)
```

Create the Dakota template file from the Hydrotrend input file:

```python
cfg_file = 'HYDRO.IN'  # get from pymt eventually
dtmpl_file = cfg_file + '.dtmpl'
os.rename(cfg_file, dtmpl_file)
cparameters['template_file'] = dtmpl_file
```

Set up the Dakota component:

```python
c.setup(dparameters['run_directory'], **cparameters)
```

then initialize, run, and finalize the Dakota component:

```python
c.initialize('dakota.yaml')
c.update()
c.finalize()
```

Dakota output is written to two files,
**dakota.out** (run information)
and
**dakota.dat** (tabular output),
in the current directory.

For more in-depth examples of using Dakotathon with PyMT,
see the Python scripts
in the [examples](./examples) directory
of this repository.

## Contributing

Dakotathon is open source software,
released under an [MIT license](https://opensource.org/licenses/MIT).
[Contributions](./CONTRIBUTING.rst) are welcome.
Please note that this project is released with a
[Contributor Code of Conduct](./CODE-OF-CONDUCT.rst).
By participating in this project you agree to abide by its terms.
