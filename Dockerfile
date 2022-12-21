FROM python:3.9
WORKDIR /home
COPY . /home
RUN apt-get update && \
      apt-get -y install sudo
RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
RUN sudo apt-get install unzip
RUN unzip chromedriver_linux64.zip
RUN apt-get install chromium -y
# 安裝指定在 requirements.txt 的 python 套件
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8080
# Define environment variable
CMD ["python3", "main.py"]
