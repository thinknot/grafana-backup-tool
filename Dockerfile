FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade \
    pip \ 
    virtualenv

ENV DIRHOME /opt/grafana-backup-tool
WORKDIR $DIRHOME

ENV VIRTUAL_ENV=$DIRHOME/venv
RUN python3 -m virtualenv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY README.md README.md
COPY setup.py setup.py
COPY grafana_backup grafana_backup

RUN pip --no-cache-dir install .

COPY docker_entry.sh docker_entry.sh

RUN chown -R 1337:1337 /opt/grafana-backup-tool
USER 1337
ENTRYPOINT ["./docker_entry.sh"]
