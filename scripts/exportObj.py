# Get the selected Objects
parts=cmds.ls(sl=True)
# create a group
cmds.group(empty=True,world=True,name="exportGRP")
# duplicate
for p in parts :
    cmds.duplicate(p,name=f"{p}_tmp")
    cmds.parent(f"{p}_tmp","exportGRP") 

# Move to origin
cmds.select("exportGRP")
cmds.CenterPivot()
cmds.move(0,0,0,"exportGRP",rotatePivotRelative=True)

# export
filePath = cmds.fileDialog2(fileFilter="*.obj",dialogStyle=2,fileMode=0,caption='Export As')

if len(filePath) !=0 :
    cmds.file(filePath[0],pr=1,typ="OBJexport",exportSelected=1,op="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1" )

#clean up
cmds.delete("exportGRP")
