FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN rm -r historic_csv_files
ENV TZ=America/Argentina/Buenos_Aires
CMD ["/bin/bash", "docker_entrypoint.sh"]