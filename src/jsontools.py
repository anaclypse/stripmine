#!/usr/bin/python

import json
import sys

def is_dict(node):
    try:
        for key,item in node.items():
            return True
    except:
        return False

def is_composite(item):
    if isinstance(item, basestring):
        return False
    try:
        for x in item:
            return True
    except:
        return False

def get_first_rest(item):
    #print "GFR: ", item

    if isinstance(item, basestring):
        return (None, None)

    rest = []
    try:
        for (idx, x) in enumerate(item):
            if idx > 0:
                rest.append(x)
            else:
                first = x
                #print "GFR First:", first
    except:
        first = None
        
    if len(rest) == 0:
        rest = None

    return (first, rest)



def walk_string(node, depth=0):
    inden = "  " * depth# + ":" + str(depth)
    atoms = ""
    subitems = ""
    if is_dict(node):
        for key, item in node.items():
            if is_composite(item):
                subitems += inden + ":>: " + str(key) + "\n"
                subitems += walk_string(item, depth+1)

            else:
                atoms += inden + ":-: " + str(key) + ":" + str(item) + "\n"

    elif is_composite(node):
        for item in node:
            subitems += walk_string(item, depth+1)

    else:
        atoms += ":?:" + repr(node)

    return atoms + subitems



def walk_find(node, query, depth=0):

    first,rest = get_first_rest(query)
    if not first:
        return "Malformed query %s" % repr(query)

    #print "Q:", depth,": ", first, ", ", rest

    if is_dict(node):
        try:
            item = node[first]
        except:
            return None

        if is_composite(item):
            if not rest:
                return item
            else:
                return walk_find(item, rest, depth+1)
        else:
            if rest:
                return str(item) + ":-" + repr(rest)
            return item

    elif is_composite(node):
        for item in node:
            result = walk_find(item, query, depth+1)
            if result:
                return result
        return None
    
    return str(node) + ":-" + repr(query)




