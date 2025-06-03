# HBNB Diagramme de packages

```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +Inscription
	+Authentification
	+Find a place
	+Place Review
}
class BusinessLogicLayer {
    +ModelClasses
    +
}
class PersistenceLayer {
    +DatabaseAccess
    +
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```