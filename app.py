
import os
from functions.main import download_images
from functions.helpers.database import DataBase
from flask import Flask,render_template,request
import threading
import logging
import ast
# from functions.main_download import *
import sys

logging.basicConfig(level=logging.ERROR)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('predict.html')
@app.route('/download', methods = ['POST','GET'])
def download():
    if request.method == "POST":
        db=DataBase('database.db')
        
        # coords = ast.literal_eval(request.form.get("Coordinates"))
        # email = request.form.get("email")
        # area = request.form.get("area")
        # region = request.form.get("region")
        # username = request.form.get("username")
        # data={'Area': area,
        #     'coordinates': coords,
        #     'Region': region,
        #     'User':username,
        #     'Email':email}
        data={'Area': 'Sant_Julia_de_Loria',
            'Co-ordinate': [[[1.2289239793090503, 42.36919824433563],
                        [1.572418212890625, 42.36919824433563],
                        [1.572418212890625, 42.541619138577296],
                        [1.2289239793090503, 42.541619138577296],
                        [1.2289239793090503, 42.36919824433563]]],
               'Region': 'Andorra',
            'User':'Username',
               'Email':'temp'}
        # db.insert(data)
        thread = threading.Thread(target=download_images, kwargs={'data':data},)
        thread.start()
        return render_template('download.html',data=data)





if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )
