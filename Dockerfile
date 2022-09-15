FROM gitlab.devpizzasoft.ru:4567/root/public-containers/python-pylint:2.12.2-python3.10.2-alpine3.15

WORKDIR /infoish

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]

