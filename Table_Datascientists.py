import sqlite3

# create a new database if the database doesn't already exist
with sqlite3.connect('project.db') as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    
    # create the table
    c.execute('DROP TABLE ds')
    c.execute('CREATE TABLE  ds (Name TEXT PRIMARY KEY , password TEXT, compagny Text, FOREIGN KEY (compagny) REFERENCES Compagnies (name) )')

    # insert dummy data into the table
    
    c.execute('INSERT INTO ds VALUES("ibrahim", "marsit","Compagny_A")')
    c.execute('INSERT INTO ds VALUES("aymen", "marsit","Compagny_A")')
    c.execute('INSERT INTO ds VALUES("bassem", "marsit","Compagny_A")')
    c.execute('INSERT INTO ds VALUES("ibrahim1", "marsit","Compagny_B")')
    c.execute('INSERT INTO ds VALUES("aymen1", "marsit","Compagny_B")')
    c.execute('INSERT INTO ds VALUES("bassem1", "marsit","Compagny_B")')
    c.execute('INSERT INTO ds VALUES("ibrahim2", "marsit","Compagny_C")')
    c.execute('INSERT INTO ds VALUES("aymen2", "marsit","Compagny_C")')
    c.execute('INSERT INTO ds VALUES("bassem2", "marsit","Compagny_B")')
