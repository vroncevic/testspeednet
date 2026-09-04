#!/bin/bash
#
# @brief   testspeednet
# @version 2.0.0
# @date    Fri Sep 04 19:07:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 coverage/ats_coverage.py testspeednet
pylint testspeednet > testspeednet.report
echo "Done"
