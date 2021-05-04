FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /deploy/
RUN pip install --upgrade pip && \
    pip install -r /deploy/requirements.txt

ADD . /deploy
WORKDIR /deploy

ENV BASE_DIR=/deploy

EXPOSE 80

CMD ["uvicorn", "ml_api.main:app", "--host", "0.0.0.0", "--port", "80"]
