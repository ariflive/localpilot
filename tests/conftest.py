import os
import sys
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import init_db


def pytest_sessionstart(session):
    asyncio.get_event_loop().run_until_complete(init_db())
