"""
Production-grade logging configuration for household-geothermal-heating skill.

Implements structured logging with multiple handlers, formatters, and
performance monitoring capabilities.
"""

import logging
import logging.handlers
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from contextlib import contextmanager


class StructuredFormatter(logging.Formatter):
    """JSON-structured formatter for production logging."""

    def __init__(self, timestamp_format: str = "iso8601"):
        super().__init__()
        self.timestamp_format = timestamp_format

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        # Base log entry
        log_entry = {
            "timestamp": self._format_timestamp(record.created),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info) if record.exc_info else None
            }

        # Add custom context from record
        if hasattr(record, 'context'):
            log_entry["context"] = record.context

        # Add skill-specific fields
        if hasattr(record, 'skill_context'):
            log_entry["skill"] = record.skill_context

        return json.dumps(log_entry, default=str, ensure_ascii=False)

    def _format_timestamp(self, created: float) -> str:
        """Format timestamp based on configuration."""
        if self.timestamp_format == "iso8601":
            return datetime.fromtimestamp(created).isoformat()
        elif self.timestamp_format == "unix":
            return str(int(created))
        elif self.timestamp_format == "milliseconds":
            return str(int(created * 1000))
        else:
            return datetime.fromtimestamp(created).strftime(self.timestamp_format)


class SkillLogFilter(logging.Filter):
    """Filter to add skill-specific context to all log records."""

    def __init__(self, skill_name: str = "household-geothermal-heating",
                 skill_version: str = "1.0.0"):
        super().__init__()
        self.skill_name = skill_name
        self.skill_version = skill_version
        self.execution_id: Optional[str] = None

    def set_execution_id(self, execution_id: str):
        """Set the current execution ID."""
        self.execution_id = execution_id

    def filter(self, record: logging.LogRecord) -> bool:
        """Add skill context to log record."""
        record.skill_context = {
            "skill": self.skill_name,
            "version": self.skill_version
        }
        if self.execution_id:
            record.skill_context["execution_id"] = self.execution_id
        return True


class PerformanceLogger:
    """Performance monitoring and metrics logging."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.metrics = {}
        self.start_times = {}

    @contextmanager
    def measure(self, metric_name: str, **context):
        """Context manager for measuring operation duration."""
        start_time = time.time()
        self.start_times[metric_name] = start_time

        try:
            yield
            duration = time.time() - start_time
            self._log_metric(metric_name, duration, "success", context)
        except Exception as e:
            duration = time.time() - start_time
            self._log_metric(metric_name, duration, "error", {**context, "error": str(e)})
            raise

    def _log_metric(self, metric_name: str, duration: float, status: str, context: Dict[str, Any]):
        """Log performance metric."""
        metric_entry = {
            "metric_type": "performance",
            "metric_name": metric_name,
            "duration_seconds": duration,
            "status": status,
            **context
        }
        self.logger.info("Performance metric", extra={"context": metric_entry})

        # Store in metrics
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append({
            "duration": duration,
            "status": status,
            "timestamp": time.time(),
            **context
        })

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics."""
        summary = {}
        for metric_name, measurements in self.metrics.items():
            successful = [m for m in measurements if m['status'] == 'success']
            summary[metric_name] = {
                "count": len(measurements),
                "success_count": len(successful),
                "success_rate": len(successful) / len(measurements) if measurements else 0,
                "avg_duration": sum(m['duration'] for m in measurements) / len(measurements) if measurements else 0,
                "min_duration": min(m['duration'] for m in measurements) if measurements else 0,
                "max_duration": max(m['duration'] for m in measurements) if measurements else 0
            }
        return summary


class SkillLogger:
    """Main logger class for the household-geothermal-heating skill."""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.logger = self._setup_logger()
        self.skill_filter = SkillFilter()
        self.logger.addFilter(self.skill_filter)
        self.performance = PerformanceLogger(self.logger)
        self.execution_id: Optional[str] = None

    def _default_config(self) -> Dict:
        """Default logging configuration."""
        return {
            "level": "INFO",
            "format": "structured",
            "handlers": {
                "console": {
                    "enabled": True,
                    "format": "json",
                    "timestamp_format": "iso8601"
                },
                "file": {
                    "enabled": True,
                    "path": "logs/skill_execution.log",
                    "max_size_mb": 10,
                    "backup_count": 5,
                    "format": "json"
                }
            },
            "events": {
                "log_all_events": False,
                "log_threshold": "INFO",
                "include_context": True,
                "include_error_details": True
            }
        }

    def _setup_logger(self) -> logging.Logger:
        """Set up logger with handlers and formatters."""
        logger = logging.getLogger("household-geothermal-heating")
        logger.setLevel(getattr(logging, self.config["level"]))

        # Clear existing handlers
        logger.handlers.clear()

        # Console handler
        if self.config["handlers"]["console"]["enabled"]:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, self.config["level"]))
            console_formatter = StructuredFormatter(
                self.config["handlers"]["console"]["timestamp_format"]
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

        # File handler
        if self.config["handlers"]["file"]["enabled"]:
            log_path = Path(self.config["handlers"]["file"]["path"])
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.handlers.RotatingFileHandler(
                log_path,
                maxBytes=self.config["handlers"]["file"]["max_size_mb"] * 1024 * 1024,
                backupCount=self.config["handlers"]["file"]["backup_count"]
            )
            file_handler.setLevel(getattr(logging, self.config["level"]))
            file_formatter = StructuredFormatter(
                self.config["handlers"]["file"]["timestamp_format"]
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        return logger

    def set_execution_id(self, execution_id: str):
        """Set execution ID for context."""
        self.execution_id = execution_id
        self.skill_filter.set_execution_id(execution_id)

    def log_event(self, event_type: str, data: Dict[str, Any], level: str = "INFO"):
        """Log a structured event."""
        event_entry = {
            "event_type": event_type,
            "execution_id": self.execution_id,
            **data
        }
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.log(log_level, f"Event: {event_type}", extra={"context": event_entry})

    def log_gate_result(self, gate_name: str, passed: bool, details: Optional[Dict] = None):
        """Log quality gate result."""
        self.log_event(
            "gate.passed" if passed else "gate.failed",
            {
                "gate": gate_name,
                "passed": passed,
                "details": details or {}
            }
        )

    def log_limitation(self, limitation_type: str, level: int, message: str):
        """Log a limitation flag."""
        self.log_event(
            "limitation.flagged",
            {
                "limitation_type": limitation_type,
                "level": level,
                "message": message
            },
            level="WARNING"
        )

    def log_error(self, error: Exception, context: Optional[Dict] = None):
        """Log an error with exception details."""
        error_entry = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            **(context or {})
        }
        self.logger.error("Error occurred", exc_info=error, extra={"context": error_entry})

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary."""
        return self.performance.get_metrics_summary()


# Global logger instance
_global_logger: Optional[SkillLogger] = None


def get_logger(config: Optional[Dict] = None) -> SkillLogger:
    """Get or create the global logger instance."""
    global _global_logger
    if _global_logger is None:
        _global_logger = SkillLogger(config)
    return _global_logger


def setup_logging(config: Optional[Dict] = None):
    """Setup logging with provided configuration."""
    return get_logger(config)


# Convenience functions
def log_event(event_type: str, data: Dict[str, Any], level: str = "INFO"):
    """Log an event using the global logger."""
    get_logger().log_event(event_type, data, level)


def log_gate_result(gate_name: str, passed: bool, details: Optional[Dict] = None):
    """Log a quality gate result using the global logger."""
    get_logger().log_gate_result(gate_name, passed, details)


def log_limitation(limitation_type: str, level: int, message: str):
    """Log a limitation flag using the global logger."""
    get_logger().log_limitation(limitation_type, level, message)


def log_error(error: Exception, context: Optional[Dict] = None):
    """Log an error using the global logger."""
    get_logger().log_error(error, context)


if __name__ == "__main__":
    # Test logging
    logger = get_logger()
    logger.set_execution_id("test-execution-001")

    logger.log_event("skill.invoked", {"query_length": 150})
    logger.log_gate_result("G1", True, {"validation": "passed"})
    logger.log_limitation("source_timeout", 2, "Primary source unavailable")

    with logger.performance.measure("test_operation", operation="test"):
        time.sleep(0.1)

    print("Performance summary:")
    print(json.dumps(logger.get_performance_summary(), indent=2))
