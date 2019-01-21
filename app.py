import datetime
import logging
import os
import pathlib

import aiohttp.web
from jose import jwt, jwk


log = logging.getLogger('mapkit_tokenserver')


routes = aiohttp.web.RouteTableDef()


def create_token(key_id, team_id, key, origin=None, expiration=None):
    now = datetime.datetime.utcnow()
    headers = {'kid': key_id}
    claims = {'iat': now, 'iss': team_id}
    if origin is not None:
        claims['origin'] = origin
    if expiration is not None:
        claims['exp'] = now + expiration
    token = jwt.encode(claims, key, algorithm='ES256', headers=headers)
    log.debug("Created token %s with claims %s", token, claims)
    return aiohttp.web.Response(text=token)


@routes.view('/mapkit_token', name='generate_token')
def new_token(request):
    token = create_token(**request.app['config'])
    return token


def read_config():
    fileable_key_names = {
        'MAPKIT_TOKEN_EXPIRATION': 'expiration',
        'MAPKIT_TEAM_ID': 'team_id',
        'MAPKIT_KEY_ID': 'key_id',
        'MAPKIT_TOKEN_ORIGIN': 'origin',
    }
    config = {}
    for env_key, config_key in fileable_key_names.items():
        if env_key in os.environ:
            config[config_key] = os.environ[env_key]
        else:
            file_key = '{}_FILE'.format(env_key)
            if file_key in os.environ:
                value_path = pathlib.Path(os.environ[file_key])
                try:
                    config[config_key] = value_path.read_text()
                except FileNotFoundError as e:
                    log.exception(
                        "Config file not found at '%s' for %s",
                        os.environ[file_key],
                        file_key,
                    )
                except Exception as e:
                    log.exception(
                        "Unable to read file at '%s' for config value %s",
                        os.environ[file_key],
                        file_key,
                    )
    # Convert the input to a timedelta
    if 'expiration' in config:
        seconds = int(config['expiration'])
        config['expiration'] = datetime.timedelta(seconds=seconds)
    try:
        key_path = os.environ['MAPKIT_KEY_FILE']
        key_data = pathlib.Path(key_path).read_text()
        # Test that the key is able to be read and parsed
        config['key'] = jwk.construct(key_data, 'ES256').to_dict()
    except Exception as e:
        log.exception("Unable to create private key.")
        raise
    assert 'team_id' in config
    assert 'key_id' in config
    assert 'key' in config
    return config


def create_app(args):
    app = aiohttp.web.Application()
    app.add_routes(routes)
    app['config'] = read_config()
    return app
