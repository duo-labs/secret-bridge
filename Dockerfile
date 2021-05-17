FROM python:3-alpine

LABEL maintainer="labs@duo.com"

RUN apk add git make bash grep
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install the various secrets providers
WORKDIR /usr/src/secret-providers

# git-secrets
RUN git clone https://github.com/awslabs/git-secrets.git
WORKDIR /usr/src/secret-providers/git-secrets
RUN make install

# detect-secrets
RUN pip install detect-secrets

# trufflehog
RUN pip install trufflehog


WORKDIR /usr/src/app
COPY . .
RUN addgroup -S secops && adduser -S secops -G secops -s /bin/sh
USER secops
WORKDIR /usr/src/app
ENTRYPOINT ["python", "main.py"]
