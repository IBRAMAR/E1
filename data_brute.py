import sqlite3
import os
import os
import sqlite3
label_no = os.listdir('./brain_tumor_dataset/no/')
label_yes = os.listdir('./brain_tumor_dataset/yes/')
with sqlite3.connect('project.db') as connection:

    c = connection.cursor()
    
#     c.execute('DROP TABLE data_brute')
    c.execute('CREATE TABLE data_brute(image blob,name TEXT PRIMARY KEY , label TEXT)')
    # c.execute('CREATE TABLE Data_brute(Name VARCHAR(50), image BINARY(50),label INT, PRIMARY KEY(Name))')
    
    for img_name in label_no :
        with open(f'./brain_tumor_dataset/no/{img_name}','rb') as img:
            file = img.read()
            label = 'no'
            name = img_name
            c.execute('INSERT INTO data_brute (image,name,label) VALUES(?, ?, ?)',(file,name, label))
    for img_name in label_yes :
        with open(f'./brain_tumor_dataset/yes/{img_name}','rb') as img:
            file = img.read()
            label = 'yes'
            name = img_name
            c.execute('INSERT INTO data_brute  (image,name,label) VALUES(?, ?, ?)',(file,name, label))
        
