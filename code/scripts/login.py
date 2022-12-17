import xmlrpc.client

# Paramètres de connexion
url = "http://localhost:8069"
db = "apa3"
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

def hasRightsToAccess(modelName) :
    """
    Vérifie si l'utilisateur a les droits d'accès à un modèle

    :param modelName: nom du modèle à accéder
    :return: True si l'utilisateur a les droits d'accès
    """
    try:
        hasRight = models.execute_kw(db, uid, password, modelName, 'check_access_rights', ['read'], {'raise_exception': False})
        return True
    except:
        print("Vous n'avez pas accès au modèle ", modelName)

def askIndefinitely(messageToDisplay, functionsToCall) :
    """
    Affiche un message et demande à l'utilisateur de saisir une valeur jusqu'à ce qu'il saisisse une valeur valide et ce, indéfiniment

    :param messageToDisplay: message à afficher à l'utilisateur
    :param functionsToCall: fonction(s) à appeler
    """
    continuer = True
    while continuer:
        userEntry = input(messageToDisplay)
        if userEntry == "q":
            continuer = False
        else:
            for functionToCall in functionsToCall:
                functionToCall(userEntry)

def showApartmentInfos(apartmentName) :
    """
    Affiche les informations d'un appartement

    :param apartmentName: nom de l'appartement
    """
    apartments = models.execute_kw(db, uid, password,'realtor.apartment', 'search_read', [[]])
    i = 0
    for apartment in apartments:

        if apartment.get("name") == apartmentName:
            print(" − name : ", apartment.get("name"))
            print(" − description : ", apartment.get("description"))
            print(" − expected_price : ", apartment.get("expected_price"))
            print(" − apartment_area : ", apartment.get("apartment_area"))
            print(" − terrace_area : ", apartment.get("terrace_area"))
        else:
            i = i + 1 # Compteur pour savoir si l'appartement existe ou non
        if i == len(apartments):
            print("L'appartement n'existe pas")

def showProductInfos(productName) :
    """
    Affiche les informations d'un product

    :param productName: nom du product
    """
    apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
    products = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[]])
    for apartment in apartments:
        for product in products:
            if (product.get("apartment_id") != False
                    and apartment.get("name") == product.get("apartment_id")[1]
                    and product.get("apartment_id")[1] == productName):
                print(" − Quantité disponible :", product.get("quantity"))

    # La gestion de l'erreur d'un appartement inexistant est gérée dans la fonction showApartmentInfos

# Vérification des droits d’accès
if hasRightsToAccess("realtor.apartment") :
    functionsToCall = [showApartmentInfos]
    askIndefinitely("Saisissez le nom de l'appartement que vous souhaitez ou q si vous voulez continuer : ", functionsToCall)


# Rechercher le product avec l'ID spécifié
if hasRightsToAccess("product.template") :
    functionsToCall = [showApartmentInfos, showProductInfos]
    askIndefinitely("Saisissez le nom du produit que vous souhaitez ou q si vous voulez continuer : ", functionsToCall)