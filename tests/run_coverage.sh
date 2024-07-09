#!/bin/bash
#
# @brief   testspeednet
# @version v1.0.2
# @date    Sat Aug 11 09:58:41 2022
# @company None, free software to use 2022
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

rm -rf htmlcov testspeednet_coverage.xml testspeednet_coverage.json .coverage
ats_coverage_run.py -n testspeednet -p ../README.md
python3 -m coverage run -m --source=../testspeednet unittest discover -s ./ -p '*_test.py' -vvv
python3 -m coverage html -d htmlcov
python3 -m coverage xml -o testspeednet_coverage.xml 
python3 -m coverage json -o testspeednet_coverage.json
python3 -m coverage report --format=markdown -m
