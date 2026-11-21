# Eye of the Storm — all-in-one image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System dependencies: nmap (portscan), exiftool (metadata), dnsutils (DNS tools)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       nmap libimage-exiftool-perl dnsutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies + spaCy NLP model (cached layer)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm

COPY . .

# Persist reports outside the container:
#   docker run -v "$(pwd)/output:/app/output" ...
VOLUME ["/app/output"]

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
