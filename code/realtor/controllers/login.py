import xmlrpc.client

from pprint import pprint

url = "http://localhost:8069"
db = "dbProjet"
username = 'admin'
password = "admin"

# Récupération de la version d'ODOO installée
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print("Version : ", common.version())

# Connexion de l'utilisateur
uid = common.authenticate(db, username, password, {})

# Référence à model.Models
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

pprint(common.version())

# Vérification des droits d'accès
hasRight = models.execute_kw(db, uid, password, 'realtor.apartment', 'check_access_rights', ['read'], {'raise_exception': False})

apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
print("Nombre d'appartements ", len(apartments))
id_created = models.execute_kw(db, uid, password, 'realtor.apartment', 'create', [{'name': 'Appart XML-RPC', 'description': "Test appart XML-RPC"}])
print("ID créé : ", id_created)
apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])

for apartment in apartments:
    print(" − Nom : ", apartment.get("name"))
    print(" − Description : ", apartment.get("description"))
    print(" − Prix attendu : ", apartment.get("expected_price"))

models.execute_kw(db, uid, password, 'openacademy.course', 'unlink', [[id_created]])