#!/bin/bash

sudo apt-get -y update

#if you need "unzip" 
sudo apt install unzip 
wget https://chromedriver.storage.googleapis.com/<chromedriver version (ex. 2.31)>/chromedriver_linux64.zip 
unzip chromedriver_linux64.zip -d ~/local/bin/


wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 
sudo dpkg -i google-chrome-stable_current_amd64.deb 
sudo apt update 
sudo apt -f install -y

main(){
    #create virtual environment
    # 36: my virtual environmnet name
    python -m venv 36 && source 36/bin/activate && pip install --upgrade && pip install -r requirements.txt
}



if ! python3.6 --version >/dev/null 2>&1; then
    echo "You have not installed python 3.6 yet."
else
    main
fi
