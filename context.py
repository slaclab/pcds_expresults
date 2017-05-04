from MySQLdb import cursors
from psdmauth.auth_client_flask import FlaskSecurityClient
from psdmauth.auth_server_dal_db import DatabaseDal
from psdmauth.multimysql import MultiMySQL

__author__ = 'mshankar@slac.stanford.edu'

# Application context.
app = None

# Connection to the authorization database.
# Note that the prefix=ROLES will look for environment variables
# ROLES_DATABASE_HOST, $ROLES_DATABASE_DB, $ROLES_DATABASE_USER, $ROLES_DATABASE_PASSWORD etc...
roles_db = MultiMySQL(prefix="ROLES", cursorclass=cursors.DictCursor)
security = FlaskSecurityClient(DatabaseDal(roles_db), "LogBook")
