FROM python:3.8.0-slim

COPY . /app
WORKDIR /app
# RUN add-apt-repository ppa:ubuntugis/ppa

RUN apt-get -y update
RUN apt-get install -y gdal-bin libgdal-dev
RUN pip install -U pip
RUN pip install rasterio
RUN pip install -r requirements.txt
RUN pip install --upgrade google-api-python-client oauth2client
RUN pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.4.0-cp38-cp38-manylinux2010_x86_64.whl

CMD ["python", "app.py"]



