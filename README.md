# Introduction 
This repository contains sample code to authenticate and authorize an external client application to connect to a
RabbitMQ message broker using an JWT toke aquired from a Microsoft Entra ID tenant using the Microsoft MSAL Python
librabry

# Getting Started
Firstly a private key and a certificate to authenticate with Microsoft Entra ID must be created. This certificate must be uploaded to the Microsoft Entra ID. 

## Create certificate
To generate the private key and certificate run the script 
generate_certificate.sh and answer the questions. The resulting certificate and private key will be saved to the src/certficate directory

```shell
./generate_certificate.sh
```

## Running the code
Configuration is done in the config.yaml file. See this file for a description of the values required. Obtain the required values from an admin of the Microsoft Entra ID tenant.

To install requirements run the following command:

```shell
pip install -r requirements.txt
```

To run the script and connect to RabbitMQ cd to the src directory and run the command

```shell
python main.py
```