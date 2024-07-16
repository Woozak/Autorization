# Issue RSA private-public key pair

```shell
# Generate RSA private key
openssl genrsa -out private.pem 2048
```

```shell
# Generate RSA public key from the private key
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```