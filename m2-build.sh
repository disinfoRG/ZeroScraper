CHROMEDRIVER_URL=https://chromedriver.storage.googleapis.com/chromedriver_linux64.zip

apt-get install -y libnss3-dev
if [ ! -x /usr/local/bin/chromedriver ]; then
  curl -O ${CHROMEDRIVER_URL}
  unzip -o chromedriver_linux64.zip
  mv chromedriver /usr/local/bin
  chmod 700 /usr/local/bin/chromedriver
fi
pip3 install pipenv && pipenv install --system
