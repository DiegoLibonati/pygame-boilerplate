import logging
import sys

import pytest

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    @pytest.mark.unit
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger()
        assert isinstance(logger, logging.Logger)

    @pytest.mark.unit
    def test_default_name(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "pygame-boilerplate"

    @pytest.mark.unit
    def test_custom_name(self) -> None:
        logger: logging.Logger = setup_logger("my-custom-logger")
        assert logger.name == "my-custom-logger"

    @pytest.mark.unit
    def test_level_is_debug(self) -> None:
        logger: logging.Logger = setup_logger("logger-level-test")
        assert logger.level == logging.DEBUG

    @pytest.mark.unit
    def test_has_one_handler(self) -> None:
        logger: logging.Logger = setup_logger("logger-handler-count-test")
        assert len(logger.handlers) == 1

    @pytest.mark.unit
    def test_handler_is_stream_handler(self) -> None:
        logger: logging.Logger = setup_logger("logger-stream-test")
        assert isinstance(logger.handlers[0], logging.StreamHandler)

    @pytest.mark.unit
    def test_handler_uses_stdout(self) -> None:
        logger: logging.Logger = setup_logger("logger-stdout-test")
        handler: logging.StreamHandler = logger.handlers[0]
        assert handler.stream is sys.stdout

    @pytest.mark.unit
    def test_no_duplicate_handlers_on_repeated_call(self) -> None:
        logger: logging.Logger = setup_logger("logger-no-dup-test")
        setup_logger("logger-no-dup-test")
        assert len(logger.handlers) == 1

    @pytest.mark.unit
    def test_handler_has_formatter(self) -> None:
        logger: logging.Logger = setup_logger("logger-formatter-test")
        assert logger.handlers[0].formatter is not None
