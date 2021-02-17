import sqlite3


with sqlite3.connect('project.db') as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    
    # create the table
    # c.execute('DROP TABLE imaging_centers')
    c.execute('CREATE TABLE imaging_centers(Name TEXT PRIMARY KEY , adress TEXT)')

    # insert  data into the table
    c.execute('INSERT INTO imaging_centers VALUES("labo1","adress_1")')
    c.execute('INSERT INTO imaging_centers VALUES("labo2","adress_2")')
    c.execute('INSERT INTO imaging_centers VALUES("labo3","adress_3")')