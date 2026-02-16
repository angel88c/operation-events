#!/bin/bash
# ============================================================================
# Generate self-signed SSL certificate for local HTTPS
# ============================================================================
# Usage: bash nginx/generate-cert.sh
# ============================================================================

CERT_DIR="nginx/certs"
mkdir -p "$CERT_DIR"

openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout "$CERT_DIR/selfsigned.key" \
    -out "$CERT_DIR/selfsigned.crt" \
    -subj "/C=MX/ST=Local/L=Local/O=Dev/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,IP:192.168.100.90,IP:127.0.0.1"

echo ""
echo "Certificate generated in $CERT_DIR/"
echo "  - selfsigned.crt"
echo "  - selfsigned.key"
echo ""
echo "NOTE: Update the IP in -addext if your network IP is different."
echo "NOTE: Browsers will show a security warning for self-signed certs — this is expected."
