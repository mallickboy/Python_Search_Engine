#!/bin/bash
# start.sh

# Print environment variables for debug
echo "HOST=$HOST"
echo "PORT=$PORT"
echo "WORKERS=$WORKERS"
echo "TIMEOUT=$TIMEOUT"

# Safe display of secret keys
if [ -n "$PINECONE_KEY" ]; then
  echo "PINECONE_KEY=${PINECONE_KEY:0:4}****"
else
  echo "PINECONE_KEY is not set"
fi

# Start Gunicorn server
exec gunicorn -w "$WORKERS" -k uvicorn.workers.UvicornWorker \
  --bind "$HOST:$PORT" --timeout "$TIMEOUT" app.main:app
