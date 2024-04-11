#
# To create a certificate we need a private key and certificate signing request
#
# This script will ask you some questions and output the resulting key and certificate to src/certificate directory
#
CERTIFICATE_DIR=src/certificate

mkdir -p $CERTIFICATE_DIR

# Generate private key
openssl genpkey -out $CERTIFICATE_DIR/private.key -algorithm RSA -pkeyopt rsa_keygen_bits:2048

# Create certificate signing request
openssl req -new -key $CERTIFICATE_DIR/private.key -out $CERTIFICATE_DIR/certificate.csr

# Create a self signed certificate valid for 365 days
openssl x509 -req -days 365 -in $CERTIFICATE_DIR/certificate.csr -signkey $CERTIFICATE_DIR/private.key -out $CERTIFICATE_DIR/certificate.crt

# Output fingerprint
openssl x509 -in $CERTIFICATE_DIR/certificate.crt -noout -fingerprint | sed -e "s/://g" > $CERTIFICATE_DIR/fingerprint.txt

echo "Result is written to $CERTIFICATE_DIR"
