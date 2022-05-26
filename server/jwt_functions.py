from server import app, jwt 

from flask import make_response, redirect
from flask_jwt_extended import (jwt_required, 
                                 get_jwt_identity,
                                create_access_token, create_refresh_token, 
                                set_access_cookies, set_refresh_cookies, 
                                unset_jwt_cookies,unset_access_cookies)


def assign_access_refresh_tokens(user_id, url):
    access_token = create_access_token(identity=str(user_id))
    refresh_token = create_refresh_token(identity=str(user_id))
    resp = make_response(redirect(url, 302))
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp

def unset_jwt():
    resp = make_response(redirect('/login', 302))
    unset_jwt_cookies(resp)
    return resp

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # No auth header
    return redirect('/signup', 302)

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    # Invalid Fresh/Non-Fresh Access token in auth header
    resp = make_response(redirect( '/signup'))
    unset_jwt_cookies(resp)
    return resp, 302

@jwt.expired_token_loader
def expired_token_callback(callback):
    # Expired auth header
    resp = make_response(redirect('/token/refresh'))
    unset_access_cookies(resp)
    return resp, 302

@app.route('/token/refresh', methods=['GET'])
@jwt_required(refresh = True)
def refresh():
    # Refreshing expired Access token
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    resp = make_response(redirect( '/', 302))
    set_access_cookies(resp, access_token)
    return resp