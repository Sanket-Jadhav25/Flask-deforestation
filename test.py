from dotenv.main import load_dotenv
from functions.helpers.email_ import Email
import os
import pandas as pd
from functions.helpers.report import Report
load_dotenv()

forest = pd.read_csv('reports\\final.csv')
rp=Report()
report_path='reports/test.pdf'
report_path=rp.create_report(predictions='405',df=forest.iloc[10],path=report_path)
email=os.getenv('email')
password=os.getenv('password')
print(email,password)
em=Email(email,password)
subject='This is Subject 2'
mail_content='Report 2'
print(report_path)
em.send_email(reciver='ankitkotharkar99@gmail.com',subject=subject,content=mail_content,files=[report_path])
em.send_email(reciver='chavanomkar245@gmail.com',subject=subject,content=mail_content,files=[report_path])