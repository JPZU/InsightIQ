# US22:Database connection
from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from database.models.user import User
from database.session import SessionLocal


@pytest.fixture(scope="module")
def db_session():
    """Fixture to provide a database session for testing."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Aceptance criteria #1


def test_orm_write_and_read(db_session: Session):
    """Test that ORM correctly writes and reads from the database."""

    # Step 1: Write Operation - Create a new user
    new_user = User(
        name="testuser",
        email="test@example.com",
        password="hashedpassword",
        role="user",
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    # Step 2: Read Operation - Retrieve user by ID
    retrieved_user = db_session.query(User).filter_by(id=new_user.id).first()

    # Step 3: Assertions - Verify data integrity
    assert retrieved_user is not None, "User was not retrieved from the database."
    assert retrieved_user.name == "testuser", "Username does not match."
    assert retrieved_user.email == "test@example.com", "Email does not match."
    assert retrieved_user.role == "user", "Role does not match."
    assert retrieved_user.password == "hashedpassword", "Password does not match."
    assert isinstance(retrieved_user.createdAt, datetime), "CreatedAt is not a datetime object."
    assert isinstance(retrieved_user.updatedAt, datetime), "UpdatedAt is not a datetime object."

    # Step 4: Cleanup - Delete the created user
    db_session.delete(retrieved_user)
    db_session.commit()

    # Verify that the user has been deleted
    deleted_user = db_session.query(User).filter_by(id=new_user.id).first()
    assert deleted_user is None, "User was not deleted from the database."
