#!/usr/bin/env python

# Test whether a connection is denied if it provides just a username when it
# needs a username and password.

import subprocess
import socket
import time

import inspect, os, sys
# From http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import mosq_test

rc = 1
keepalive = 10
connect_packet = mosq_test.gen_connect("connect-uname-test", keepalive=keepalive, username="user")
connack_packet = mosq_test.gen_connack(rc=4)

broker = subprocess.Popen(['../../src/mosquitto', '-c', '01-connect-uname-no-password-denied.conf'], stderr=subprocess.PIPE)

try:
    time.sleep(0.5)

    sock = mosq_test.do_client_connect(connect_packet, connack_packet)
    sock.close()
    rc = 0
finally:
    broker.terminate()
    broker.wait()
    if rc:
        (stdo, stde) = broker.communicate()
        print(stde)

exit(rc)

