# Start with a "fat" python image as we need the compiler to install some
# Python packages
FROM python:3.8 AS builder

WORKDIR /usr/local/src

# Third-party deps
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# This code
COPY setup.py setup.py
COPY mapkit_token_server mapkit_token_server
RUN pip install --user .

FROM python:3.8-slim
COPY --from=builder /root/.local /root/.local

EXPOSE 80

CMD ["python", "-m", "aiohttp.web", \
               "-H", "0.0.0.0", \
               "-P", "80", \
               "mapkit_token_server:create_app"]
