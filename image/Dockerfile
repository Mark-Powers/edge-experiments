FROM python:3.7-alpine

COPY requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY power_meter.py ./power_meter.py
COPY main.py ./main.py
COPY rpc_client.py ./rpc_client.py

CMD [ "python", "./main.py" ]
