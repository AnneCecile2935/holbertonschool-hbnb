from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace(  # Namespace permet de regrouper les routes pr une même entité
    'places',                           # Le nom du Namespace
    description='Place operations'      # Documentation autogénérée de l'API
)
# ----------------------------- modèle de données pour validation à la création
# Sert à valider automatiquement les entrées dans les requêtes

place_model = api.model('Place', {                 # "model" permet de déclarer
    'title': fields.String(                         # "fields.String" = string
        required=True,                              # Champ obligatoire
        description='Title of the place'            # Description
    ),
    'description': fields.String(                   # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Description of the place'      # Description
    ),
    'price': fields.Float(                          # "fields.Float" = Float
        required=True,                              # Champ obligatoire
        description='Price per night'               # Description
    ),
    'latitude': fields.Float(                       # "fields.Float" = Float
        required=True,                              # Champ obligatoire
        description='Latitude coordinate'           # Description
    ),
    'longitude': fields.Float(                      # "fields.Float" = Float
        required=True,                              # Champ obligatoire
        description='Longitude coordinate'          # Description
    ),
    'owner': fields.String(                         # "fields.String" = string
        required=True,                              # Champ obligatoire
        description='Owner user ID'                 # Description
    )
})
# ------------------------- modèle de données pour validation à la modification
place_update_model = api.model('PlaceUpdate', {    # "model" permet de déclarer
    'title': fields.String(                         # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Title of the place'            # Description
    ),
    'description': fields.String(                   # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Description of the place'      # Description
    ),
    'price': fields.Float(                          # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Price per night'               # Description
    ),
    'latitude': fields.Float(                       # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Latitude coordinate'           # Description
    ),
    'longitude': fields.Float(                      # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Longitude coordinate'          # Description
    )
})


# ------------------------------------------ Route POST & GET : /api/v1/places/
@api.route('/')                        # Création d'une route
class PlaceList(Resource):             # Récupération des méthodes par Resource
    @api.expect(place_model, validate=True)          # Vérifie avec place_model
    @api.response(201, 'Place successfully created')                    # OK
    @api.response(400, 'Bad request')                                # NOK
# --------------------------------- Fonction pour enregister une nouvelle place
    def post(self):
        """Register a new place"""
        place_data = api.payload                 # Récupère les données
        owner_id = place_data.get("owner")       # Récupère l'id du champ owner
        owner = facade.get_user(owner_id)    # Récup le user_id par le owner_id
        if not owner:                   # Si le owner n'est pas trouvé = Erreur
            return {'error': 'Owner user not found'}, 404

        try:
            # Vérifie les données et si OK crée une nouvelle place
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner': new_place.owner
            }, 201
        except ValueError as e:               # Utilise les methode de classe
            return {'error': str(e)}, 400     # Return obj error et code status

# ------------------------------------------ Route POST & GET : /api/v1/places/
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Get all places"""
        places = facade.get_all_places()       # Récupération de la liste
        places_list = []                       # Liste vide
        for place in places:                   # Boucle dans le _storage
            places_list.append({               # Ajoute chaque place à la liste
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': place.owner,
            })
        return places_list, 200                # Return la liste


# --------------------------------- Route GET & PUT : /api/v1/places/<place_id>
@api.route('/<place_id>')              # Création d'une route
class PlaceResource(Resource):         # Récupération des méthodes par Resource
    @api.response(200, 'Place details retrieved successfully')  # OK
    @api.response(404, 'Place not found')                       # NOK
    @api.response(404, 'Owner not found')                       # NOK
# -------------------------------- Fonction pour récupérer une place par son id
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)        # Récupère l'id de la place
        if not place:                             # Si pas trouvé = Erreur
            return {'error': 'Place not found'}, 404

        owner = facade.get_user(place.owner)      # Récupère le owner
        if not owner:                             # Si il n'existe pas = Erreur
            return {'error': 'Owner not found'}, 404
        return {                                  # Sinon return la place
            'id': place.id,

            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
            }
        }, 200                                    # Récupération OK

# --------------------------------- Route GET & PUT : /api/v1/places/<place_id>
    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated succesfully')
    @api.response(404, 'Place not found')
# --------------------------------- Fonction pour modifier une place par son id
    def put(self, place_id):
        try:
            place = facade.get_place(place_id)  # Récupère la place par sont id
            if not place:  # Si la place n'est pas trouvée = Erreur
                return {'error': 'Place not found'}, 404
            update_data = api.payload  # Récupère les nouvelles données
            # Vérification que un champ owner est été remplis
            if 'owner' in update_data:
                return {
                    'error': "Modification of 'owner' field is not allowed."
                }, 400
            # Vérifie les nouvelles données et si OK modifie la place
            updated_place = facade.update_place(place_id, update_data)
            return {
                'id': updated_place.id,
                'description': updated_place.description,
                'title': updated_place.title,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
            }, 200
        except ValueError as ve:
            return {'error': str(ve)}, 400
