from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_security import current_user, login_user
from models import User, OAuth
from db import db
from sqlalchemy.orm.exc import NoResultFound

blueprint = make_github_blueprint(scope='user:email')

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def github_logged_in(blueprint, token):
    if not token:
        print("Failed to log in.")
        return False

    resp = github.get("/user")
    print(resp)
    info = resp.json()
    print(info)
    if not resp.ok:
        print("Failed to fetch user info.")
        return False

    print('Login OK')

    github_login = info['login']
    github_id = str(info['id'])
    github_name = info['name']

    emails_resp = github.get('/user/emails')
    if not emails_resp.ok:
        print("Failed to fetch user emails.")
        return False
    print(emails_resp)
    emails = emails_resp.json()
    print(emails)
    primary_emails = list(filter(lambda x: x['primary'], emails))
    print(primary_emails)
    primary_email = primary_emails[0]['email']
    print(primary_email)

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=github_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=github_id, token=token)

    if oauth.user:
        login_user(oauth.user)
        print("Successfully signed into existing account")

    else:
        # Create a new local user account for this user
        user = User(email=primary_email, active=True)
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        print("Successfully signed in to new account")

    
    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def google_error(blueprint, message, response):
    msg = "OAuth error from {name}! message={message} response={response}".format(
        name=blueprint.name, message=message, response=response
    )
    print(msg)
