Test speed net (download/upload)
---------------------------------

**testspeednet** is tool for test speed net (download/upload).

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|testspeednet python checker| |testspeednet python package| |testspeednet interface checker| |testspeednet isp checker| |testspeednet srp checker| |github issues| |documentation status| |github contributors|

.. |testspeednet python checker| image:: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python_checker.yml

.. |testspeednet python package| image:: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_package.yml

.. |testspeednet interface checker| image:: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_interface_checker.yml

.. |testspeednet isp checker| image:: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_isp_checker.yml

.. |testspeednet srp checker| image:: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_srp_checker.yml

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/testspeednet.svg
   :target: https://github.com/vroncevic/testspeednet/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/testspeednet.svg
   :target: https://github.com/vroncevic/testspeednet/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/testspeednet/badge/?version=latest
   :target: https://testspeednet.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
-----------------

|testspeednet python3 build|

.. |testspeednet python3 build| image:: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/testspeednet/releases

To install **testspeednet** type the following

.. code-block:: bash

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

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # pyton3
    pip3 install testspeednet

📦 Dependencies
---------------

**testspeednet** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_

📁 Tool structure
-----------------

**testspeednet** is based on OOP.

Tool structure

.. code-block:: bash

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

✨ Features
-----------

* Comprehensive network speed testing for download, upload, ping, and overall bandwidth.
* Provides a modular and extensible architecture based on OOP and SOLID principles.
* Multi-command CLI interface supporting speed, download, upload, fetch, and history.
* Automatic persistence of measurement results and available test servers in local SQLite database.
* Optional JSON export capability for programmatic processing and reporting (--json).
* History inspection with configurable record limit (--limit).
* High code quality with full type checking and quality gates compliance.

📊 Code coverage
----------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------

Install package

.. code-block:: bash

    pip3 install testspeednet

Prepare main entry point by downloading `main.py` or create your own.

.. code-block:: bash

    wget -O main.py https://raw.githubusercontent.com/vroncevic/testspeednet/main/main.py

Running tool for checking network speed

.. code-block:: bash

    python3 main.py speed

Running tool for fetching servers

.. code-block:: bash

    python3 main.py fetch

Running tool for viewing history

.. code-block:: bash

    python3 main.py history --limit 10

📚 Docs
-------

More documentation and info at

* `testspeednet.readthedocs.io <https://testspeednet.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

👥 Contributing
---------------

`Contributing to testspeednet <https://github.com/vroncevic/testspeednet/blob/dev/CONTRIBUTING.md>`_

📄 Copyright and licence
-------------------------

Copyright (C) 2016 - 2026 by `vroncevic.github.io/testspeednet <https://vroncevic.github.io/testspeednet>`_

**testspeednet** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.
