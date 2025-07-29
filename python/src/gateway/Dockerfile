FROM python:3.10-slim-bullseye

# os dependencies (flags to prevent additional unnecessary stuff)
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config && \
    pip install --no-cache-dir --upgrade pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# requirements
# copy instruction for requirements.txt separate from copy instruction for rest of app
#   if dependencies for app changes (resulting in requirements.txt changingg), 
#       we'd recreate that layer with the new requirements installed in "RUN pip install . . ." layer, and every layer after that
#   but if only app code changes, and no new requirements, we won't have to rebuild the "RUN pip install . . ." layer - usually the most time consuming layer to build

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 8080

CMD ["python3", "server.py"]