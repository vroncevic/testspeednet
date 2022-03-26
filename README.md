<img align="right" src="https://raw.githubusercontent.com/vroncevic/speedtest/dev/docs/speedtest_logo.png" width="25%">

# Generate Memory Map Modules

**speedtest** is tool for generation of memory map modules.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

![Python package](https://github.com/vroncevic/speedtest/workflows/Python%20package%20speedtest/badge.svg?branch=master) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/speedtest.svg)](https://github.com/vroncevic/speedtest/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/speedtest.svg)](https://github.com/vroncevic/speedtest/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents**

- [Installation](#installation)
  - [Install using pip](#install-using-pip)
  - [Install using setuptools](#install-using-setuptools)
  - [Install using docker](#install-using-docker)
- [Dependencies](#dependencies)
- [Generation flow of py module](#generation-flow-of-py-module)
- [Tool structure](#tool-structure)
- [Docs](#docs)
- [Copyright and Licence](#copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Installation

![Install Python2 Package](https://github.com/vroncevic/speedtest/workflows/Install%20Python2%20Package%20speedtest/badge.svg?branch=master) ![Install Python3 Package](https://github.com/vroncevic/speedtest/workflows/Install%20Python3%20Package%20speedtest/badge.svg?branch=master)

Currently there are three ways to install tool

- Install process based on pip
- Install process based on setup.py (setuptools)
- Install process based on docker mechanism

##### Install using pip

Python package is located at **[pypi.org](https://pypi.org/project/speedtest/)**.

You can install by using pip

```bash
# python2
pip install speedtest
# python3
pip3 install speedtest
```

##### Install using setuptools

Navigate to release **[page](https://github.com/vroncevic/speedtest/releases/)** download and extract release archive.

To install modules, locate and run setup.py with arguments

```bash
tar xvzf speedtest-x.y.z.tar.gz
cd speedtest-x.y.z/
# python2
pip install -r requirements.txt
python setup.py install_lib
python setup.py install_data
python setup.py install_egg_info
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_data
python3 setup.py install_egg_info
```

##### Install using docker

You can use docker to create image/container.

[![speedtest docker checker](https://github.com/vroncevic/speedtest/workflows/speedtest%20docker%20checker/badge.svg)](https://github.com/vroncevic/speedtest/actions?query=workflow%3A%22speedtest+docker+checker%22)

### Dependencies

**speedtest** requires next modules and libraries

- [ats-utilities - Python App/Tool/Script Utilities](https://vroncevic.github.io/ats_utilities)

### Generation flow of py module

Base flow of generation process

![Tool flow](https://raw.githubusercontent.com/vroncevic/speedtest/dev/docs/speedtest_flow.png)

### Tool structure

**speedtest** is based on OOP

Generator structure

```bash

```

### Docs

[![Documentation Status](https://readthedocs.org/projects/speedtest/badge/?version=latest)](https://speedtest.readthedocs.io/projects/speedtest/en/latest/?badge=latest)

More documentation and info at

- [speedtest.readthedocs.io](https://speedtest.readthedocs.io/en/latest/)
- [www.python.org](https://www.python.org/)

### Copyright and Licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2016 by [vroncevic.github.io/speedtest](https://vroncevic.github.io/speedtest)

**speedtest** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 2.x/3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/speedtest/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://psfmember.org/index.php?q=civicrm/contribute/transact&reset=1&id=2)
