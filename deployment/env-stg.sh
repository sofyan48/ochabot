#!/bin/bash
vault kv get -format=json staging/stg-ochabot-gpt-chat-srvc | jq -r '.data.data | to_entries | .[] | "\(.key)=\(.value)"' >> .env