```mermaid

flowchart TD

classDiagram

BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Review
BaseModel <|-- Amenity

class BaseModel {
  + id : string
  + create_instance : datetime
  + update_instance : datetime

  + __init__()
  + __str__()
  + save()
  + push_to_BDD()
}

class User {
  + name : str
  + surname : str
  + email : str
  - password : str
  + admin : bool

  + __init__()
  + __str__()
  + save()
  + delete()
  + push_to_BDD()
}

class Place {
  # user_id : str
  + title : str
  + description : str
  + price : float
  + latitude : float
  + longitude : float
  + review_ids : list[str]
  + amenity_ids : list[str]

  + create()
  + update()
  + delete()
  + list()
  + getDetails()
}

class Review {
  # user_id : str
  # place_id : str
  + notation : int
  + comments : str
  + place_visited : bool

  + __init__()
  + __str__()
  + delete()
  + save()
  + listed()
  + push_to_BDD()
}

class Amenity {
  # place_id : str
  + name : str
  + description : str

  + __init__()
  + __str__()
  + delete()
  + save()
  + push_to_BDD()
}

User "1" -- "*" Place
User "1" -- "*" Review
Place "1" *--> "*" Review : contains
Place "1" *-- "*" Amenity : contains
```

---
