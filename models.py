
from sqlalchemy import Column,String,Integer,DateTime,func,ForeignKey,Table, null
from sqlalchemy.orm import relationship
from database import Base


role_manager = Table(
    "Role_Manager",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False, primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), nullable=False, primary_key=True)
)

followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id',Integer,ForeignKey('user.id')),
    Column('followed_id',Integer,ForeignKey('user.id')),
)  

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(16),unique=True,nullable=False,comment='name')
    email = Column(String(100),nullable=True,comment="username")
    password = Column(String(50),unique=False,nullable=False,comment='password')
    roles = Column(String(10),nullable=True,comment="roles",default="User")
    birthday = Column(DateTime,nullable=True)
    school_id = Column(String(9),nullable=True,unique=True,comment="10XACX0XX")
    school_grade = Column(String(3),nullable=True,comment="互動X")
    profile_img = Column(String(100),nullable=True)

    roles = relationship('Role',secondary=role_manager,back_populates='users')
    works = relationship('Work',back_populates='owner')

    follower = relationship(
        'User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = ('faned_users'),
    )

    created_at = Column(DateTime,server_default=func.now(),comment="創建時間")
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now() ,comment="更新時間")


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer,nullable=False, primary_key=True,autoincrement=True)
    name = Column(String(10),nullable=False,comment="Role_Name")

    users = relationship('User',secondary=role_manager,back_populates='roles')


class Work(Base):
    __tablename__ = 'work'

    id = Column(Integer,nullable = False,primary_key=True,autoincrement=True)
    name = Column(String(16),nullable=False,unique=False)
    owner_id = Column(ForeignKey("user.id"))
    owner = relationship('User',back_populates='works')



    saved_at = Column(String(20))
    created_at = Column(DateTime,server_default=func.now(),comment="創建時間")
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now() ,comment="更新時間")