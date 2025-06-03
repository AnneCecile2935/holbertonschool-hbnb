# holbertonschool-hbnb

```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +ServiceAPI
    +Class2
}
class BusinessLogicLayer {
    +ModelClasses
    +Class4
}
class PersistenceLayer {
    +DatabaseAccess
    +Class4
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```