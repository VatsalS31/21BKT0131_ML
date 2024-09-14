import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base
from models.document_model import Document
from models.user_model import User

# Create a test database engine
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

# Session for testing
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    # Set up the test database and create the tables
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_document(test_db):
    new_doc = Document(title="Test Title", content="Test Content", similarity_score=0.9)
    test_db.add(new_doc)
    test_db.commit()

    # Fetch the document from the database
    doc = test_db.query(Document).filter(Document.title == "Test Title").first()
    assert doc.title == "Test Title"
    assert doc.content == "Test Content"
    assert doc.similarity_score == 0.9

def test_create_user(test_db):
    new_user = User(user_id="test_user", api_calls=1)
    test_db.add(new_user)
    test_db.commit()

    # Fetch the user from the database
    user = test_db.query(User).filter(User.user_id == "test_user").first()
    assert user.user_id == "test_user"
    assert user.api_calls == 1
