#!/usr/bin/env python

import argparse

from ClutterBaseCore import Connection


def add_mesh(database:str,name : str ,description : str,mesh : str,top :str,front : str,side : str,persp : str) :
    with Connection.ClutterBaseConnection(database) as connection :
            connection.add_item(name,description,mesh,top,persp,side,front)

if __name__=="__main__" :
    parser = argparse.ArgumentParser(description='Add mesh to clutterbase')
    parser.add_argument('--mesh', '-m' ,help='The mesh to add',required=True)
    parser.add_argument('--name', '-n' ,help='Name for query',required=True)
    parser.add_argument('--description', '-d' ,help='Description',required=True)
    parser.add_argument('--database', '-db' ,help='The database to add to',required=True)
    parser.add_argument('--top', '-t' ,help='top image',required=True)
    parser.add_argument('--front', '-f' ,help='front image',required=True)
    parser.add_argument('--side', '-s' ,help='side image',required=True)
    parser.add_argument('--persp', '-p' ,help='persp image',required=True)
    
    args = parser.parse_args()

    add_mesh(args.database,args.name,args.description,args.mesh,args.top,args.front,args.side,args.persp)