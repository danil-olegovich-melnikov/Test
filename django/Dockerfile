FROM python:3.9

WORKDIR /app/django

COPY requirements.txt ./
COPY entrypoint.sh ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x ./entrypoint.sh

COPY . ./

ENTRYPOINT ["sh", "/app/django/entrypoint.sh"]
CMD python3 manage.py collectstatic --noinput; python3 manage.py runserver 0.0.0.0:8000
