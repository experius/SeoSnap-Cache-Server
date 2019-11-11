FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV LISTEN_PORT 5000
EXPOSE 5000

WORKDIR /app

# Copy program
COPY . .

# Setup program
RUN pip install -r requirements.txt

# Mount cache
RUN mkdir /app/cache
VOLUME /app/cache

ENV RENDERTRON_CACHE_ROOT=/app/cache