from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://root:107382@localhost:3306/wangpan")
ModelBase = declarative_base()


class User(ModelBase):

    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(256))
    password = Column(String(256))
    # ip = Column(String(15))
    # port = Column(Integer)

    subfile_path = relationship("SubfilePath")
    file = relationship("File")


class File(ModelBase):

    __tablename__ = "File"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(256))
    size = Column(Float)

    user_id = Column(Integer, ForeignKey("User.id"))
    file_md5_id = Column(String(64), ForeignKey("FileMd5.id"))


class FileMd5(ModelBase):

    __tablename__ = "FileMd5"

    id = Column(String(64), primary_key=True)
    nums = Column(Integer)

    subfile = relationship("Subfile")
    file = relationship("File")


class Subfile(ModelBase):

    __tablename__ = "Subfile"

    id = Column(String(64), primary_key=True)
    num = Column(Integer)

    subfile_path = relationship("SubfilePath")
    file_md5_id = Column(String(64), ForeignKey("FileMd5.id"))


class SubfilePath(ModelBase):

    __tablename__ = "SubfilePath"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(512))

    user_id = Column(Integer, ForeignKey("User.id"))
    subfile_id = Column(String(64), ForeignKey("Subfile.id"))


if __name__ == '__main__':
    ModelBase.metadata.create_all(engine)
