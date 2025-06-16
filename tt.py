from polyfactory import SQLAlchemyFactory
from sqlalchemy.orm import relationship
from my_project import models  # импортируйте ваши модели


class EmployeeFactory(SQLAlchemyFactory[models.Employee]):
    __model__ = models.Employee

    # Укажите значения полей по умолчанию, при необходимости
    username = "test_user"
    roles = ["user"]


class WebinarFactory(SQLAlchemyFactory[models.Webinar]):
    __model__ = models.Webinar

    # Фабрика для создания вебинаров
    event_id = None
    date = "2023-01-01"
    duration = 60
    link = "http://example.com"
    
    @classmethod
    def create(cls, *args, **kwargs):
        event = kwargs.pop('event', None)
        instance = super().create(*args, **kwargs)
        if event:
            instance.event = event
            instance.event_id = event.id
        
        return instance


class EventFactory(SQLAlchemyFactory[models.Event]):
    __model__ = models.Event

    # Параметры для создания событий
    name = "Test Event"
    description = "This is a test event"
    organizers = []

    @classmethod
    def create(cls, *args, **kwargs):
        # Получаем организаторов из kwargs
        organizers = kwargs.pop('organizers', None)
        instance = super().create(*args, **kwargs)

        # Если организаторы переданы, устанавливаем их
        if organizers:
            instance.organizers = organizers

        return instance


# Пример использования
if __name__ == "__main__":
    # Создание организаторов
    org1 = EmployeeFactory.create(username="Organizer One", roles=["admin"])
    org2 = EmployeeFactory.create(username="Organizer Two", roles=["admin"])
    
    # Создание события с контролируемыми организаторами
    event = EventFactory.create(organizers=[org1, org2])
    
    # Создание вебинара, связанного с событием
    webinar = WebinarFactory.create(event=event)
    
    print(event)  # вывод информации о событии
    print(webinar)  # вывод информации о вебинаре
