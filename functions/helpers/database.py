import sqlite3 as sql

class DataBase():
    def __init__(self,db_path):
        self.db_path=db_path
    
    def connect(self,):
        self.conn = sql.connect(self.db_path)
        self.conn.row_factory = sql.Row
        self.cur = self.conn.cursor()

        
    def create_table(self,):
        self.connect()
        self.conn.execute('CREATE TABLE IF NOT EXISTS prediction (coords TEXT, email TEXT, area TEXT, region TEXT,username TEXT)')
        self.conn.close()
    
    def insert(self,data):
        self.create_table()
        self.connect()
        self.cur.execute("INSERT INTO prediction (coords,email,area,region,username)VALUES(?, ?, ?, ?, ?)",(str(data['Co-ordinate']),data['Email'],data['Area'],data['Region'],data['User']))
        self.conn.commit()
        self.conn.close()
    
    def get_last(self,):
        self.connect()
        return self.cur.execute('select * from prediction').fetchall()[-1]
