import uuid
from datetime import datetime
from part3.app.extensions import db, bcrypt, jwt
class BaseModel(db.Model):
    """
    BaseModel class  that provides a unique ID, creation and update timestamps,
    and methods to save and update the instance attributes.
    """
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()))
    created_at = db.Column(
        db.DateTime,
        default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    def __init__(self):
        """
        Initialize a new BaseModel instance.

        Attributes:
            id (str): A unique identifier generated using uuid4.
            created_at (datetime): Timestamp when instance was created.
            update_at (datetime): Timestamp when instance was last updated.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.update_at = datetime.now()

    def save(self):
        """
        Update the 'update_at' timestamp with the current datetime.
        """
        self.update_at = datetime.now()

    def update(self, data):
        """
        Update instance attributes with the provided dictionary.

        Args:
            data (dict): Dictionary of attribute names and their new values.

        Raises:
            AttributeError: If any key in data does not correspond to an existing attribute.
        """
        for key, value in data.items():
            if not hasattr(self, key):
                raise AttributeError(f"{key} is not valid attribute")
            setattr(self, key, value)
        self.save()
