import sqlite3

# create a new database if the database doesn't already exist
with sqlite3.connect('project.db') as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    
    # create the table
    c.execute('DROP TABLE data')
    c.execute('CREATE TABLE data(image blob,name TEXT PRIMARY KEY , label TEXT, doctor TEXT)')

    # insert  data into the table
    with open('./static/images/0.jpg','rb') as img:
        file = img.read()
    label = 'tumor'
    name ='image1'
    doctor = 'ibrahim'
    c.execute('INSERT INTO data (image,name,label,doctor) VALUES(?, ?, ?, ?)',(file,name, label, doctor))
    label = 'tumor'
    name ='image2'
    doctor = 'aymen'
    c.execute('INSERT INTO data (image,name,label,doctor) VALUES(?, ?, ?, ?)',(file,name, label, doctor))
    label = 'tumor'
    name ='image3'
    doctor = 'ibrahim'
    c.execute('INSERT INTO data (image,name,label,doctor) VALUES(?, ?, ?, ?)',(file,name, label, doctor))
    label = 'tumor'
    name ='image4'
    doctor = 'aymen'
    c.execute('INSERT INTO data (image,name,label,doctor) VALUES(?, ?, ?, ?)',(file,name, label, doctor))
