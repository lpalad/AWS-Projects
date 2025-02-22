# API Gateway Documentation

## REST API Configuration

### 1. Create API
```bash
# Create the REST API
aws apigateway create-rest-api \
    --name "ANZ-poc-api" \
    --description "API for ANZ PoC mobile access"

# Note: Actual API ID and resource IDs will be different in your implementation
export API_ID="YOUR_API_ID"
export ROOT_RESOURCE_ID="YOUR_ROOT_RESOURCE_ID"


2. Create Resource and Method
# Create /readings resource
aws apigateway create-resource \
    --rest-api-id $API_ID \
    --parent-id $ROOT_RESOURCE_ID \
    --path-part "readings"

# Create GET method
aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id "YOUR_RESOURCE_ID" \
    --http-method GET \
    --authorization-type NONE

3. Lambda Integration
bash
aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id "YOUR_RESOURCE_ID" \
    --http-method GET \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri arn:aws:apigateway:REGION:lambda:path/2015-03-31/functions/YOUR_LAMBDA_ARN/invocations

4. CORS Configuration
bash
aws apigateway put-method-response \
    --rest-api-id $API_ID \
    --resource-id "YOUR_RESOURCE_ID" \
    --http-method GET \
    --status-code 200 \
    --response-parameters "method.response.header.Access-Control-Allow-Origin=false"

5. Deploy API
bash
aws apigateway create-deployment \
    --rest-api-id $API_ID \
    --stage-name prod



API Usage Example
Endpoint Structure
https://YOUR_API_ID.execute-api.REGION.amazonaws.com/prod/readings



Sample Web Integration
html
<!DOCTYPE html>
<html>
<head>
    <title>ANZ Sensor Data</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
    </style>
</head>
<body>
    <h1>ANZ Sensor Readings</h1>
    <div id="data-container"></div>

    <script>
        function fetchData() {
            fetch('YOUR_API_ENDPOINT')
                .then(response => response.json())
                .then(data => {
                    // Process and display data
                    // Implementation details here
                })
                .catch(error => console.error('Error:', error));
        }

        // Fetch data every 15 seconds
        setInterval(fetchData, 15000);
    </script>
</body>
</html>


Security Considerations
API endpoint access control
CORS configuration
Rate limiting considerations
API key implementation (optional)
IAM role permissions

Best Practices
Monitor API usage
Implement error handling
Consider caching strategies
Regular security reviews
Performance optimization

Troubleshooting
CORS issues
Lambda integration errors
Authorization problems
Rate limit exceeded
