from models.seeion import GetSession
from models.models import User


with GetSession() as session:
    # print(session.query(User))
    # user = session.query(User).filter(User.id==1).one()
    # print(user)
    user: User = User(username='test1', password='123456', ip='127.0.0.1', port=12345)
    print(user)
    session.add(user)
    session.commit()
