FROM python:3.7-slim

EXPOSE 80
WORKDIR /usr/src/mapkit_token

# Split dependency installation out to attempt to optimize Docker layering
COPY mapkit_token/requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


COPY mapkit_token/app.py .

CMD ["python", "-m", "aiohttp.web", \
               "-H", "0.0.0.0", \
               "-P", "80", \
               "app:create_app"]
