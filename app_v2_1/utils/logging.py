from __future__ import annotations

from typing import Literal

LogMode = Literal["silent", "normal", "verbose"] | None


def should_log(log_mode: LogMode, level: int) -> bool:
    if log_mode in (None, "normal"):
        return level <= 1
    if log_mode == "verbose":
        return True
    return False


def indent(message: str, level: int) -> str:
    return f"{' ' * level}{message}"


def log(log_mode: LogMode, message: str, *, level: int = 1) -> None:
    if should_log(log_mode, level):
        print(message)
