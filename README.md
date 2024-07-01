# Test speed net (download/upload)

<img align="right" src="https://github.com/vroncevic/testspeednet/blob/master/docs/speedtest_logo.png" width="25%">

**testspeednet** is tool for test speed net (download/upload).

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![testspeednet python checker](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python_checker.yml/badge.svg)](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python_checker.yml) [![testspeednet package checker](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_package_checker.yml/badge.svg)](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_package.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/testspeednet.svg)](https://github.com/vroncevic/testspeednet/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/testspeednet.svg)](https://github.com/vroncevic/testspeednet/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Installation](#installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [Dependencies](#dependencies)
- [Tool structure](#tool-structure)
- [Docs](#docs)
- [Contributing](#contributing)
- [Copyright and licence](#copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/testspeednet/dev/docs/debtux.png)

[![testspeednet python3 build](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python3_build.yml/badge.svg)](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**testspeednet** is located at **[pypi.org](https://pypi.org/project/testspeednet/)**.

You can install by using pip

```bash
# python3
pip3 install testspeednet
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/testspeednet/releases/)** download and extract release archive.

To install **testspeednet** type the following

```bash
tar xvzf testspeednet-x.y.z.tar.gz
cd testspeednet-x.y.z/
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install ./dist/testspeednet-*-py3-none-any.whl
rm -f get-pip.py
chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/testspeednet_run.py
ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/testspeednet_run.py /usr/local/bin/testspeednet_run.py
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/testspeednet/releases)** download and extract release archive.

To install **testspeednet** locate and run setup.py with arguments

```bash
tar xvzf testspeednet-x.y.z.tar.gz
cd testspeednet-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### Dependencies

**testspeednet** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/)

### Tool structure

**testspeednet** is based on OOP

Tool structure

```bash
    testspeednet/
          ├── conf/
          │   ├── apis.yaml
          │   ├── testspeednet.cfg
          │   ├── testspeednet.logo
          │   └── testspeednet_util.cfg
          ├── __init__.py
          ├── log/
          │   └── testspeednet.log
          ├── net/
          │   ├── config.py
          │   ├── download.py
          │   ├── __init__.py
          │   ├── model.py
          │   ├── speed.py
          │   ├── test.py
          │   ├── upload.py
          │   └── utils/
          │       ├── catch_request.py
          │       ├── checking_servers.py
          │       ├── connector.py
          │       ├── distance.py
          │       ├── do_nothing_factory.py
          │       ├── fake_shutdown_event.py
          │       ├── get_exception_factory.py
          │       ├── get_response_stream_factory.py
          │       ├── gzip_decoded_response.py
          │       ├── http_downloader.py
          │       ├── http_uploader_data.py
          │       ├── http_uploader.py
          │       ├── __init__.py
          │       ├── net_exceptions.py
          │       ├── opener.py
          │       ├── printer_factory.py
          │       ├── requester.py
          │       ├── test_http_connection.py
          │       ├── test_http_handler.py
          │       ├── test_https_connection.py
          │       ├── test_https_handler.py
          │       ├── test_net_config.py
          │       ├── test_results.py
          │       └── user_agent.py
          ├── py.typed
          └── run/
              └── testspeednet_run.py
    
    6 directories, 39 files
```

### Docs

[![Documentation Status](https://readthedocs.org/projects/testspeednet/badge/?version=latest)](https://testspeednet.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [testspeednet.readthedocs.io](https://testspeednet.readthedocs.io)
* [www.python.org](https://www.python.org/)

### Contributing

[Contributing to testspeednet](CONTRIBUTING.md)

### Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2016 - 2024 by [vroncevic.github.io/testspeednet](https://vroncevic.github.io/testspeednet)

**testspeednet** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/testspeednet/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
