import sqlite3

# create a new database if the database doesn't already exist
with sqlite3.connect('project.db') as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()

    # create the table
    # c.execute('DROP TABLE Compagnies')
    # c.execute('CREATE TABLE Compagnies(name TEXT PRIMARY KEY , adresse TEXT)')

    # insert  data into the table
    c.execute('INSERT INTO Compagnies VALUES("Compagny_A","adress_A")')
    c.execute('INSERT INTO Compagnies VALUES("Compagny_B","adress_B")')
    c.execute('INSERT INTO Compagnies VALUES("Compagny_C","adress_C")')
  
  
