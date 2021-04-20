from PIL import Image
from reportlab.pdfgen.canvas import Canvas
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.lib.utils import ImageReader
import pandas as pd
import random
import numpy as np

def create_pdf(path):
    
    c = Canvas()

    forest = pd.read_csv('reports/')

    del forest["REGION"]
    del forest["AREA"]

    a = list(forest.iloc[0])
    y = a[1:11]

    x = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    fig = plt.figure(figsize=(6, 4))
    plt.plot(x,y)
    plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    plt.ylabel('Forest in Sq. km')
    plt.xlabel('Years')

    imgdata = BytesIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data

    drawing=svg2rlg(imgdata)

    renderPDF.draw(drawing,c, 50, 450)
    c.showPage()
    c.save()
    return path