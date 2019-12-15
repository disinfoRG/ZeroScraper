apt-get install -y libnss3-dev
if [ ! -x /usr/local/bin/chromedriver ]; then
  curl -O https://chromedriver.storage.googleapis.co77.0.3865.40/chromedriver_linux64.zip
  unzip -o chromedriver_linux64.zip
  mv chromedriver /usr/local/bin
  chmod 700 /usr/local/bin/chromedriver
fi
pip3 install pipenv && pipenv install --system
