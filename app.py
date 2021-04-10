from flask import Flask,render_template,request
import sqlite3 as sql

app = Flask(__name__)
conn = sql.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS prediction (down TEXT, email TEXT, country TEXT, region TEXT)')
print ("Table created successfully")
conn.close()


@app.route('/')
def hello_world():
    return render_template('predict.html')
@app.route('/download', methods = ['POST','GET'])
def download():
    if request.method == "POST":
        down = request.form.get("Coordinates")
        email = request.form.get("email")
        country = request.form.get("country")
        region = request.form.get("region")
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

        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO prediction (down,email,country,region)VALUES(?, ?, ?, ?)",(down,email,country,region))
            con.commit()
            msg = "Record successfully added"
        from fire import db
        down1 = db()[0]
        email1 = db()[1]
        country1 = db()[2]
        region1 = db()[3]
        return render_template('download1.html', down1=down1, email1=email1, country1=country1, region1=region1)




if __name__ == '__main__':
    app.run()


