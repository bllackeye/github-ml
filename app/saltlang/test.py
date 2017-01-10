import sys
import logging
import datetime
import subprocess
import time
import json
from subprocess import Popen

logger = logging.getLogger(__name__)


def write(param1, param2, param3):
    print(param1)
    print(param2)
    print(param3)
    return "params:%s,%s,%s" % (param1,param2,param3)
