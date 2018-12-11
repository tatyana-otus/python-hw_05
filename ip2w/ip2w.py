#!/usr/bin/env python

import logging
import os
import urllib2
import urllib
import urlparse
import json
import re
import ConfigParser
import time

CONFIG_PATH = "/usr/local/etc/ip2w/ip2w.cfg"
LOG_DIR = "/var/log/ip2w"
LOG_NAME = "ip2w.log"

CONFIG = {
    "geo_url": "https://ipinfo.io",

    "weather_url": "https://api.openweathermap.org/data/2.5/weather",
    "weather_appid": ""
}

cfg = CONFIG.copy()
ip4_re = re.compile(r"^\/ip2w\/(\d+\.\d+\.\d+\.\d+)+$")

STATUS_OK = '200 OK'
STATUS_ER = '400 Bad Request'


def set_logger(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s] %(levelname).1s %(message)s',
                            datefmt='%Y.%m.%d %H:%M:%S',
                            filename=os.path.join(dir, LOG_NAME),
                            filemode='w')
    except (IOError, OSError) as e:
        logging.exception("{} doesn't exist".format(dir))


def init(path):
    try:
        if not os.path.isfile(path):
            raise IOError("No {} config file".format(path))
        file_cfg = ConfigParser.SafeConfigParser(CONFIG, allow_no_value=True)
        file_cfg.read(path)
        cfg["geo_url"] = file_cfg.get("API", "geo_url")
        cfg["weather_url"] = file_cfg.get("API", "weather_url")
        cfg["weather_appid"] = file_cfg.get("API", "weather_appid")
        if cfg["weather_appid"] == "":
            raise ValueError("No weather_appid in {} config".format(path))
    except Exception as e:
        logging.exception("init error")


def application(environ, start_response):
    try:
        url = environ["REQUEST_URI"]
        response_body = request_handler(cfg["geo_url"],
                                        cfg["weather_url"],
                                        cfg["weather_appid"],
                                        url)
        status = STATUS_OK
    except Exception as e:
        logging.exception("Error with request: {}".format(url))
        response_body = '{"message": "Error"}\n'
        status = STATUS_ER
    headers = [('Content-Type', 'application/json'),
               ('Content-Length', str(len(response_body)))]
    start_response(status, headers)
    return [response_body]


def get_conn_data(url, timeout=5, reconnect_attempts=10, reconnect_delay=1):
    attempts = reconnect_attempts
    while True:
        try:
            conn = urllib2.urlopen(url, timeout=timeout)
            data = conn.read()
            conn.close()
            return data
        except urllib2.URLError as e:
            time.sleep(reconnect_delay)
            logging.error("Connection error: reconnecting ... ")
            attempts -= 1
            if attempts == 0:
                raise


def get_geo(url, ip_address):
    url = urlparse.urljoin(url, ip_address, "geo")
    logging.info(url)
    data = get_conn_data(url)
    raw_data = json.loads(data)
    coords = tuple(raw_data.get('loc', '').split(','))
    if coords:
        lat, lon = coords[0].encode(), coords[1].encode()
    return lat, lon


def get_weather(url, lat, lon, appid):
    arg = {"lat": lat, "lon": lon, "appid": appid, "units": "metric"}
    url = url + "?" + urllib.urlencode(arg)
    logging.info(url)
    data = get_conn_data(url)
    raw_data = json.loads(data)
    return format_response(raw_data)


def format_response(raw_data):
    res = {"city": raw_data.get("name", ""),
           "temp": raw_data.get("main", {}).get("temp", ""),
           "description": raw_data.get("weather", [dict()])[0].get("description", "")}
    return json.dumps(res) + '\n'


def request_handler(geo_url, weather_url, appid, argument):
    result = ip4_re.match(argument)
    lat, lon = get_geo(geo_url, result.group(1))
    return get_weather(weather_url, lat, lon, appid)


set_logger(LOG_DIR)
init(CONFIG_PATH)
