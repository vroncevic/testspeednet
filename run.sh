#!/bin/bash
#
# @brief   testspeednet
# @version 2.0.0
# @date    Fri Sep 04 19:07:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 main.py fetch
python3 main.py speed --json speed_result.json
python3 main.py download --json download_result.json
python3 main.py upload --json upload_result.json
python3 main.py history --limit 5 --json history_result.json
