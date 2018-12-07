# uWSGI daemon
uWSGI daemon (for CentOS 7) returns the current weather in the city to which requested IPv4 address belongs.
Response has json format

## Usage
Insert your own OpenWeather API key into ip2.cfg

## Testing
```
python ./test_ip2w.py
```

## Testing with nginx
Build an image from Dockerfile
```
sudo docker build -t test/uwsgi_test .
```
and run
```
sudo  docker run --rm -p 9008:80 -it --mount src="$(pwd)",target=/test_1,type=bind -w /test_1 test/uwsgi_test:latest /bin/bash -c "./dockerboot.sh; /bin/bash"
```
in a host execute commands, for example:
```
curl http://0.0.0.0:9008/ip2w/8.8.8.8
curl http://0.0.0.0:9008/ip2w/104.76.50.234
```

## Creating an RPM package
Execute commands
```
sudo  docker run --rm -it --mount src="$(pwd)",target=/test_1,type=bind -w /test_1 test/uwsgi_test:latest /bin/bash
./buildrpm.sh ip2w.spec
cp /root/rpm/RPMS/noarch/ip2w-0.0.1-1.noarch.rpm .
```

## Installing RPM package
```
sudo rpm -i ip2w-0.0.1-1.noarch.rpm
sudo systemctl start ip2w
```
configure nginx to proxy to uwsgi, before default server block insert:
```
server {
    listen 80;
        server_name 0.0.0.0;

        location /ip2w/ {
            include uwsgi_params;
            uwsgi_pass unix:/run/uwsgi/ip2w.sock;
        }
    }
```