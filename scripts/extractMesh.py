#!/usr/bin/env python

import argparse

from ClutterBaseCore import Connection


def extract_mesh(database,name,out) :
    with Connection.ClutterBaseConnection(database) as connection :
        connection.extract_mesh(name,out)


if __name__=="__main__" :
    parser = argparse.ArgumentParser(description='extract mesh to clutterbase')
    parser.add_argument('--name', '-n' ,help='Name for query',required=True)
    parser.add_argument('--database', '-db' ,help='The database to add to',required=True)
    parser.add_argument('--out', '-o' ,help='output filename',required=True)
    args = parser.parse_args()


    extract_mesh(args.database,args.name,args.out)