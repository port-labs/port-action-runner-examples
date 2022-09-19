#!/bin/bash

# Getting token response from API
token=$(curl --location --request POST 'https://api.getport.io/v1/auth/access_token' \
--header 'Content-Type: application/json' \
--data-raw "{
    \"clientId\": \"$PORT_CLIENT_ID\",
    \"clientSecret\": \"$PORT_CLIENT_SECRET\"
}")
# Checking if token in response, outputting check to /dev/null
if echo "$token" | jq --exit-status '.accessToken' >/dev/null; then
    # Extracting Bearer Token from response
    bearer=$(echo "$token" | jq '.accessToken' | sed 's/"//g')
    echo "$bearer"
else
    exit 2
fi
