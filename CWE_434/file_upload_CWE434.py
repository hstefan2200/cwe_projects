"""
CWE-434: Unrestricted Upload of File with Dangerous Type
"""

import os
from random import choice
from flask import Flask, render_template, request, send_from_directory, redirect, url_for

# UPLOAD_FOLDER = '/home/ec2-user/environment/SDEV325/static/uploads'
UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload')
def upload():
    """upload page"""
    return render_template('upload.html')
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            filename = f.filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file', filename=filename))
            return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
   
@app.route('/uploads')
def uploads():
    path = os.getcwd()+'/static/uploads'
    img_list = {}
    for name in os.listdir(path):
        img_list[name] = path+name
    return render_template('uploads.html', img_list=img_list)

if __name__ == '__main__':
    app.debug = True
    app.run(host=os.environ['IP'], port=os.environ['PORT']) 
    