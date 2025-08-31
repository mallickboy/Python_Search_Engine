FROM python:3.10.18-slim-bookworm

WORKDIR /pysearch

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY start.sh ./start.sh
RUN chmod +x start.sh

EXPOSE 8000

# Optional: caching model
ENV TRANSFORMERS_CACHE=./model_cache
COPY model_cache ./model_cache

CMD ["./start.sh"]
