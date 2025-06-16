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
