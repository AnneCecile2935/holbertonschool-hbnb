"""
Definition of a generic repository interface and an in-memory implementation.

This module introduces the Repository design pattern,
used to abstract CRUD operations (Create, Read, Update, Delete)
on business objects.

Classes:
- Repository (ABC):
    Abstract interface defining the basic operations
    any repository must implement.
    Abstract methods:
    - add(obj): adds an object to the repository.
    - get(obj_id): retrieves an object by its ID.
    - get_all(): returns all stored objects.
    - update(obj_id, data): updates an existing object with new data.
    - delete(obj_id): removes an object from the repository.
    - get_by_attribute(attr_name, attr_value): retrieves an object
    based on a specific attribute.

- InMemoryRepository:
    Concrete implementation of the Repository interface,
    using a dictionary for temporary in-memory storage.
    Mainly used for testing or lightweight prototypes without a database.
"""
from abc import ABC, abstractmethod
# from app.models import User, Place, Review, Amenity


class Repository(ABC):
    """
    Abstract interface for managing business objects in a generic repository.

    Defines the base operations to be implemented by
    any concrete repository class.
    """
    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository.

        Parameter:
        - obj: The object to be added.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by its unique identifier.

        Parameter:
        - obj_id: The unique ID of the object.

        Returns:
        - The matching object, or None if not found.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects stored in the repository.

        Returns:
        - A list of all objects.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an existing object with new data.

        Parameters:
        - obj_id: The unique ID of the object to update.
        - data: A dictionary containing the updated attributes.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Remove an object from the repository.

        Parameter:
        - obj_id: The unique ID of the object to delete.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute and its value.

        Parameters:
        - attr_name: Name of the attribute to filter on.
        - attr_value: Expected value of the attribute.

        Returns:
        - The matching object, or None if not found.
        """
        pass


class InMemoryRepository(Repository):
    """
    Concrete implementation of the Repository interface
    using in-memory storage.

    Useful for testing or when no persistent database is required.
    """
    def __init__(self):
        """
        Initialize the internal dictionary used to store objects.

        Keys are object IDs; values are the objects themselves.
        """
        self._storage = {}

    def add(self, obj):
        """
        Add an object to the repository.

        Parameter:
        - obj: The object to store. Must have an `id` attribute.
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Parameter:
        - obj_id: The object's identifier.

        Returns:
        - The matching object, or None.
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Retrieve all objects currently in the repository.

        Returns:
        - A list of all stored objects.
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an object with new data.

        Parameters:
        - obj_id: The unique ID of the object to update.
        - data: A dictionary of new attributes.

        Note:
        - The object must implement an `update()` method.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Delete an object from the repository by its ID.

        Parameter:
        - obj_id: The object's identifier.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Search for the first object with a given attribute and value.

        Parameters:
        - attr_name: The name of the attribute to match.
        - attr_value: The expected value of the attribute.

        Returns:
        - The matching object, or None if not found.
        """
        return next(
            (
                obj for obj in self._storage.values()
                if getattr(obj, attr_name) == attr_value
            ),
            None
        )

    def clear(self):
        """Clear all data from the in-memory storage."""
        self._storage.clear()


class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy-backed implementation of the Repository interface.

    Provides persistence using SQLAlchemy's ORM system.

    Attributes:
    - model: The SQLAlchemy model class managed by the repository.
    """
    def __init__(self, model):
        """
        Initialize the repository with a specific SQLAlchemy model.

        Parameter:
        - model: The SQLAlchemy model class to operate on.
        """
        self.model = model

    def add(self, obj):
        """
        Add an object to the database.

        Parameter:
        - obj: The SQLAlchemy model instance to add.
        """
        from app import db
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Parameter:
        - obj_id: The primary key of the object.

        Returns:
        - The object if found, else None.
        """
        return self.model.query.get(obj_id)

    def get_all(self):
        """
        Retrieve all objects from the database.

        Returns:
        - A list of all objects.
        """
        return self.model.query.all()

    def update(self, obj_id, data):
        """
        Update an existing object in the database.

        Parameters:
        - obj_id: The ID of the object to update.
        - data: A dictionary of attribute names and new values.
        """
        from app import db
        obj = self.get(obj_id)
        if not obj:
            raise ValueError(f"Object with ID '{obj_id} not found")

        for key, value in data.items():
            setattr(obj, key, value)
        db.session.commit()

    def delete(self, obj_id):
        """
        Delete an object from the database.

        Parameter:
        - obj_id: The ID of the object to delete.
        """
        from app import db
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve the first object where the given attribute matches the value.

        Parameters:
        - attr_name: The model attribute to filter on.
        - attr_value: The value to match.

        Returns:
        - The matching object, or None if no match is found.
        """
        return self.model.query.filter(
            getattr(self.model, attr_name) == attr_value
            ).first()
