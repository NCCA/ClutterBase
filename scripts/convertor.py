#!/usr/bin/env mayapy # note I have this as an alias

import argparse
import os
import sys

import maya.standalone

formats=["obj","ma","mb","fbx","usda","usdb","usd"]

def export(input,output,dir) :
    maya.standalone.initialize(name='python')
    # note this has to happen after the init
    import maya.cmds as cmds
    cmds.loadPlugin("objExport")
    cmds.loadPlugin("mayaUsdPlugin")
    cmds.loadPlugin("fbxmaya")
    original_dir=os.getcwd()
    os.chdir(dir)
    working_dir=os.getcwd()
    files=os.listdir(".")
    for file in files :
        if file.endswith(input) :
            cmds.file(f=True,new=True)
            cmds.file(f"{working_dir}/{file}",i=True)
            cmds.select(all=True)
            out_file=file[0:file.find(input)-1]
            if output == "fbx" :
                cmds.file(f"{working_dir}/{out_file}",options="v=0;",type="FBX export" ,pr=True ,es=True)
            elif output == "usd" :
                cmds.file(f"{working_dir}/{out_file}",options=";exportUVs=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;",type="USD Export" ,pr=True ,es=True)


    # change back to working dir
    os.chdir(original_dir)
    return
    # files = os.listdir(".")
    # for mayafile in files :
    # if mayafile.endswith(".ma") :
    #     cmds.file(mayafile,o=True)
    #     cmds.select(all=True)
    #     newFile="%s.obj" %(mayafile)
    #     cmds.file(newFile,type="OBJexport",pr=True,es=True)


    # cmds.file("/Users/jmacey/Downloads/test.fbx",options="v=0;",type="FBX export" ,pr=True ,es=True,f=True)


if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='Batch Convert files valid formats are "obj","ma","mb","usd","usda","usdb","fbx"')
    parser.add_argument('--input', '-i' ,help='input format',required=True)
    parser.add_argument('--output', '-o' ,help='output format',required=True)
    parser.add_argument('dir', nargs='?', default=os.getcwd())

    args = parser.parse_args()
    if args.input not in formats :
        print("error unsuported input format")
        sys.exit()
    if args.output not in formats :
        print("error unsupported output format") 
        sys.exit()
    if args.input == args.output :
        print("input and output formats must be different")
        sys.exit()
    export(args.input,args.output,args.dir)