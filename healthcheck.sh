#!/usr/bin/env bash
# Usage: ./healthcheck.sh <url>
# ./healthcheck.sh https://www.google.com

while ! curl \
  --header "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36" \
  --silent \
  --output /dev/null \
  --head \
  --fail \
  --max-time 3 \
  --location ${1}; do
  echo "Healthchecking...${1}"
  sleep 2
done
