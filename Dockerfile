FROM python:3.13

ADD src/*.py /src/
ADD logs/.conf /logs/

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "./src/bot.py" ]