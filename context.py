from flask_authnz import FlaskAuthnz, MongoDBRoles, UserGroups

__author__ = 'mshankar@slac.stanford.edu'

# Application context.
app = None

MONGODB_HOSTS=os.environ.get("MONGODB_HOSTS", None)
if not MONGODB_URL:
    MONGODB_URL = "mongodb://" + MONGODB_HOSTS + "/admin"
MONGODB_USERNAME=os.environ['MONGODB_USERNAME']
MONGODB_PASSWORD=os.environ['MONGODB_PASSWORD']


# Connection to the authorization database.
mongorolereaderclient = MongoClient(host=MONGODB_URL, username=MONGODB_USERNAME, password=MONGODB_PASSWORD, tz_aware=True)
usergroups = UserGroups()
roleslookup = MongoDBRoles(mongorolereaderclient, usergroups)
security = FlaskAuthnz(roleslookup, "LogBook")
