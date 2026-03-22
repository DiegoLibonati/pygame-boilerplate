import logging

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        logger = setup_logger("test-logger")

        assert isinstance(logger, logging.Logger)

    def test_logger_has_correct_name(self) -> None:
        logger = setup_logger("my-app-logger")

        assert logger.name == "my-app-logger"

    def test_logger_uses_default_name(self) -> None:
        logger = setup_logger()

        assert logger.name == "pygame-app"

    def test_logger_has_debug_level(self) -> None:
        logger = setup_logger("debug-test-logger")

        assert logger.level == logging.DEBUG

    def test_logger_has_handler(self) -> None:
        logger = setup_logger("handler-test-logger")

        assert len(logger.handlers) >= 1

    def test_logger_does_not_duplicate_handlers(self) -> None:
        logger_name = "duplicate-test-logger"

        setup_logger(logger_name)
        setup_logger(logger_name)
        logger = setup_logger(logger_name)

        assert len(logger.handlers) == 1

    def test_same_name_returns_same_logger(self) -> None:
        logger1 = setup_logger("same-name-logger")
        logger2 = setup_logger("same-name-logger")

        assert logger1 is logger2

    def test_different_names_return_different_loggers(self) -> None:
        logger1 = setup_logger("logger-a")
        logger2 = setup_logger("logger-b")

        assert logger1 is not logger2
