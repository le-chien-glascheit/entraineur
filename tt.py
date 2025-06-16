from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from polifactory import Factory, List, Lazy, Seed

Base = declarative_base()

# Определяем модели
class Parent(Base):
    __tablename__ = 'parents'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'children'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('parents.id'))
    parent = relationship("Parent", back_populates="children")

# Создаем фабрики
class ParentFactory(Factory):
    class Meta:
        model = Parent

    id = Lazy(lambda: Seed(1, 1))
    name = List(["Parent 1", "Parent 2", "Parent 3"])

class ChildFactory(Factory):
    class Meta:
        model = Child

    id = Lazy(lambda: Seed(1, 1))
    name = List(["Child A", "Child B", "Child C"])

    # Можно переопределить метод для кастомизации
    @classmethod
    def create(cls, **kwargs):
        parent = kwargs.pop('parent', None)
        child = super().create(**kwargs)
        if parent:
            child.parent = parent
        return child

# Пример использования
if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Создаем родителя и детей с использованием кастомной фабрики
    parent = ParentFactory()
    session.add(parent)
    session.commit()

    # Создание детей с заданным родителем
    child1 = ChildFactory(parent=parent)
    child2 = ChildFactory(parent=parent)

    session.add(child1)
    session.add(child2)
    session.commit()

    # Проверка результата
    print(f"Parent: {parent.name}, Children: {[child.name for child in parent.children]}")



from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from polifactory import Factory, LazyAttribute, Sequence

Base = declarative_base()

# Определим модели

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship('Post', back_populates='user')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='posts')

# Создаем фабрики

class UserFactory(Factory):
    class Meta:
        model = User
    
    id = Sequence(int)
    name = Sequence(lambda n: f'User {n}')

class PostFactory(Factory):
    class Meta:
        model = Post
    
    id = Sequence(int)
    title = Sequence(lambda n: f'Post {n}')
    
    # Устанавливаем пользователя вручную
    user = LazyAttribute(lambda obj: UserFactory())

# Пример использования:

# Создаем движок и сессию
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Используем фабрики для создания объектов
user = UserFactory.create()
posts = PostFactory.create_batch(5, user=user)

# Добавляем пользователя и посты в сессию
session.add(user)
session.add_all(posts)
session.commit()

# Проверяем данные
for post in session.query(Post).all():
    print(f"Post ID: {post.id}, Title: '{post.title}', User: '{post.user.name}'")

___________________________________

from polyfactory.factories import Factory, AbstractFactory
from polyfactory import Field

class PostFactory(Factory):
    __model__ = Post
    title = Field(factory=lambda: "Sample Post Title")

class UserFactory(AbstractFactory):
    __model__ = User

    username = Field(factory=lambda: "user_{0}".format(random.randint(1, 1000)))
    
    # Кастомизируем метод
    def create_with_posts(self, count: int = 3):
        user = self.build()
        user.posts = PostFactory.create_batch(count, user=user)
        return user

