from sqlalchemy.orm import sessionmaker

from .models import engine


class GetSession:

    def __enter__(self):
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        # return True
