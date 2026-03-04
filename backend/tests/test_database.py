"""
Test Database Connection and Operations
"""

import pytest
from sqlalchemy.orm import Session


def test_db_connection(db_session: Session):
    """
    Test database connection is working
    """
    result = db_session.execute("SELECT 1").scalar()
    assert result == 1


def test_db_session_rollback(db_session: Session):
    """
    Test database session rollback works correctly
    """
    # This test verifies that the session can be rolled back
    # without errors (important for test isolation)
    db_session.rollback()
    assert True
