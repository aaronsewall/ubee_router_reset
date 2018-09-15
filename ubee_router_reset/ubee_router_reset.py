"""Continually checks internet is up and reset if it's not."""
from configparser import ConfigParser
from random import randint
from socket import gethostbyname, create_connection, error
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def is_connected(hostname: str):
    """Wait between 30 to 90 seconds, then check if internet is connected."""
    # sleep 30 to 90 seconds
    sleep(randint(30, 90))  # nosec
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        create_connection((host, 80), 2)
        return True
    except error:
        pass
    return False


def reset_modem_router(password: str,
                       username: str = 'admin',
                       url: str = '192.168.0.1',
                       backup_config: str = 'backupsettings.conf',
                       headless: bool = True,):
    """Reset Ubee modem router using selenium."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    address = "http://{}:{}@{}/htdocs/rg_mgt_config.php".format(username, password, url)
    driver.get(address)
    assert "Ubee" in driver.title  # nosec
    elem = driver.find_element_by_id("ID_MGT_CONFIG_IMPORTFILE")
    elem.send_keys(backup_config)
    restore_button = driver.find_element_by_id("ID_MGT_CONFIG_RESTORE")
    restore_button.click()
    driver.close()


if __name__ == '__main__':
    config = ConfigParser()
    config.read('myconfig.yml')
    c = config['DEFAULT']
    RETRY = int(c['RETRY'])
    while True:
        while is_connected(c['TEST_URL']):
            RETRY = int(c['RETRY'])
        else:
            RETRY -= 1
            if RETRY == 0:
                print("Internet down! Resetting Ubee modem router...")
                reset_modem_router(username=c['USERNAME'], password=c['PASSWORD'],
                                   url=c['URL'], backup_config=c['BACKUP_CONFIG'])
            break
