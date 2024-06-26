Test speed net (download/upload)
---------------------------------

**testspeednet** is tool for test speed net (download/upload).

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|testspeednet python checker| |testspeednet python package| |github issues| |documentation status| |github contributors|

.. |testspeednet python checker| image:: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_python_checker.yml

.. |testspeednet python package| image:: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/testspeednet/actions/workflows/testspeednet_package.yml

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

Installation
-------------

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

Dependencies
-------------

**testspeednet** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_

Tool structure
---------------

**testspeednet** is based on OOP.

Tool structure

.. code-block:: bash

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

Copyright and licence
-----------------------

|license: gpl v3| |license: apache 2.0|

.. |license: gpl v3| image:: https://img.shields.io/badge/license-gplv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |license: apache 2.0| image:: https://img.shields.io/badge/license-apache%202.0-blue.svg
   :target: https://opensource.org/licenses/apache-2.0

Copyright (C) 2021 - 2024 by `vroncevic.github.io/testspeednet <https://vroncevic.github.io/testspeednet>`_

**testspeednet** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

|python software foundation|

.. |python software foundation| image:: https://raw.githubusercontent.com/vroncevic/testspeednet/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_us/i/btn/btn_donatecc_lg.gif
   :target: https://www.python.org/psf/donations/

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`