FROM python:3.9.16-alpine

RUN apk add bash vim gzip tar git openldap-clients npm

RUN mkdir --parents /work/pcds_expresults

COPY requirements.txt /work

RUN pip3 install -r /work/requirements.txt

COPY src /work/pcds_expresults

WORKDIR /work/pcds_expresults

RUN npm install

COPY startservice.sh /work

EXPOSE 5000 5001

CMD [ "/work/startservice.sh" ]
