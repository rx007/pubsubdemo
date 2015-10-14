import logging

class BaseLoggingMixin:
    _logger = None

    @property
    def logger(self):
        if not self._logger:
            FORMAT = '%(asctime)-15s %(message)s'
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)
            self._logger = logging.getLogger()
        return self._logger

        # logging.debug("1ssss")
        
