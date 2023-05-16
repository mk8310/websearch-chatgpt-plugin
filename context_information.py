import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS


class ContextInformation(object):
    def __init__(self):
        """
        Initialize ContextInformation
        """
        load_dotenv()
        self.__api_key = os.environ.get("GOOGLE_API_KEY")
        self.__cx = os.environ.get("CUSTOM_SEARCH_ENGINE_ID")
        self.__app = Flask(__name__)
        self.__logger = logging.getLogger(__name__)
        self.__logger.level = logging.DEBUG
        CORS(self.__app)

    @property
    def api_key(self):
        """
        Get Google API key
        :return: Google API key
        """
        return self.__api_key

    @property
    def cx(self):
        """
        Get Google Custom Search Engine ID
        :return: Google Custom Search Engine ID
        """
        return self.__cx

    @property
    def app(self):
        """
        Get Flask app
        :return: Flask app
        """
        return self.__app

    @property
    def logger(self):
        """
        Get logger
        :return: logger
        """
        return self.__logger
