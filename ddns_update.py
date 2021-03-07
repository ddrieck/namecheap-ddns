import socket
import requests
import configparser
import logging
from datetime import datetime

logging.basicConfig(filename="log.txt", level=logging.INFO)
logfile = "log.txt"

def remote_ip(domain):
    ip = socket.gethostbyname(domain)
    return ip

def local_ip():
    response = requests.get('https://icanhazip.com')
    ip = response.text.strip()
    return ip

def set_ip(domain,host,password,local_ip):
    set_ip = requests.get('https://dynamicdns.park-your-domain.com/update?host=%s&domain=%s&password=%s&ip=%s' % (host, domain, password, local_ip))
    return set_ip

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    domain = config['DEFAULT']['Domain']
    ddns_password = config['DEFAULT']['Password']

    remote = remote_ip(domain)
    local = local_ip()

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    logging.info("\n==== BEGINNING CHECK AT: %s ====" % (dt_string))
    if remote != local:
        for section in config.sections():
            set_ip(domain, config[section]['Host'], ddns_password, local)
            logging.info("\nLocal IP: %s Remote IP: %s \nChanged DNS address for %s." % (local, remote, config[section]['Host']))
    else:
        logging.info("\nLocal IP: %s Remote IP: %s IPs match. No changes." % (local, remote))

if __name__ == '__main__':
    main()

