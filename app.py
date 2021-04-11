from flask import Flask,render_template,request
import requests as req
import threading

import sqlite3 as sql
import ast
# from functions.main_download import *

app = Flask(__name__)
conn = sql.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS prediction (down TEXT, email TEXT, area TEXT, region TEXT,username TEXT)')
print ("Table created successfully")
conn.close()


@app.route('/')
def hello_world():
    return render_template('predict.html')
@app.route('/download', methods = ['POST','GET'])
def download():
    if request.method == "POST":
        coords = ast.literal_eval(request.form.get("Coordinates"))
        email = request.form.get("email")
        area = request.form.get("area")
        region = request.form.get("region")
        username = request.form.get("username")
        data={'Area': area,
            'coordinates': coords,
            'Region': region,
            'User':username,
            'Email':email}
        # print(data)
        # print(type(data['coordinates']))
        req.post("http://127.0.0.1:5000/download", data=data)
        # down = request.form.get("Coordinates")
        # email = request.form.get("email")
        # area = request.form.get("area")
        # region = request.form.get("region")
        # conn = sql.connect('database.db')
        # c = conn.cursor()
        #
        # # delete all rows from table
        # c.execute('DELETE FROM prediction;', );
        #
        # print('We have deleted', c.rowcount, 'records from the table.')
        #
        # # commit the changes to db
        # conn.commit()
        # # close the connection
        # conn.close()

        # with sql.connect("database.db") as con:
        #     cur = con.cursor()
        #     cur.execute("INSERT INTO prediction (down,email,area,region)VALUES(?, ?, ?, ?)",(down,email,area,region))
        #     con.commit()
        #     msg = "Record successfully added"
        # from fire import db
        # down1 = db()[0]
        # email1 = db()[1]
        # area1 = db()[2]
        # region1 = db()[3]
        # return render_template('download1.html', down1=down1, email1=email1, area1=area1, region1=region1)
        return render_template('download1.html')





if __name__ == '__main__':
    app.run(port=8000)


