import sqlite3

conn = sqlite3.connect("metaHousing.sqlite")

for page_id, name, slug, meta in conn.execute("SELECT * FROM metaData"):
    itemID = page_id
    print(itemID)
    print("-"*20)

for row in conn.execute("SELECT pageID, meta FROM metaData"):
    print(row)

conn.close()
