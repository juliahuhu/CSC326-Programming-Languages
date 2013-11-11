#!/bin/bash
sudo apt-get install git
sudo apt-get install python-pip
sudo apt­get install apache2­utils
sudo apt­get install sysstat
sudo apt­get install unzip
sudo easy_install -U bottle
sudo easy_install beautifulsoup4
sudo easy_install oauth2client
sudo easy_install httplib2
sudo easy_install beaker
sudo easy_install urllib3
git clone https://github.com/vincentleest/CSC326.git
#wget https://google-api-python-client.googlecode.com/files/google-api-python-client-1.2.tar.gz
#wget http://google-api-python-client.googlecode.com/files/google-api-python-client-gae-1.2.zip
yes | tar -xvwzf google-api-python-client-1.2.tar.gz
yes | unzip google-api-python-client-gae-1.2.zip -d CSC326
#mv google-api-python-client-1.2 CSC326
#cd CSC326/google-api-python-client-1.2
sudo pip install --upgrade google-api-python-client
