from contextlib import contextmanager

from typing import Generator, List, Any
from datetime import datetime
from pytz import timezone, UTC
import logging

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from . import engine

session_maker = sessionmaker(engine)

def now() -> int:
    """Get the current epoch/unix time."""
    return epoch(datetime.now(tz=UTC))


def epoch(t: datetime) -> int:
    """Convert a :class:`.datetime` to UNIX time."""
    delta = t - datetime.fromtimestamp(0, tz=UTC)
    return int(round((delta).total_seconds()))


def from_epoch(t: int) -> datetime:
    """Get a :class:`datetime` from an UNIX timestamp."""
    return datetime.fromtimestamp(t, tz=UTC)


@contextmanager
def transaction() -> Generator[Session, None, None]:
    """Context manager for database transaction."""
    try:    
        session = session_maker()

        yield session
        # The caller may have explicitly committed already, in order to
        # implement exception handling logic. We only want to commit here if
        # there is anything remaining that is not flushed.
        if session.new or session.dirty or session.deleted:
            session.commit()
    except Exception as e:
        logging.warn(f'{now()}: Commit failed, rolling back: {str(e)}')
        session.rollback()
        raise