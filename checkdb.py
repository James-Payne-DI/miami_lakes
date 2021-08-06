import sqlite3

conn = sqlite3.connect("metaHousing.sqlite")

for page_id, name, slug, meta in conn.execute("SELECT * FROM metaData"):
    itemID = page_id
    print(itemID)
    print("-"*20)

for row in conn.execute("SELECT pageID, meta FROM metaData"):
    print(row)

conn.close()

clear_db = input("would you like to clear the database (y/n)? ")


if clear_db == "y":
    #Connecting to sqlite
    conn = sqlite3.connect('metaHousing.sqlite')
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #Doping EMPLOYEE table if already exists
    cursor.execute("DROP TABLE metaData")
    print("Table dropped... rowcount is: ", cursor.rowcount)
    #Commit your changes in the database
    conn.commit()
    #Closing the connection
    conn.close()
