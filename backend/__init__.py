"""Backend package initializer for the project.

This file makes the `backend` directory a Python package so test
discovery/imports like `from backend.app.main import app` work when
running pytest or starting the application.
"""

__all__ = ["app"]
