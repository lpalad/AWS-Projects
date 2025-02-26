#!/bin/bash
# Test script for sending sample orders to the API Gateway endpoint

# Check for required argument
if [ -z "$1" ]; then
    echo "Usage: ./test-orders.sh <api-endpoint-url> [number-of-orders]"
    echo "Example: ./test-orders.sh https://example.execute-api.region.amazonaws.com/stage/orders 5"
    exit 1
fi

# Set variables
API_URL="$1"
NUM_REQUESTS=${2:-10}  # Default to 10 requests if not specified

echo "Sending $NUM_REQUESTS test orders to $API_URL"

# Loop to send multiple test orders
for i in $(seq 1 $NUM_REQUESTS); do
  # Generate test order data
  ORDER_ID="test-order-$i-$(date +%s)"
  QUANTITY=$((1 + RANDOM % 10))
  PRICE=$((10 + RANDOM % 90))
  
  echo "Sending order $i: ID=$ORDER_ID, Quantity=$QUANTITY, Price=\$$PRICE"
  
  # Send the request using curl
  curl -s -X POST \
    "$API_URL" \
    -H 'Content-Type: application/json' \
    -d "{
      \"order_id\": \"$ORDER_ID\",
      \"customer_name\": \"Test Customer\",
      \"product\": \"Demo Product\",
      \"quantity\": $QUANTITY,
      \"price\": $PRICE
    }"
  
  echo ""
  
  # Brief pause between requests
  sleep 1
done

echo "All test orders sent successfully."
