import sqlite3

# create a new database if the database doesn't already exist
with sqlite3.connect('project.db') as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    
    # create the table
    c.execute('DROP TABLE doctor')
    # c.execute('CREATE TABLE  doctor(doctor TEXT, password TEXT)')
    c.execute('CREATE TABLE  doctor (doctor TEXT PRIMARY KEY, password TEXT, institution Text, FOREIGN KEY (doctor) REFERENCES data (doctor) )')

    # insert dummy data into the table
    
    c.execute('INSERT INTO doctor VALUES("ibrahim", "marsit","labo 1")')
    c.execute('INSERT INTO doctor VALUES("aymen", "marsit","labo 2")')
    c.execute('INSERT INTO doctor VALUES("bassem", "marsit","labo 3")')
    c.execute('INSERT INTO doctor VALUES("yamina", "karoui","labo 4")')