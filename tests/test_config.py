from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import FrozenInstanceError
from datetime import date
from pathlib import Path

import pytest
from config import Config


def test_config_uses_manual_run_defaults() -> None:
    config = Config.from_environment({"GITHUB_TOKEN": "secret"}, default_date=date(2026, 7, 17))

    assert config == Config(
        github_token="secret",
        report_date=date(2026, 7, 17),
        repo_limit=100,
        empty_streak_limit=10,
        summarizer_model=None,
        is_ci=False,
        github_output=None,
    )


def test_config_parses_environment_overrides() -> None:
    config = Config.from_environment(
        {
            "GITHUB_TOKEN": "secret",
            "TODAY": "2026-07-16",
            "REPO_LIMIT": " 25 ",
            "EMPTY_REPO_CONSECUTIVE_LIMIT": " 0 ",
            "SUMMARIZER_MODEL": "deepseek/deepseek-chat",
            "GITHUB_ACTIONS": "true",
            "GITHUB_OUTPUT": "/tmp/github-output",
        },
        default_date=date(2026, 7, 17),
    )

    assert config == Config(
        github_token="secret",
        report_date=date(2026, 7, 16),
        repo_limit=25,
        empty_streak_limit=0,
        summarizer_model="deepseek/deepseek-chat",
        is_ci=True,
        github_output=Path("/tmp/github-output"),
    )


def test_config_is_frozen() -> None:
    config = Config.from_environment({"GITHUB_TOKEN": "secret"}, default_date=date(2026, 7, 17))

    with pytest.raises(FrozenInstanceError):
        config.repo_limit = 5  # type: ignore[misc]


def test_config_fails_fast_without_github_token() -> None:
    with pytest.raises(ValueError, match="GITHUB_TOKEN environment variable is required"):
        Config.from_environment({}, default_date=date(2026, 7, 17))


def test_ci_config_fails_fast_without_report_date() -> None:
    with pytest.raises(ValueError, match="TODAY environment variable is required"):
        Config.from_environment(
            {"GITHUB_TOKEN": "secret", "GITHUB_ACTIONS": "true"},
            default_date=date(2026, 7, 17),
        )


def test_imports_do_not_resolve_configuration() -> None:
    src = Path(__file__).parents[1] / "src"
    modules = ", ".join(path.stem for path in src.glob("*.py"))
    environment = {
        "GITHUB_ACTIONS": "true",
        "PATH": os.environ["PATH"],
        "PYTHONPATH": str(src),
    }

    result = subprocess.run(
        [sys.executable, "-c", f"import {modules}"],
        check=False,
        capture_output=True,
        env=environment,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_importing_log_does_not_configure_global_logging() -> None:
    src = Path(__file__).parents[1] / "src"
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import logging; import log; "
                "logger = logging.getLogger('stargazer'); "
                "assert logger.level == logging.NOTSET; assert not logger.handlers"
            ),
        ],
        check=False,
        capture_output=True,
        env={"PATH": os.environ["PATH"], "PYTHONPATH": str(src)},
        text=True,
    )

    assert result.returncode == 0, result.stderr
