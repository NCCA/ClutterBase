CREATE TABLE IF NOT EXISTS ClutterBase (
    id integer PRIMARY KEY AUTOINCREMENT,
    Name text NOT NULL,
    Description text Not Null,
    MeshData BLOB Not Null,
    TopImage BLOB NOT NULL,
    PerspImage BLOB NOT NULL,
    SideImage BLOB NOT NULL,
    FrontImage BLOB NOT NULL,
    FileType TEXT CHECK( FileType IN ('obj','usd','fbx') )   NOT NULL DEFAULT 'obj'
);