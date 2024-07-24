FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3000

ENTRYPOINT [ "python" ]

CMD ["app.py"]