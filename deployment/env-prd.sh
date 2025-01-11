#!/bin/bash
vault kv get -format=json production/prd-ochabot-gpt-chat-srvc | jq -r '.data.data | to_entries | .[] | "\(.key)=\(.value)"' >> .env