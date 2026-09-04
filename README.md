# Test speed net (download/upload)

<img align="right" src="https://raw.githubusercontent.com/vroncevic/testspeednet/refs/heads/master/docs/speedtest_logo.png" width="25%">

**testspeednet** is tool for test speed net (download/upload).

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![testspeednet python checker](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python_checker.yml/badge.svg)](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python_checker.yml) [![testspeednet package checker](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_package_checker.yml/badge.svg)](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_package.yml) [![testspeednet interface checker](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_interface_checker.yml/badge.svg)](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_interface_checker.yml) [![testspeednet isp checker](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_isp_checker.yml/badge.svg)](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_isp_checker.yml) [![testspeednet srp checker](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_srp_checker.yml/badge.svg)](https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_srp_checker.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/testspeednet.svg)](https://github.com/vroncevic/testspeednet/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/testspeednet.svg)](https://github.com/vroncevic/testspeednet/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
  - [✨ Features](#-features)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation

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

### 📦 Dependencies

**testspeednet** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/)

### 📁 Tool structure

**testspeednet** is based on OOP.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
    testspeednet/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── __init__.py
         │   │   ├── speed_test_result.py
         │   │   ├── speed_test_server.py
         │   │   └── speed_test_stat.py
         │   └── service/
         │       ├── engine.py
         │       ├── ijson_exporter.py
         │       ├── inetwork_speed_tester.py
         │       ├── __init__.py
         │       ├── iserver_repository.py
         │       ├── iservice.py
         │       └── isubprocessor.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── command.py
         │   │   ├── download_command_definition.py
         │   │   ├── download_command_executor.py
         │   │   ├── fetch_command_definition.py
         │   │   ├── fetch_command_executor.py
         │   │   ├── history_command_definition.py
         │   │   ├── history_command_executor.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── __init__.py
         │   │   ├── speed_command_definition.py
         │   │   ├── speed_command_executor.py
         │   │   ├── upload_command_definition.py
         │   │   └── upload_command_executor.py
         │   ├── config/
         │   │   ├── apis.yaml
         │   │   ├── testspeednet.cfg
         │   │   ├── testspeednet.logo
         │   │   └── testspeednet_util.cfg
         │   ├── database/
         │   │   ├── __init__.py
         │   │   └── server_repository.py
         │   ├── __init__.py
         │   ├── json_exporter.py
         │   ├── network_speed_tester.py
         │   └── subprocessor.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     11 directories, 62 files
```
</details>

#### ✨ Features

* Comprehensive network speed testing for download, upload, ping, and overall bandwidth.
* Provides a modular and extensible architecture based on OOP and SOLID principles.
* Includes command line interface (CLI) support via a command/executor structure.
* Robust validation of project bundles, dependencies, and options.
* Automatic persistence of measurement results and available test servers in local SQLite database.
* Optional JSON export capability for programmatic processing and reporting (`--json`).
* History inspection with configurable record limit (`--limit`).
* High code quality with full type checking and quality gates compliance.

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `testspeednet/__init__.py` | 9 | 0 | 100%|
| `testspeednet/core/__init__.py` | 9 | 0 | 100%|
| `testspeednet/core/model/__init__.py` | 9 | 0 | 100%|
| `testspeednet/core/model/speed_test_result.py` | 18 | 0 | 100%|
| `testspeednet/core/model/speed_test_server.py` | 24 | 0 | 100%|
| `testspeednet/core/model/speed_test_stat.py` | 20 | 0 | 100%|
| `testspeednet/core/service/__init__.py` | 9 | 0 | 100%|
| `testspeednet/core/service/engine.py` | 92 | 0 | 100%|
| `testspeednet/core/service/ijson_exporter.py` | 15 | 0 | 100%|
| `testspeednet/core/service/inetwork_speed_tester.py` | 18 | 0 | 100%|
| `testspeednet/core/service/iserver_repository.py` | 20 | 0 | 100%|
| `testspeednet/core/service/iservice.py` | 24 | 0 | 100%|
| `testspeednet/core/service/isubprocessor.py` | 14 | 0 | 100%|
| `testspeednet/engine.py` | 59 | 0 | 100%|
| `testspeednet/infrastructure/__init__.py` | 9 | 0 | 100%|
| `testspeednet/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `testspeednet/infrastructure/cli/engine.py` | 39 | 0 | 100%|
| `testspeednet/infrastructure/cli/icli.py` | 14 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/bundle.py` | 22 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/dep_validator.py` | 36 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/dependencies.py` | 18 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/factory.py` | 56 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/keys.py` | 26 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/opt_validator.py` | 36 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/options.py` | 15 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/registry.py` | 24 | 0 | 100%|
| `testspeednet/infrastructure/cli/setup/validator.py` | 43 | 0 | 100%|
| `testspeednet/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `testspeednet/infrastructure/command/command.py` | 16 | 0 | 100%|
| `testspeednet/infrastructure/command/download_command_definition.py` | 24 | 0 | 100%|
| `testspeednet/infrastructure/command/download_command_executor.py` | 34 | 0 | 100%|
| `testspeednet/infrastructure/command/fetch_command_definition.py` | 24 | 0 | 100%|
| `testspeednet/infrastructure/command/fetch_command_executor.py` | 31 | 0 | 100%|
| `testspeednet/infrastructure/command/history_command_definition.py` | 24 | 0 | 100%|
| `testspeednet/infrastructure/command/history_command_executor.py` | 36 | 0 | 100%|
| `testspeednet/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `testspeednet/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `testspeednet/infrastructure/command/speed_command_definition.py` | 24 | 0 | 100%|
| `testspeednet/infrastructure/command/speed_command_executor.py` | 33 | 0 | 100%|
| `testspeednet/infrastructure/command/upload_command_definition.py` | 24 | 0 | 100%|
| `testspeednet/infrastructure/command/upload_command_executor.py` | 34 | 0 | 100%|
| `testspeednet/infrastructure/database/__init__.py` | 9 | 0 | 100%|
| `testspeednet/infrastructure/database/server_repository.py` | 85 | 0 | 100%|
| `testspeednet/infrastructure/json_exporter.py` | 55 | 0 | 100%|
| `testspeednet/infrastructure/network_speed_tester.py` | 99 | 0 | 100%|
| `testspeednet/infrastructure/subprocessor.py` | 48 | 0 | 100%|
| `testspeednet/setup/__init__.py` | 9 | 0 | 100%|
| `testspeednet/setup/bundle.py` | 23 | 0 | 100%|
| `testspeednet/setup/dep_validator.py` | 36 | 0 | 100%|
| `testspeednet/setup/dependencies.py` | 19 | 0 | 100%|
| `testspeednet/setup/factory.py` | 55 | 0 | 100%|
| `testspeednet/setup/keys.py` | 27 | 0 | 100%|
| `testspeednet/setup/opt_validator.py` | 34 | 0 | 100%|
| `testspeednet/setup/options.py` | 12 | 0 | 100%|
| `testspeednet/setup/registry.py` | 32 | 0 | 100%|
| `testspeednet/setup/validator.py` | 48 | 0 | 100%|
| **Total** | 1628 | 0 | 100% |

</details>

### 🛠 Usage

Install package

```bash
pip3 install testspeednet
```

Prepare main entry point by downloading [main.py](https://raw.githubusercontent.com/vroncevic/testspeednet/main/main.py) or create your own.

```bash
wget -O main.py https://raw.githubusercontent.com/vroncevic/testspeednet/main/main.py
```

Running tool for checking network speed

```bash
python3 main.py speed
```

Running tool for fetching speed test servers

```bash
python3 main.py fetch
```

Running tool for viewing measurement history

```bash
python3 main.py history --limit 10
```

### 📚 Docs

[![Documentation Status](https://readthedocs.org/projects/testspeednet/badge/?version=latest)](https://testspeednet.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [testspeednet.readthedocs.io](https://testspeednet.readthedocs.io)
* [www.python.org](https://www.python.org/)

### 👥 Contributing

[Contributing to testspeednet](CONTRIBUTING.md)

### 📄 Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2016 - 2026 by [vroncevic.github.io/testspeednet](https://vroncevic.github.io/testspeednet)

**testspeednet** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/testspeednet/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
