FROM python:3.8

COPY requirements.txt .

RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
COPY . .

EXPOSE 8000
CMD ["/usr/local/bin/gunicorn", "-w","2","-b","0.0.0.0:8000", "app:app", "--reload"]