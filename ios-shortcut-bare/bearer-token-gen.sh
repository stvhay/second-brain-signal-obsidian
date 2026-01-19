#!/bin/bash
# Generate a random bearer token

printf "%s\n" "$(openssl rand -base64 32 | tr -d '/+=' | cut -c1-40)"

