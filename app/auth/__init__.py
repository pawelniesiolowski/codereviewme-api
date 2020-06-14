from urllib.request import urlopen
from app.auth.error import AuthError
from flask import request
from jose import jwt


def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'code': 401,
            'message': 'Authorization header missing'
        }, 401)

    auth_header_parts = auth_header.split()
    if len(auth_header_parts) != 2 or auth_header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 401,
            'message': 'Malformed authorization header'
        }, 401)
    return auth_header_parts[1]


def check_permissions(permission, payload):
    """
    Parameters:
    permission: string permission (i.e. 'post:create_technology')
    payload: decoded jwt payload

    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 401,
            'message': 'Permissions not included in JWT'
        }, 401)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 401,
            'message': 'Client don\'t have required permission'
        }, 401)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(
        f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/jwks.json'
    )
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 401,
            'message': 'Authorization header malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if not rsa_key:
        raise AuthError({
            'code': 401,
            'message': 'Unable to find the appropriate authentication header'
        }, 401)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=app.config["ALGORITHMS"],
            audience=app.config["API_AUDIENCE"],
            issuer='https://' + app.config["AUTH0_DOMAIN"] + '/'
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 401,
            'message': 'Token expired'
        }, 401)

    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 401,
            'message': 'Incorrect claims'
        }, 401)
    except Exception:
        raise AuthError({
            'code': 401,
            'message': 'Unable to parse authentication token'
        }, 401)
