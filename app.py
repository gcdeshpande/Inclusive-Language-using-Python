from concurrent.futures import process
from pprint import pprint
from queue import PriorityQueue
import bcrypt
from flask import (Flask, flash, redirect, render_template, request, session, url_for)
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson import ObjectId
import os
import spacy
import PyPDF2
import pandas as pd
from PIL import Image
from pytesseract import pytesseract

path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app  = Flask(__name__)
app.secret_key = "super secret key"

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['inclusivity']

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/logindata', methods =["GET", "POST"])
def logindata():
    loginuser = db.userdata.find_one({'email' : request.form['email']})

    if loginuser:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), loginuser['password']) == loginuser['password']:
            session['email'] = request.form['email']
            return redirect(url_for('addtext'))

    return 'invalid username/password combination'

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/register', methods =["GET", "POST"])
def register():
    if request.method == 'POST':
        
        existing_user = db.userdata.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            db.userdata.insert_one({'name' : request.form['name'], 'email' : request.form['email'] , 'password' : hashpass})
            session['email'] = request.form['email']
            return redirect(url_for('addtext'))
        else:
            return 'username exists'

    return render_template('register.html')  

@app.route('/addtext')
def addtext():
    syllabusdb = db.usertext.find({'email': session['email']})
    if 'email' in session:
        return render_template('addtext.html',textdata = syllabusdb)
    else:
        return redirect(url_for('index')) 

@app.route('/textdata', methods =["GET", "POST"])
def textdata():
    db.usertext.insert_one({'email' : session['email'],'text' : request.form['textdata'], 'finaltext' : None})
    flash('syllabus uploaded successfully')
    return redirect(url_for('addtext'))

@app.route('/filedata', methods = ['GET', 'POST'])
def filedata(header=None):
    if request.method == 'POST': 
        file = request.files['filedata']
        filename = secure_filename(file.filename)
        test = request.form['option']
        print(test)
        
        if request.form['option'] == "text":
            with open(filename) as f:
                filecontent = f.read()
                print(filecontent)
                db.usertext.insert_one({'email' : session['email'] , 'text' : filecontent })
                return redirect(url_for('addtext'))
        elif request.form['option'] == "Image":
            path_to_image = request.files['filedata']
            pytesseract.tesseract_cmd = path_to_tesseract
            img = Image.open(path_to_image)
            text = pytesseract.image_to_string(img)
            db.usertext.insert_one({'email' : session['email'] , 'text' : text})
            print(text)
    return redirect(url_for('addtext'))

@app.route('/analyzer')
def analyzer():
    username  = db.userdata.find({'email': session['email']})
    syllabusdb = db.usertext.find({'email': session['email']})
    return render_template('analyzer.html', textdata = syllabusdb, data = username)

@app.route("/perdata/<oid>")
def perdata(oid):
    textdata = db.usertext.find_one({'_id': ObjectId(oid)})
    nlp = spacy.load('en_core_web_sm')

    file_doc = textdata['text']
    doc1 = nlp(file_doc)



    token1 = [token.text for token in doc1]
    print(token1)


    token1 = [[token.text,token.lemma_] for token in doc1]
    print(token1)

    from spacy.lang.en.stop_words import STOP_WORDS
    stop = STOP_WORDS

    token1 = [token.text for token in doc1]
    print(token1)
    filtered = [token.text for token in doc1]
    #filtered= " ".join(filtered)
    [token.text for token in doc1 if token.is_stop == False and       
    token.text.isalpha() == True]
    print(filtered)

    doc2 = pd.read_csv(r"newDataset.csv",encoding="utf-8-sig")
    doc2.head()

    vals1=doc2['KEY']

    vals2=doc2['VALUE'].values

    val2=vals2.tolist()

    val1=vals1.tolist()

    for i in range(len(filtered)):
        filtered[i] = filtered[i].lower()

    filtered

    for i in range(len(val1)):
        val1[i] = val1[i].lower()

    for i in range(len(val2)):
        val2[i] = val2[i].lower()

    print(val1)

    print(val2)

    Process=" ".join(filtered)
    print(Process,end='\n\n')

    for ex in val1:
        if ex in Process:
            print("YES")
            print(ex)
            print(val2[val1.index(ex)])
            Process=Process.replace(ex,val2[val1.index(ex)])
    
    print(Process)
    
    db.usertext.update_one(
        {"_id": ObjectId(oid)},
        {"$set": {"finaltext": Process}}
    )

    return redirect("/results/" + oid)

@app.route("/results/<oid>")
def results(oid):
    data  = db.usertext.find({"_id": ObjectId(oid)})
    return render_template('results.html',textdata = data)



# @app.route('/syllabusfile', methods = ['GET', 'POST'])
# def syllabusfile(header=None):
#     if request.method == 'POST': 
#         file = request.files['syllabusfile']
#         filename = secure_filename(file.filename)
        

#         print(request.form['filetype'])
#         if request.form['filetype'] == "Text":
            
#             with open(filename) as f:
#                 filecontent = f.read()
#                 print(filecontent)
#                 db.syllabusdata.insert_one({'email' : session['email'] , 'syllabus' : filecontent, 'Subject' : request.form['option'] })
#                 return redirect(url_for('dashboard'))
#         elif request.form['filetype'] == "Pdf":
#             return " Available in future" 
       
        

if __name__ == '__main__':
    app.debug = True
    app.run()