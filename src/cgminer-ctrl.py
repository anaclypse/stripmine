#!/usr/bin/python

import socket
import json
import jsontools
import sys
import argparse

default_api_ip = '127.0.0.1'
default_api_port = 4028

def get_response(sckt):
    buff = sckt.recv(4096)
    done = False
    while not done:
        more = sckt.recv(4096)
        if not more:
            done = True
        else:
            buff = buff+more
    if buff:
        return buff


def cgminer_comm(in_command, api_ip = default_api_ip, api_port = default_api_port):

    api_command = in_command.split('|')

    sckt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sckt.connect((api_ip,int(api_port)))

    if len(api_command) == 2:
        sckt.send(json.dumps({"command":api_command[0],"parameter":api_command[1]}))
    else:
        sckt.send(json.dumps({"command":api_command[0]}))

    raw_response = get_response(sckt)
    sckt.close()

    response = raw_response.replace('\x00','')
    response = json.loads(response)
    return response


def get_api():
    print "oops"


def main(argv):
    parser = argparse.ArgumentParser(description="cgminer control and query tool")
                       
    parser.add_argument('--ip', action='store', metavar="IP", default=None,
                        help='specify ip[:port] that cgminer is listening on')

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-l', '--list-avail', dest='listcmd', action='store_true', default=False,
                        help='list available cgminer commands')

    group.add_argument('-c', '--command', action='store', default=None, 
                       help="string formatted cgminer api command, e.g. gpufan|0,80")

    parser.add_argument('-q', '--query', dest='queries', action='append', metavar="LIST", default=[],
                        help='query the given command with list or nested list of keys')

    args = parser.parse_args()

    if args.command:
        comm_ip = default_api_ip
        comm_port = default_api_port
        if args.ip:
            ip_port = args.ip.split(":")
            if len(ip_port) == 1:
                comm_ip = ip_port[0]
            elif len(ip_port) == 2:
                comm_ip = ip_port[0]
                comm_port = ip_port[1]
            else:
                print "Malformed ip:port argument %s" % args.ip
                sys.exit(1)

        resp = cgminer_comm(args.command, comm_ip, comm_port)
        print jsontools.walk_string(resp)
        #print "Q: ", args.queries
        for query in args.queries:
            print "Query: ", query.split(":")
            print "Response: ", jsontools.walk_find(resp, query.split(":"))

    elif args.queries:
        print "Cannot specify query without command"
        sys.exit(1)

    elif args.listcmd:
        print "List of available commands:"

if __name__ == "__main__":
    main(sys.argv)

