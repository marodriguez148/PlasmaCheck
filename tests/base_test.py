from utils.logger import get_logger

class BaseTest:
    def setup_method(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

    def teardown_method(self) -> None:
        pass