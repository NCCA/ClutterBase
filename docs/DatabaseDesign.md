# Database Design

This database is going to be a very simple container. Each row will contain all that is required for an asset.

|Name|Type|Attributes|
|----|----|----------|
|ID  |Integer| Primary Key |
|Name| Text | Not Null |
|Description | Text | Not Null |
|MeshData | BLOB | Not Null|
|TopImage | BLOB | Not Null|
|SideImage| BLOB | Not Null|
|FrontImage|BLOB| Not Null|
|PerspImage|BLOB| Not Null| 