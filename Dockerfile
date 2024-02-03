FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD python app.py
