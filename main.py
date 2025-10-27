from multiprocessing import freeze_support
import yaml
from uvicorn import run
import ssl

from Card_Name_Platform_Service.app.api import *

if __name__ == "__main__":
    freeze_support()
    with open("config.yaml", "r") as file:
        data = yaml.load(stream=file, Loader=yaml.Loader)

    # CNP Service
    config_CNP_Service = data["CNP_SERVICE"]
    CNP_HOST = config_CNP_Service["CNP_HOST"]
    CNP_PORT = config_CNP_Service["CNP_PORT"]
    SECURE = config_CNP_Service["SECURE"]
    NUM_CPU = config_CNP_Service["NUM_CPU"]

    if SECURE:
        # SSL
        config_SSL = data["SSL"]
        KEY = config_SSL["KEY"]
        CERT = config_SSL["CERT"]
        CA_CERT = config_SSL["CA_CERT"]
        run(app="Card_Name_Platform_Service.app.api:app", host=CNP_HOST, port=CNP_PORT, workers=NUM_CPU, ssl_certfile=CERT, ssl_keyfile=KEY, ssl_ca_certs=CA_CERT) 
    else:
        run(app="Card_Name_Platform_Service.app.api:app", host=CNP_HOST, port=CNP_PORT, workers=NUM_CPU) 