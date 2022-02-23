FROM python:latest
LABEL Developer: 'Hans Silva Loaiza'
WORKDIR /usr/app/src
RUN pip3 install --upgrade pip --user
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python", "./run.py"]