import contextlib
from sqlalchemy.orm import Session


@contextlib.contextmanager
def transaction(session: Session):
    if not session.in_transaction():
        with session.begin():
            yield
    else:
        yield
