import logging
from collections import Counter

from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


# table in database structure
class WordCount(Base):
    __tablename__ = "word_counts"
    word = Column(String, primary_key=True)
    count = Column(Integer, default=0)


# Drop existing tables in database, initialise it anew
def init_db(db_name):
    engine = create_engine(f"sqlite:///{db_name}", echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine


# stores the current chunk's word counts to database - uses raw SQL instead of ORM for performance
def flush_to_db(counter: Counter, engine):
    if not counter:
        return
    stmt = """
        INSERT INTO word_counts(word, count)
        VALUES (:word, :count)
        ON CONFLICT(word) DO UPDATE SET count = count + excluded.count
    """
    try:
        with engine.begin() as conn:
            conn.execute(text(stmt), [{"word": w, "count": c} for w, c in counter.items()])
        counter.clear()
    except Exception as e:
        logging.error(f"Failed to flush to DB: {e}")