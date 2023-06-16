import os

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base

connection_string = 'postgresql://test:test@localhost/video_bot_qa'
# connection_string = os.environ['DB_URL']

engine = create_engine(connection_string)
Base = declarative_base()

class RedditSubmission(Base):
    __tablename__ = 'reddit_submissions'

    id = Column(String(20), primary_key=True)
    subreddit = Column(String, nullable=False)
    content_type = Column(String)

# class Production(Base):
#     __tablename__ = 'productions'

#     id = Column(Integer, primary_key=True)

# Create the table in the database
Base.metadata.create_all(engine)