FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV LISTEN_PORT 5000
EXPOSE 5000

WORKDIR /app

# Logging
RUN mkdir /app/logs
VOLUME /app/logs

# Install reqs
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy program
COPY . /app/

# Mount cache
RUN mkdir /app/cache
VOLUME /app/cache

ENV RENDERTRON_CACHE_ROOT=/app/cache