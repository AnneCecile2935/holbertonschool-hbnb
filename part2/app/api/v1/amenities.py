from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace(  # Namespace permet de regrouper les routes pr une même entité
    'amenities',                        # Le nom du Namespace
    description='Amenity operations'    # Documentation autogénérée de l'API
)
# ------------------------------------------- modèle de données pour validation
# Sert à valider automatiquement les entrées dans les requêtes

amenity_model = api.model('Amenity', {          # "model" permet de déclarer
    'name': fields.String(                      # "fields.String" = string
        required=True,                          # Champ obligatoire
        description='Name of amenity'           # Description
    )
})


# --------------------------------------- Route POST & GET : /api/v1/amenities/
@api.route('/')                 # Création d'une route
class AmenityList(Resource):    # Récupération des méthodes par Resource
    @api.expect(amenity_model, validate=True)      # Vérifie avec amenity_model
    @api.response(201, 'Amenity successfully created')                    # OK
    @api.response(400, 'Invalid input data or name already registered')   # NOK
# ---------------------------------- Fonction pour enregister un nouvel amenity
    def post(self):
        """Register a new amenity"""
        try:
            amenity_data = api.payload                  # Récupère les données
            # Vérifie les données et si OK crée un nouvel amenity
            new_amenity = facade.create_amenity(amenity_data)
            return {                           # Retourne un obj JSON key/value
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201                                                # Création Ok
        except (TypeError, ValueError) as e:  # Utilise les méthodes de classe
            return {'error': str(e)}, 400     # Return obj error et code status

# --------------------------------------- Route POST & GET : /api/v1/amenities/
    @api.response(200, 'List of amenites retrieved successfully')
# ------------------------------ Fonction pour récupérer la liste des amenities
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()       # Récupération de la liste
        amenities_list = []                          # Liste vide
        for amenity in amenities:            # Boucle dans le _storage
            amenities_list.append({          # Ajoute chaque amenity à la liste
                'id': amenity.id,
                'name': amenity.name
            })
        return amenities_list, 200           # Return la liste


# ---------------------------- Route GET & PUT : /api/v1/amenities/<amenity_id>
@api.route('/<amenity_id>')         # Création d'une route
class AmenityResource(Resource):    # Récupération des méthodes par Resource
    @api.response(200, 'Amenity details retrieved successfully')    # OK
    @api.response(404, 'Amenity not found')                         # NOK
# ------------------------------- Fonction pour récupérer un amenity par son id
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)   # Récupère l'id de l'amenity
        if not amenity:                            # Si amenity id pas trouvé
            return {'error': 'Amenity not found'}, 404                 # Erreur
        return {                                   # Sinon retourne l'amenity
            'id': amenity.id,
            'name': amenity.name
        }, 200                                     # Récupération OK

# ---------------------------- Route GET & PUT : /api/v1/amenities/<amenity_id>
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
# -------------------------------- Fonction pour modifier un amenity par son id
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            amenity_data = api.payload             # Récupère nouvelles données
            # Vérifie les nouvelles données et si OK modifie l'amenity
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name
            }, 200                                          # OK
        except ValueError as e:
            # Si le message d'erreur contient 'not found'
            if 'not found' in str(e).lower():
                return {'error': str(e)}, 404               # Return 404
            return {'error': str(e)}, 400
