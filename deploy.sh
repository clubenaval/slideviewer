#Oracle linux
systemctl stop firewalld.service
yum install -y python
pip3 install flask
python3 app.py

#Alpine Linuz
apk add python3
apk add python3 py3-pip
apk add python3 py3-flask
