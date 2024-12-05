FROM hdgigante/python-opencv:4.10.0-alpine
RUN apk add gcc build-base linux-headers ffmpeg
RUN pip install flask==3.1.0 uwsgi flask-cors>=5.0.0 google-cloud-storage==2.18.2 moviepy==1.0.3 requests==2.32.3 --no-cache-dir
# RUN pip install opencv-python==4.10.0.84
WORKDIR /app
COPY . .
CMD ["uwsgi", "--ini", "uwsgi.ini"]
EXPOSE 8080
