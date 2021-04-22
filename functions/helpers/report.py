import os
import matplotlib.pyplot as plt
from io import BytesIO
from svglib.svglib import svg2rlg
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from svglib.svglib import svg2rlg
class Report():
    def __init__(self):
        pass
    
    def create_report(self,predictions,forest,data):
        
        width = 210
        height = 297

        # -------------------------------------------------------

        pdf = FPDF()
        pdf.add_page()
        pdf.image(os.path.abspath(os.path.join(os.getcwd(),"report_templates/deforestation1.png")),0,0,width, height)      #image 1

        # -------------------------------------------------------

        pdf.add_page()
        pdf.image(os.path.abspath(os.path.join(os.getcwd(),"report_templates/deforestation2.png")),0,0,width, height)       #image 2

        name = f"{data['Region']} {data['Area']}"                      #name of the area
        total_area = forest['TOTAL_AREA']                                                  #toatl area 
        predicted_area = predictions                                           #predicted area
        year = data['Year']                                                       #prediction year   
        pdf.set_font('Arial', 'B', 30)

        # fpdf.text(x: float, y: float, txt: str)

        pdf.text(20, 35, 'Name of area: ')
        pdf.text(20, 55, name)
        pdf.text(20, 75, 'Prediction for the year: '+ str(year))

        x = 35
        y = 153
        pdf.text(x, y, 'Predicted')
        pdf.text(x, y + 15, 'percetage')
        pdf.text(x, y + 30, 'of forest')


        x = 130
        y = 230
        pdf.text(x, y, 'Predicted')
        pdf.text(x, y + 15, 'Area of')
        pdf.text(x, y + 30, 'forest')

        # -------------

        x = 130
        y = 153
        # pdf.text(x, y, 'Predicted')
        pdf.set_font('Arial', 'B', 45)
        pdf.text(x-1, y + 18, '%.2f'%(predicted_area/total_area * 100) + "%")
        # pdf.text(x, y + 30, 'of forest')

        x = 35
        y = 230
        pdf.text(x-2, y+12, str(predicted_area))
        pdf.set_font('Arial', 'B', 30)
        # pdf.text(x, y + 15, 'percetage')
        pdf.text(x+2, y + 25, 'Sq. KM')

        # -------------------------------------------------------
        
        pdf.add_page()
        pdf.image(os.path.abspath(os.path.join(os.getcwd(),"report_templates/deforestation3.png")),0,0,width, height)                #image3
        pdf.set_font('Arial', 'B', 16)
        # pdf.cell(40, 10, 'Hello World!')
        # pdf.add_page()
        # forest = pd.read_csv(r'D:\final.csv')                                        #csv data
        del forest["REGION"]
        del forest["AREA"]
        a = list(forest.iloc[0])
        y = a[1:11]
        x = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
        fig = plt.figure(figsize=(6, 3.7), dpi=300, edgecolor = "green")
        plt.plot(x,y, color = "green")
        plt.xticks(np.arange(min(x), max(x)+1, 1.0))
        plt.ylabel('Forest in Sq. km')
        plt.xlabel('Years')
        plt.savefig("figure1.png")
        pdf.image("figure1.png",10,77, width-10,((width-10)/6)*3.7)
        pdf.set_font('Arial', 'B', 18)
        last_year_area_forest = 486                                                 #current last year foreset data
        last_year_area_crop = 195                                                   #current last year crops data
        pdf.text(21, 247, '%.1f'%(last_year_area_forest/total_area * 100) + "%")
        pdf.text(115, 247, '%.1f'%(last_year_area_crop/total_area * 100) + "%")
        path=os.path.abspath(os.path.join(os.getcwd(),f"reports/{name}.pdf"))
        pdf.output(path, 'F')
        return path