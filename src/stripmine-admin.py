#!/usr/bin/python

import socket
import sys
import argparse
from stripmine import gen_local_config
from stripmine import read_local_config

def get_args(argv):
    parser = argparse.ArgumentParser(description="stripmine daemon control program")

    parser.add_argument('--config-path', dest='confpath', metavar='PATH', 
                        action='store', default=None, 
                        help='stripmine config file path')

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--gen-config', dest='genconf', 
                       action='store_true', default=False, 
                       help='generate default configuration file for stripmine')

    group.add_argument('--command-list', dest='cmdlist', 
                       action='store_true', default=False, 
                       help='print command options')

    group.add_argument('-c', dest='cmnds', metavar='CMD', 
                       nargs="+", action='append', default=[],
                       help='use --command-list for list of options, use -c COMMAND help for help with specific command')
                        
    return parser.parse_args(argv)

def main(argv):
    args = get_args(argv)

    if args.genconf:
        if args.confpath:
            gen_local_config(args.confpath)
        else:
            gen_local_config()

    if args.confpath:
        config = read_local_config(args.confpath)
    else:
        config = read_local_config()
        
    #print config

    for cmd in args.cmnds:
        msg = " ".join(cmd) 

        host = config['host']
        port = config['port']
        print host, ":", port, ": ", msg

        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect((host, port))
        skt.send(msg)
        data = skt.recv(1024)
        skt.close()
        print 'Received', repr(data)

if __name__ == "__main__":
    main(sys.argv[1:])
