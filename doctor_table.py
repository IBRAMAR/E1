import sqlite3

# create a new database if the database doesn't already exist
with sqlite3.connect('project.db') as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    
    # create the table
    c.execute('DROP TABLE doctor')
    c.execute('CREATE TABLE  doctor (doctor TEXT PRIMARY KEY, password TEXT, institution Text, FOREIGN KEY (doctor) REFERENCES data (doctor) )')

    # insert dummy data into the table
    
    c.execute('INSERT INTO doctor VALUES("ibrahim", "marsit","labo 1")')
    c.execute('INSERT INTO doctor VALUES("ibrahim1", "marsit","labo 1")')
    c.execute('INSERT INTO doctor VALUES("ibrahim2", "marsit","labo 1")')
    c.execute('INSERT INTO doctor VALUES("ibrahim3", "marsit","labo 1")')
    c.execute('INSERT INTO doctor VALUES("aymen", "marsit","labo 2")')
    c.execute('INSERT INTO doctor VALUES("aymen1", "marsit","labo 2")')
    c.execute('INSERT INTO doctor VALUES("aymen2", "marsit","labo 2")')
    c.execute('INSERT INTO doctor VALUES("aymen3", "marsit","labo 2")')
    c.execute('INSERT INTO doctor VALUES("bassem", "marsit","labo 3")')
    c.execute('INSERT INTO doctor VALUES("bassem1", "marsit","labo 3")')
    c.execute('INSERT INTO doctor VALUES("bassem2", "marsit","labo 3")')
    c.execute('INSERT INTO doctor VALUES("bassem3", "marsit","labo 3")')
    c.execute('INSERT INTO doctor VALUES("yamina", "karoui","labo 3")')
    c.execute('INSERT INTO doctor VALUES("yamina1", "karoui","labo 2")')
    c.execute('INSERT INTO doctor VALUES("yamina2", "karoui","labo 1")')
    c.execute('INSERT INTO doctor VALUES("yamina3", "karoui","labo 1")')
    c.execute('INSERT INTO doctor VALUES("ayah", "marsit","labo 1")')
    c.execute('INSERT INTO doctor VALUES("ayah1", "marsit","labo 1")')
    c.execute('INSERT INTO doctor VALUES("ayah2", "marsit","labo 3")')
    c.execute('INSERT INTO doctor VALUES("ayah3", "marsit","labo 2")')

