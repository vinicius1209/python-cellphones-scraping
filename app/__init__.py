from flask import Flask
from config import Config

phone_scraping = Flask(__name__)
phone_scraping.config.from_object(Config)

from app import routes

if __name__ == "__main__":
    phone_scraping.run(host='0.0.0.0', debug=False, port=5000)

