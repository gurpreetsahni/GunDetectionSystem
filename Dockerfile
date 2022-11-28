FROM python:3.8.5
RUN apt-get update &&\
    apt-get install ffmpeg libsm6 libxext6 -y &&\
    apt install sox -y
EXPOSE 8501
WORKDIR /app
COPY ./app .
RUN pip3 install -r requirements.txt
CMD streamlit run weapon_detection.py

