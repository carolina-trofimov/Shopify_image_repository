
#Shopify Image Repository

### Code challenge for Shopify Internship


Shopify image Repository is a full-stack web application that allows user to upload, view and delete images. The images are hosted on AWS S3.


## Dependencies

* [Postgres](https://www.postgresql.org/download/)
* Python 3.7


## Installing

* ```$ git clone https://github.com/carolina-trofimov/shopify_challenge```

* ```$ virtualenv env ``` -> to create virtual environment

* ```$ source env/bin/activate``` -> activate your virtual environment

* ```$ pip3 install awscli``` -> To install AWS CLI

* ```$ aws configure``` -> To add AWSAccessKeyId and AWSSecretKey

* ```$ createdb image_repository``` -> to create your data base

* ```$ python3 models.py ``` 

* ```$ pip3 install -r requirements.txt ``` -> to install all the libraries needed

## Executing program

* Source and activate your virtual environment

* ```$ python3 server.py ```

## Author:

 **Carolina Trofimov**

[LinkedIn](https://www.linkedin.com/in/carolina-trofimov/)

## Version History 

* 0.1
    * Initial release
