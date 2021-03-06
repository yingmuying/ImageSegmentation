from flask import Flask, request,redirect,url_for,flash,render_template
from saliencyCut import processImage
from VGG16 import inference,vgg
import tensorflow as tf
import os
from werkzeug.utils import  secure_filename
app = Flask(__name__)
UPLOAD_FOLDER = "/home/clw/PycharmProjects/test/static/uploadImage"
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/',methods=['GET','POST'])
def upload_file():
    return render_template("index.html")
@app.route('/segimage',methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    full_filename = os.path.join(UPLOAD_FOLDER,filename)
    file.save(full_filename)
    processImage(full_filename)
    class_names,probs= inference(vgg,"{}process.jpg".format(full_filename))
    print(class_names)
    #return """
    #<html>
    #<img src="/static/uploadImage/{}process.jpg"/>
    #<p> 分类结果 </P>
    #<p>{}:{}</p>
    #""".format(filename,class_names[0],probs[0])
    return render_template("prediction.html",segFile="static/uploadImage/{}process.jpg".format(filename),
                            bboxFile="static/uploadImage/{}bbox.jpg".format(filename),
                            hcFile="static/uploadImage/{}hc.jpg".format(filename),
                            rawFile="static/uploadImage/{}".format(filename),
                           class_names=class_names
                           )

@app.after_request
def add_header(r):
    r.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    r.headers['Cache-Control'] = 'public,max-age=0'
    return  r
if __name__ == '__main__':
    app.run()
