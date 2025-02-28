#!/usr/bin/env bash
# load-test.sh
# Sends repeated requests to generate traffic for testing.

CLOUDFRONT_DOMAIN="d1234example.cloudfront.net"
ITERATIONS=5
PAGES=("index.html" "about.html" "contact.html")

for ((i=1; i<=ITERATIONS; i++)); do
  for page in "${PAGES[@]}"; do
    echo "Sending request #$i to $page"
    curl -s -o /dev/null "https://$CLOUDFRONT_DOMAIN/$page"
    sleep 1
  done
done

echo "Load test complete."

