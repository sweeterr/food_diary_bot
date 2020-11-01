FROM python:3.7

WORKDIR /food_diary_bot
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python"]

CMD ["bot.py"]