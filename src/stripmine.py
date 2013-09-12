#!/usr/bin/python
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import logging
import time
import socket
import sys
#import signal

#third party libs
from daemon import runner

#PidFile = "/var/run/stripmine/stripmine.pid"
PidFile = "/home/pi/src/stripmine/stripmine.pid"

#LogFile = "/var/log/stripmine/stripmine.log"
LogFile = "/home/pi/src/stripmine/stripmine-test.log"
LogLevel = logging.INFO
LogFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LoggerName = "StripMineLog"

#def program_cleanup(*arg):
#    print "Cleanup was called with", len(arg), "arguments:", arg

#def reload_program_config(*arg):
#    print "Reload was called with", len(arg), "arguments:", arg


class MainLoop():
   
    def __init__(self, logger):
        self.logger = logger
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = PidFile
        self.pidfile_timeout = 5

    def cgminer_send(self, data):
        self.logger.info("cgminer: %s", repr(data))
        
    def run(self):
	sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.bind(('localhost', 8945))
        sckt.listen(5)
	
	while True:
	    (connection, address) = sckt.accept()
	    self.logger.info("Connected by %s", repr(address))
            msg = ""
            while True:
                data = connection.recv(1024)
                if not data: break
                self.logger.info("Recv data %s", repr(data))
                msg += data
                connection.send("recv %d" % len(data))

            connection.close()
            tokv = msg.split()

            if len(tokv) == 0:
                self.logger.info("Bad message format: %s", msg)

            elif (tokv[0] == "cgminer"):
                self.cgminer_send(tokv[1:])

        sckt.close()


def logger_setup():
    #see top of file for Log config values
    logger = logging.getLogger(LoggerName)
    logger.setLevel(LogLevel)
    formatter = logging.Formatter(LogFormat)
    handler = logging.FileHandler(LogFile)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def main():
    mainloop = MainLoop(logger_setup())
    daemon_runner = runner.DaemonRunner(mainloop)
    context = daemon_runner.daemon_context
    #ensures that the logger file handle does not get closed during daemonization
    context.files_preserve=[handler.stream]

## Does not work -> error closing socket connection
#    context.signal_map = {
#        signal.SIGTERM: program_cleanup,
#        signal.SIGHUP: 'terminate',
#        signal.SIGUSR1: reload_program_config,
#        }
    daemon_runner.do_action()

def main_test(argv):
    mainloop = MainLoop(logger_setup())
    mainloop.run()

def print_usage():
    print "Usage: %s start|stop|restart|test" % sys.argv[0]
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
