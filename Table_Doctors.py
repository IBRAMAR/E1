import sqlite3

# create a new database if the database doesn't already exist
with sqlite3.connect('project.db') as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    
    # create the table
 
    c.execute('DROP TABLE  Doctors')
    c.execute('CREATE TABLE   Doctors (name TEXT PRIMARY KEY, password TEXT, labo Text, FOREIGN KEY (name) REFERENCES data (name) )')

    # insert 
    
    c.execute('INSERT INTO  Doctors VALUES("ibrahim", "marsit","labo 1")')
    c.execute('INSERT INTO  Doctors VALUES("ibrahim1", "marsit","labo 1")')
    c.execute('INSERT INTO  Doctors VALUES("ibrahim2", "marsit","labo 1")')
    c.execute('INSERT INTO  Doctors VALUES("ibrahim3", "marsit","labo 1")')
    c.execute('INSERT INTO  Doctors VALUES("aymen", "marsit","labo 2")')
    c.execute('INSERT INTO  Doctors VALUES("aymen1", "marsit","labo 2")')
    c.execute('INSERT INTO  Doctors VALUES("aymen2", "marsit","labo 2")')
    c.execute('INSERT INTO  Doctors VALUES("aymen3", "marsit","labo 2")')
    c.execute('INSERT INTO  Doctors VALUES("bassem", "marsit","labo 3")')
    c.execute('INSERT INTO  Doctors VALUES("bassem1", "marsit","labo 3")')
    c.execute('INSERT INTO  Doctors VALUES("bassem2", "marsit","labo 3")')
    c.execute('INSERT INTO  Doctors VALUES("bassem3", "marsit","labo 3")')
    c.execute('INSERT INTO  Doctors VALUES("ayah", "marsit","labo 1")')
    c.execute('INSERT INTO  Doctors VALUES("ayah1", "marsit","labo 1")')
    c.execute('INSERT INTO  Doctors VALUES("ayah2", "marsit","labo 3")')
    c.execute('INSERT INTO  Doctors VALUES("ayah3", "marsit","labo 2")')