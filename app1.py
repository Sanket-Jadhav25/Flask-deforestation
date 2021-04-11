from flask import Flask,render_template,request
import requests as req
import threading

import ast
from functions.main_download import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('predict.html')
@app.route('/download', methods = ['POST','GET'])
def download():
    if request.method == "POST":
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
        thread = threading.Thread(target=download_images, kwargs=data)
        thread.start()
        return render_template('download1.html')





if __name__ == '__main__':
    app.run(port=8000)


