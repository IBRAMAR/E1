import os
import requests
from flask import Flask, flash, request, redirect, url_for, render_template, session, jsonify,g
from werkzeug.utils import secure_filename
from flask import send_from_directory
from tensorflow import keras
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
from keras.applications.vgg16 import VGG16, preprocess_input
from functools import wraps
import sqlite3
import plotly
import json
import pandas as pd

UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
app = Flask(__name__, template_folder='template')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "m4xpl0it"
app.database = 'project.db'
# app._static_folder = './static/css/main.css'

#model = keras.models.load_model('./trained_model/2020-09-04_VGG_model.h5')
path = './trained_model/2020-09-04_VGG_model.h5'
basedir = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(basedir,path )
model = keras.models.load_model(MODEL_PATH)

def preprocess_imgs(set_name, img_size):
  print('je suis dans la fonction preprocess imgs')
  set_new = []
  for img in set_name:
      img = cv2.resize(
          img,
          dsize=img_size,
          interpolation=cv2.INTER_CUBIC
      )
      set_new.append(preprocess_input(img))
  return np.array(set_new)

def get_prediction(image_bytes):
  print('je suis dans la fonction get prediction')
  img_crop = Image.open(BytesIO(image_bytes))
  img_crop = np.expand_dims(img_crop, axis=0)
  #imp_prepro = preprocess_imgs(set_name=[img_crop], img_size=IMG_SIZE)
  IMG_SIZE = (224,224)
  imp_prepro = preprocess_imgs(set_name=img_crop, img_size=IMG_SIZE)
  pred = model.predict_classes(imp_prepro)
  result = ["Abscence de tumeur " if pred[0][0] == 0 else " Possible présence de tumeur "]
  return result[0]

def connect_db():
    return sqlite3.connect(app.database)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
def login_required_DS(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login_DS'))
    return wrap

@app.route('/empty_page')
def empty_page():
    #filename = session.get('filename', None)
    #os.remove(os.path.join( UPLOAD_FOLDER, filename))
    return redirect(url_for('home'))
    #return render_template('home.html')

@app.route('/datascientists', methods=['POST', 'GET'])
@login_required_DS
def datascientists():
    ds = session.get('user', None)
    return render_template('datascientists.html', ds=ds)

@app.route('/doctor', methods=['POST', 'GET'])
@login_required
def doctor():
    image_label = False
    message = ' Submit for add label image'
    doctor = session.get('user', None)
    if request.method == 'POST':
        print('entrer du post')
        #f = request.files['bt_image']
        f = request.files['inputFile']
        filename = str(f.filename)
        print(filename)
        if filename!='':
            ext = filename.split(".")
            
            if ext[1] in ALLOWED_EXTENSIONS: # check if allowed extension see upper
                
                
                filename = secure_filename(f.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                basedir = os.path.abspath(os.path.dirname(__file__))
                print('before uploading')
                with open(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename),'rb') as img:
                    file = img.read()
                # print('longueur fichier est de :',len(file))
                label = request.form['label']
                name = filename
                doctor = session.get('user', None)
                #doctor = 'aymen'
                g.db = connect_db()
                print('connection oki')
                c = g.db.cursor()
                # insert new labelise data into new table data
                c.execute('INSERT INTO data (image,name,label,doctor) VALUES(?, ?, ?, ?)',(file,name, label, doctor))
                g.db.commit()
                c.close()
                g.db.close()
                image_label = True
                message = f'{filename} added to db !! '
                print('save db oki !!')
    return render_template('doctor.html', image_label = image_label, message= message,doctor=doctor)

@app.route('/pred_page')
def pred_page():
    pred = session.get('pred_label', None)
    f_name = session.get('filename', None)
    return render_template('pred.html', pred=pred, f_name=f_name)

@app.route("/test_link")
def test_link():
    return render_template('test_link.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/predict', methods=['POST'])
def predict():
  if request.method == 'POST':
    file = request.files['file']
    img_bytes = file.read()
    prediction = get_prediction(img_bytes)
    data= {}
    data['prediction'] = prediction
    return jsonify(data)

@app.route('/login', methods=['GET','POST'])
def login():
    g.db = connect_db()
    #cur = g.db.execute('select * from users')
    res = g.db.execute("select * from doctor")
    #posts = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
    dic_users = {}
    users = []
    passwords = []
    for row in res:
        users.append(row[0])
        passwords.append(row[1])
        
    dic_users['username'] = users
    dic_users['password'] = passwords

    g.db.close()
    error=None
    if request.method == 'POST':
        # if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if request.form['username']  not in  dic_users['username'] or request.form['password'] not in dic_users['password']:
            error = 'Invalids credentials. Please try agin'
        else:
            session['logged_in'] = True
            flash('Your were just logged in!')
            session['user'] = request.form['username']
            doctor = session.get('user', None)
            return redirect(url_for('doctor',doctor=doctor))
    #return render_template('login.html',error=error,posts=posts)
    return render_template('login.html',error=error)

@app.route('/login_DS', methods=['GET','POST'])
def login_DS():
    g.db = connect_db()
    #cur = g.db.execute('select * from users')
    res = g.db.execute("select * from ds")
    #posts = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
    dic_users = {}
    users = []
    passwords = []
    for row in res:
        users.append(row[0])
        passwords.append(row[1])
        
    dic_users['username'] = users
    dic_users['password'] = passwords

    g.db.close()
    error=None
    if request.method == 'POST':
        # if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if request.form['username']  not in  dic_users['username'] or request.form['password'] not in dic_users['password']:
            error = 'Invalids credentials. Please try agin'
        else:
            session['logged_in'] = True
            flash('Your were just logged in!')
            session['user'] = request.form['username']
            ds = session.get('user', None)
            return redirect(url_for('datascientists',ds=ds))
    #return render_template('login.html',error=error,posts=posts)
    return render_template('login_DS.html',error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Your were just logged out!')
    return redirect(url_for('login'))

@app.route('/logout_DS')
@login_required_DS
def logout_DS():
    session.pop('logged_in', None)
    flash('Your were just logged out!')
    return redirect(url_for('login_DS'))

@app.route('/', methods=['POST', 'GET'])
def home():
    #try:
    if request.method == 'POST':
        f = request.files['bt_image']
        filename = str(f.filename)

        if filename!='':
            ext = filename.split(".")
            
            if ext[1] in ALLOWED_EXTENSIONS: # check if allowed extension see upper
                filename = secure_filename(f.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                basedir = os.path.abspath(os.path.dirname(__file__))
                with open(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename),'rb') as img:
                    image_new = img.read()

                predicted = requests.post("http://localhost:5000/predict", files={"file": image_new}).json()
                session['pred_label'] = predicted['prediction']
                
                session['filename'] = filename

                #return redirect(url_for('pred'))
                return redirect(url_for('pred_page'))
                #return type(image_new)
    #except Exception as e:
    #    print("Exception\n")
    #   print(e, '\n')
    #return redirect(url_for('uploaded_file', filename=filename))
    return render_template('home.html')

@app.route('/metrics')
def metrics():
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)
    g.db = connect_db()
    c = g.db.cursor()
    res_yes = g.db.execute("SELECT COUNT(label) FROM data_brute WHERE label='yes';")
    nb_yes = res_yes.fetchone()
    res_no = g.db.execute("SELECT COUNT(label) FROM data_brute WHERE label='no';")
    nb_no = res_no.fetchone()
    res_labo_1 = g.db.execute("SELECT COUNT(institution) FROM doctor WHERE institution='labo 1';")
    nb_labo_1 = res_labo_1.fetchone()
    res_labo_2 = g.db.execute("SELECT COUNT(institution) FROM doctor WHERE institution='labo 2';")
    nb_labo_2 = res_labo_2.fetchone()
    res_labo_3 = g.db.execute("SELECT COUNT(institution) FROM doctor WHERE institution='labo 3';")
    nb_labo_3 = res_labo_3.fetchone()
    res_ds_A = g.db.execute("SELECT COUNT(compagny) FROM ds WHERE compagny='Compagny A';")
    nb_ds_A = res_ds_A.fetchone()
    res_ds_B = g.db.execute("SELECT COUNT(compagny) FROM ds WHERE compagny='Compagny B';")
    nb_ds_B = res_ds_B.fetchone()
    res_ds_C = g.db.execute("SELECT COUNT(compagny) FROM ds WHERE compagny='Compagny C';")
    nb_ds_C = res_ds_C.fetchone()




    g.db.commit()
    c.close()
    g.db.close()
    
    graphs = [
        {
            'data' : [
                {
                  'values': [nb_yes[0], nb_no[0]],
                  'labels': ['Cancer', 'No_cancer'],
                   'type': 'pie',
                #    'width':100, 
                #    'height':100,
                }
                    ]
                ,
            'layout': {
                # 'title':'Dataset', 
                'autosize': True,
                'div':'a'}
        }
        ,
                dict(
            data=[

                dict(
                    x=['labo1', 'labo2', 'labo3'],
                    y=[nb_labo_1[0], nb_labo_2[0], nb_labo_3[0]],
                    type='bar',
                    # name= 'LA Zoo',
                    marker=  dict(color=['rgb(106, 237, 100)', 'rgb(100, 100, 237)','rgb(237, 100, 150)'])
                ),
            ],
            layout=dict(
                # title='c',
                barmode= 'group',
                div = 'b',
            )
        ),
        dict(
            data=[
                dict(
                    values= [nb_ds_A[0],nb_ds_B[0],nb_ds_C[0]],
                    # values= [3,4,5],
                    labels=['Company_A','Company_B','Company_C'],
                    type='pie',
                ),
            ],
            layout=dict(
                # title='b',
                autosize= True,
                div = 'c',
            )
        ),


        dict(
            data=[

                dict(
                    x= ['Liam', 'Sophie', 'Jacob', 'Mia', 'William', 'Olivia'],
                    y=[8.0, 8.0, 12.0, 12.0, 13.0, 20.0],
                    type='bar',
                     name= 'tumor',
                    marker=  dict(color='rgb(142,124,195)')
                ),
                dict(
                    x= ['Liam', 'Sophie', 'Jacob', 'Mia', 'William', 'Olivia'],
                    y=[18.0, 18.0, 2.0, 2.0, 3.0, 2.0],
                    type='bar',
                    name= ' No tumor',
                    marker=  dict(color='rgb(255, 0, 0)')
                ),
            ],
            layout=dict(
                title='labo 1',
                barmode= 'group',
                div = 'd',
            )
        ),
        dict(
            data=[

                dict(
                    x= ['Liam', 'Sophie', 'Jacob', 'Mia', 'William', 'Olivia'],
                    y=[8.0, 8.0, 12.0, 12.0, 13.0, 20.0],
                    type='bar',
                    name= 'Tumor',
                    marker=  dict(color='rgb(142,124,195)')
                ),
                dict(
                    x= ['Liam', 'Sophie', 'Jacob', 'Mia', 'William', 'Olivia'],
                    y=[18.0, 18.0, 2.0, 2.0, 3.0, 2.0],
                    type='bar',
                    name= ' No Tumor',
                    marker=  dict(color='rgb(255, 0, 0)')
                ),
            ],
            layout=dict(
                title='labo 2',
                barmode= 'group',
                div = 'e',
            )
        ),
        dict(
            data=[

                dict(
                    x= ['Liam', 'Sophie', 'Jacob', 'Mia', 'William', 'Olivia'],
                    y=[8.0, 8.0, 12.0, 12.0, 13.0, 20.0],
                    type='bar',
                    name= 'Tumor',
                    marker=  dict(color='rgb(142,124,195)')
                ),
                dict(
                    x= ['Liam', 'Sophie', 'Jacob', 'Mia', 'William', 'Olivia'],
                    y=[18.0, 18.0, 2.0, 2.0, 3.0, 2.0],
                    type='bar',
                    name= ' No Tumor',
                    marker=  dict(color='rgb(255, 0, 0)')
                ),
            ],
            layout=dict(
                title='labo 3',
                barmode= 'group',
                div = 'f',
            )
        ),


      
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    # ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    # ids = [f"{i['layout']['title']}" for i in graphs]
    ids = [f"{i['layout']['div']}" for i in graphs]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('metrics.html',
                           ids=ids,
                           graphJSON=graphJSON)


@app.route('/test_metrics')
def test_metrics():
    return render_template('test_metrics.html')


if __name__=="__main__":
    app.run()
    app.run(debug=True)
    