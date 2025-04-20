#!/bin/bash

# Create RSA private key
openssl genrsa -out private.pem 2048

# Extract public key from the private key
openssl rsa -in private.pem -pubout -out public.pem

echo "RSA key pair generated (private.pem & public.pem)"
