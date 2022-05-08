from flask_dance.contrib.github import make_github_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error


blueprint = make_github_blueprint()

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def github_logged_in(blueprint, token):
    if not token:
        print("Failed to log in.")
        return False

    resp = blueprint.session.get("/oauth2/v1/userinfo")
    print(resp)
    if not resp.ok:
        print("Failed to fetch user info.")
        return False

    print('Login OK')
    info = resp.json()
    print(info)
    
    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def google_error(blueprint, message, response):
    msg = "OAuth error from {name}! message={message} response={response}".format(
        name=blueprint.name, message=message, response=response
    )
    print(msg)
