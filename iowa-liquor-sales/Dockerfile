FROM python:3.10
EXPOSE 8080

WORKDIR /iowa_sales

COPY ./src/requirements.txt .

RUN pip install -r requirements.txt

ADD . /iowa_sales

ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
