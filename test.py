#!/usr/bin/python3
##coding=utf-8
# ------------------------------------------------------
#
# Zimbra Exporter
#
# Script by : Jason Cheng
# Website : www.jason.tools / blog.jason.tools
# Version : 1.0
# Date : 2021/11/28
#
# ------------------------------------------------------

import requests
import prometheus_client
import os
import psutil
import time
import datetime
import configparser
from prometheus_client.core import CollectorRegistry
from prometheus_client import Gauge
from prometheus_client import Counter
from flask import Response,Flask

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('/usr/local/bin/zimbra_exporter_config.ini')

# ------
# define
# ------

PORT_EXPORTER = config.get('Settings', 'PORT_EXPORTER')
MAILSERVER = config.get('Settings', 'MAILSERVER')
EXCLUDE_DOMAIN = config.get('Settings', 'EXCLUDE_DOMAIN')
PORT_SMTP = config.get('Settings', 'PORT_SMTP')
PORT_IMAP = config.get('Settings', 'PORT_IMAP')
PORT_IMAPS = config.get('Settings', 'PORT_IMAPS')
PORT_POP3 = config.get('Settings', 'PORT_POP3')
PORT_POP3S = config.get('Settings', 'PORT_POP3S')
PORT_WEBCLIENT = config.get('Settings', 'PORT_WEBCLIENT')

# ------



# get top usage

if (EXCLUDE_DOMAIN ==''):
      get_qu_cmd = '/bin/su - zimbra -c "zmprov getQuotaUsage ' + MAILSERVER + '| grep -v \"spam.\" | grep -v \"virus-quarantine.\" | head -n 6"'
    else:
      get_qu_cmd = '/bin/su - zimbra -c "zmprov getQuotaUsage ' + MAILSERVER + '| grep -v \"' + EXCLUDE_DOMAIN + '\" | grep -v \"spam.\" | grep -v \"virus-quarantine.\" | head -n 6"'

    get_qu = os.popen(get_qu_cmd).read().splitlines()
    qu = Gauge("zimbra_quota_usage","Zimbra User Quota Usage:",["name","usage"],registry=REGISTRY)
    for i in range(len(get_qu)):

      qu_name = get_qu[i].split(' ')[0].strip()
      qu_usage = int(get_qu[i].split(' ')[2].strip())
      qu_quota = int(get_qu[i].split(' ')[1].strip())
      qu_value = 0
      if (qu_quota != 0 and qu_usage != 0):
        qu_value = qu_usage / qu_quota

      qu.labels(qu_name,qu_usage).set(qu_value)


    # -----
~                                                                   