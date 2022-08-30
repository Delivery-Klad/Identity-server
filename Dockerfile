FROM python:3.8

ENV DATABASE_URL=
ENV SECRET=

ADD requirements.txt /requirements.txt
ADD run.py /main.py
ADD okteto-stack.yaml /okteto-stack.yaml
RUN pip install -r requirements.txt

EXPOSE 8080
COPY ./app app

CMD ["python3", "main.py"]