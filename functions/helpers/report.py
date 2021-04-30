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
    
    def create_report(self,predictions,forest,data,years):
        
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
        pdf.text(x, y, 'Current')
        pdf.text(x, y + 15, 'area of')
        pdf.text(x, y + 30, 'the forest')


        x = 130
        y = 230
        pdf.text(x, y, 'Predicted')
        pdf.text(x, y + 15, 'area of')
        pdf.text(x, y + 30, 'forest')

        # -------------

        x = 130
        y = 153
        # pdf.text(x, y, 'Predicted')
        pdf.set_font('Arial', 'B', 45)
        pdf.text(x, y + 14, str(round(forest['forest_year_10'],2)))
        pdf.set_font('Arial', 'B', 30)
        pdf.text(x+6, y + 27, 'Sq. KM')
        # pdf.text(x, y + 30, 'of forest')

        x = 35
        y = 230
        pdf.set_font('Arial', 'B', 45)
        pdf.text(x-2, y+12, str(round(predicted_area,2)))
        pdf.set_font('Arial', 'B', 30)
        # pdf.text(x, y + 15, 'percetage')
        pdf.text(x+2, y + 25, 'Sq. KM')

        # -------------------------------------------------------
        
        pdf.add_page()
        pdf.image(os.path.abspath(os.path.join(os.getcwd(),"report_templates/deforestation3.png")),0,0,width, height)                #image3
        pdf.set_font('Arial', 'B', 16)
        del forest["REGION"]
        del forest["AREA"]
        a = list(forest.iloc[0])
        y = a[1:11]
        fig = plt.figure(figsize=(6, 3.7), dpi=300, edgecolor = "green")
        plt.plot(years,y, color = "green")
        plt.xticks(np.arange(min(years), max(years)+1, 1.0))
        plt.ylabel('Forest in Sq. km')
        plt.xlabel('Years')
        plt.savefig("figure1.png")
        pdf.image("figure1.png",10,77, width-10,((width-10)/6)*3.7)
        pdf.set_font('Arial', 'B', 18)
        last_year_area_forest = forest['forest_year_10']                       #current last year foreset data
        # last_year_area_crop = forest['crops_year_10']                          #current last year crops data
        pdf.text(21, 247, '%.1f'%(last_year_area_forest/total_area * 100) + "%")
        # pdf.text(115, 247, '%.1f'%(last_year_area_crop/total_area * 100) + "%")
        pdf.text(115, 247, '%.1f'%(predicted_area/total_area * 100) + "%")
        path=os.path.abspath(os.path.join(os.getcwd(),f"reports/{name}.pdf"))
        pdf.output(path, 'F')
        return path
