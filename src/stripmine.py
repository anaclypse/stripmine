#!/usr/bin/python
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import logging
import time
import socket
import sys
import json
import threading

#third party libs
from daemon import runner

#local libs
import config as conf

#static logging values
LogLevel = logging.INFO
LogFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LoggerName = "StripMineLog"

def gen_local_config(fname=conf.values.local_config):
    config={}
    config['host'] = 'localhost'
    config['port'] = 8945
    config['pidfile'] = conf.values.install_path + '/stripmine.pid'
    config['logfile'] = conf.values.install_path + '/stripmine.log'
    config['cgminers'] = {}
    config['cgminers']['0'] = {}
    config['cgminers']['0']['ip'] = '127.0.0.1'
    config['cgminers']['0']['port'] = 4028


    try:
        json.dump(config, open(fname, 'w'), indent=0)
    except:
        print "Error writing json to file: ", fname
        sys.exit(1)

def read_local_config(fname=conf.values.local_config):
    try:
        config = json.load(open(fname, 'r'))
    except:
        print "Error reading json from file: ", fname
        sys.exit(1)

    return config


class MainLoop():
   
    def __init__(self, logger, config, testmode=False):
        self.logger = logger
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = config['pidfile']
        self.pidfile_timeout = 5

        self.testmode = testmode
        self.config=config
        self.loglock = threading.Lock()
        self.done = False

    def safelog_info(self, *args):
        with self.loglock:
            self.logger.info(*args)

    def cgminer_send(self, data):
        self.safelog_info("cgminer: %s", repr(data))
        

    def heartbeat(self):
        while not self.done:
            time.sleep(5)
            localtime = time.asctime( time.localtime(time.time()) )
            self.safelog_info("Hello: %s", str(localtime))

        self.safelog_info("Heartbeat shutting down")

    def run(self):
        hb = threading.Thread(target=start_heartbeat, args=[self])
        hb.setDaemon(True)
        hb.start()

	sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = self.config['host']
        port = self.config['port']
        sckt.bind((host, port))
        sckt.listen(5)
	
	while not self.done:
	    (connection, address) = sckt.accept()
	    self.safelog_info("Connected by %s", repr(address))
            msg = ""
            while True:
                data = connection.recv(1024)
                if not data: break
                self.safelog_info("Recv data %s", repr(data))
                msg += data
                connection.send("recv %d" % len(data))

            connection.close()
            tokv = msg.split()

            if len(tokv) == 0:
                self.safelog_info("Bad message format: %s", msg)

            elif (tokv[0] == "cgminer"):
                self.cgminer_send(tokv[1:])

            elif (tokv[0] == "quit"):
                if self.testmode: self.done=True

        sckt.close()
        self.done = True
        self.safelog_info("Socket listener shutting down")


def start_heartbeat(mainloop):
    mainloop.heartbeat()

def logger_setup(config):
    #see top of file for Log config values
    logger = logging.getLogger(LoggerName)
    logger.setLevel(LogLevel)
    formatter = logging.Formatter(LogFormat)
    handler = logging.FileHandler(config['logfile'])
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return handler, logger

def main():
    config = read_local_config()
    handler, logger = logger_setup(config)
    mainloop = MainLoop(logger, config)
    daemon_runner = runner.DaemonRunner(mainloop)
    context = daemon_runner.daemon_context
    #ensures that the logger file handle does not get closed during daemonization
    context.files_preserve=[handler.stream]
    daemon_runner.do_action()

def main_test(argv):
    config = read_local_config()
    handler, logger = logger_setup(config)
    mainloop = MainLoop(logger, config, testmode=True)
    mainloop.run()

def print_usage():
    print "Usage: %s --test|start|stop|restart" % sys.argv[0]
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
    if sys.argv[1] == "--test":
        main_test(sys.argv[2:])
        sys.exit(0)
    if (sys.argv[1] != "start") and (sys.argv[1] != "stop") and (sys.argv[1] != "restart"):
        print_usage()

    main()
