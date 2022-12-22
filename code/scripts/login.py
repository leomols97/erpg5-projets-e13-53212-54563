import xmlrpc.client

# Paramètres de connexion
url = "http://localhost:8069"
db = "apa12"
username = input("Saisissez login : ")
password = input("Saisissez password : ")

# Récupération de la version d’ODOO installée
common = xmlrpc.client.ServerProxy(
    '{}/xmlrpc/2/common'.format(url))

# Connexion de l’utilisateur
uid = common.authenticate(db, username, password, {})

# Référence à model.Models
models = xmlrpc.client.ServerProxy(
    '{}/xmlrpc/2/object'.format(url))

# Vérification des droits d’accès
try:
    hasRight = models.execute_kw(db, uid, password,
                                 'realtor.apartment', 'check_access_rights',
                                 ['read'], {'raise_exception': False})

    apartment = models.execute_kw(db, uid, password,
                                  'realtor.apartment', 'search_read', [[]])

    nomAppart = input("Saisissez le nom de l'appartement que vous souhaitez ou q si vous voulez quitter : ")

    continuer = True;
    while (continuer):
        i = 0
        for nom in apartment:

            if (nom.get("name") == nomAppart):
                print(" − name : ", nom.get("name"))
                print(" − description : ", nom.get("description"))
                print(" − expected_price : ", nom.get("expected_price"))
                print(" − apartment_area : ", nom.get("apartment_area"))
                print(" − terrace_area : ", nom.get("terrace_area"))
            else:
                i = i + 1
            if (i == len(apartment)):
                print("L'appartement n'existe pas")

        name = input("Saisissez le nom de l'appartement que vous souhaitez ou q si vous voulez quitter : ")
        if (name == "q"):
            continuer = False
        else:
            nomAppart = name
except:
    print("vous n'avez pas accès au modèle 'Apartment'")