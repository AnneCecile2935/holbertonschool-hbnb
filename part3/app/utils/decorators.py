from functools import wraps

def handle_errors(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            if 'not found' in str(e).lower():
                return {'error': str(e)}, 404
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Unexpected error: {str(e)}'}, 400
    return decorated
