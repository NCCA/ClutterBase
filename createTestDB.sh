#!/usr/bin/env bash

sql="DROP TABLE IF EXISTS ClutterBase;
CREATE TABLE ClutterBase (
                id integer PRIMARY KEY AUTOINCREMENT,
                Name text NOT NULL,
                Description text Not Null,
                MeshData BLOB Not Null,
                TopImage BLOB NOT NULL,
                PerspImage BLOB NOT NULL,
                SideImage BLOB NOT NULL,
                FrontImage BLOB NOT NULL,
                FileType TEXT CHECK( FileType IN ('obj','usd','fbx') )   NOT NULL DEFAULT 'obj'
                );"

echo $sql | sqlite3 ClutterTest.db

./scripts/addToDatabase.py -m testdata/Jug/Jug.usd -n "A Jug" -d "this is a longer description" -db ClutterTest.db -t testdata/Jug/JugTop.png -s testdata/Jug/JugSide.png -p testdata/Jug/JugPersp.png -f testdata/Jug/JugFront.png


./scripts/addToDatabase.py -m testdata/Bottle/bottle.fbx -n "Simple Bottle" -d "FBX Bottle" -db ClutterTest.db -t testdata/Bottle/BottleTop.png -s testdata/Bottle/BottleSide.png -p testdata/Bottle/BottlePersp.png -f testdata/Bottle/BottleFront.png


./scripts/addToDatabase.py -m testdata/Whisk/whisk.obj -n "A Whisk" -d "A whist to test Obj import" -db ClutterTest.db -t testdata/Whisk/WhiskTop.png -s testdata/Whisk/WhiskSide.png -p testdata/Whisk/WhiskPersp.png -f testdata/Whisk/WhiskFront.png

./scripts/addToDatabase.py -m testdata/Loaf/loaf.obj -n "A Loaf" -d "Not sure what type of bread this is" -db ClutterTest.db -t testdata/Loaf/LoafTop.png -s testdata/Loaf/LoafSide.png -p testdata/Loaf/LoafPersp.png -f testdata/Loaf/LoafFront.png

./scripts/addToDatabase.py -m testdata/Mug/Mug1.fbx -n "Mug" -d "A generic mug" -db ClutterTest.db -t testdata/Mug/MugTop.png -s testdata/Mug/MugSide.png -p testdata/Mug/MugPersp.png -f testdata/Mug/MugFront.png

./scripts/addToDatabase.py -m testdata/PanStack/panstack.usd -n "PanStack" -d "A stack of saucepans" -db ClutterTest.db -t testdata/PanStack/PansTop.png -s testdata/PanStack/PansSide.png -p testdata/PanStack/PansPersp.png -f testdata/PanStack/PansFront.png

./scripts/addToDatabase.py -m testdata/Pin/pin.obj -n "Rolling Pin" -d "A rolling Pin" -db ClutterTest.db -t testdata/Pin/PinTop.png -s testdata/Pin/PinSide.png -p testdata/Pin/PinPersp.png -f testdata/Pin/PinFront.png

./scripts/addToDatabase.py -m testdata/Spatula/spatula.fbx -n "Spatula" -d "A spatula" -db ClutterTest.db -t testdata/Spatula/SpatulaTop.png -s testdata/Spatula/SpatulaSide.png -p testdata/Spatula/SpatulaPersp.png -f testdata/Spatula/SpatulaFront.png

./scripts/addToDatabase.py -m testdata/Spoon/spoon.obj -n "Spoon" -d "A spoon" -db ClutterTest.db -t testdata/Spoon/SpoonTop.png -s testdata/Spoon/SpoonSide.png -p testdata/Spoon/SpoonPersp.png -f testdata/Spoon/SpoonFront.png


./scripts/addToDatabase.py -m testdata/Stool/Stool.usd -n "Wooden Stool" -d "A simple wooden stool" -db ClutterTest.db -t testdata/Stool/StoolTop.png -s testdata/Stool/StoolSide.png -p testdata/Stool/StoolPersp.png -f testdata/Stool/StoolFront.png

./scripts/addToDatabase.py -m testdata/Stool/stoolBig.fbx -n "A metal Stool" -d "A nice metal stool with twisted legs" -db ClutterTest.db -t testdata/Stool/StoolBigTop.png -s testdata/Stool/StoolBigSide.png -p testdata/Stool/StoolBigPersp.png -f testdata/Stool/StoolBigFront.png

./scripts/addToDatabase.py -m testdata/Teapot/teapot.obj -n "A stove top kettle" -d "A stove top kettle or teapot" -db ClutterTest.db -t testdata/Teapot/TeapotTop.png -s testdata/Teapot/TeapotSide.png -p testdata/Teapot/TeapotPersp.png -f testdata/Teapot/TeapotFront.png

