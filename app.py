
from dotenv import load_dotenv
from functions.helpers.email_ import Email
import os
from functions.main import download_images
from functions.helpers.database import DataBase
from flask import Flask,render_template,request
import threading
import logging
import json

load_dotenv()
logging.basicConfig(level=logging.ERROR)
app = Flask(__name__)

@app.route('/home')
@app.route('/')
def home():
    return render_template('predict.html')

@app.route('/faq')
def faq ():
    return render_template('faq.html')

@app.route('/how_to')
def how_to ():
    return render_template('howto.html')

@app.route('/aboutus')
def aboutus ():
    return render_template('aboutus.html')

@app.route('/download', methods = ['POST','GET'])
def download():
    if request.method == "POST":
        # db=DataBase('database.db')
        
        coords=json.loads(request.form.get("Coordinates"))['features'][0]['geometry']['coordinates']
        email = request.form.get("email")
        area = request.form.get("area")
        region = request.form.get("region")
        username = request.form.get("username")
        year = int(request.form.get("year"))

        data={'Area': area,
            'Co-ordinate': coords,
            'Region': region,
            'User':username,
            'Email':email,
            'Year':year}
        # data={'Area': 'Mumbai2',
        #     'Co-ordinate': [[[1.2289239793090503, 42.36919824433563],
        #                 [1.572418212890625, 42.36919824433563],
        #                 [1.572418212890625, 42.541619138577296],
        #                 [1.2289239793090503, 42.541619138577296],
        #                 [1.2289239793090503, 42.36919824433563]]],
        #     'Region': 'India',
        #     'User':'Omkar2',
        #     'Email':'meomkarchavan99@gmail.com',
        #     'Year':2023}
        thread = threading.Thread(target=download_images, kwargs={'data':data},)
        thread.start()
        
        email=os.getenv('email')
        password=os.getenv('password')
        em=Email(email,password)
        subject='Confirmation'
        mail_content=f"We have recived your request for {data['Region']} {data['Area']}"
        em.send_email(reciver=data['Email'],subject=subject,content=mail_content)
        return render_template('download.html',data=data)




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
    )
