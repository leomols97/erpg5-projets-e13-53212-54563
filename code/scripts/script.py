import xmlrpc.client
from getpass import getpass

class OdooParser:
    def __init__(self):
        # Les informations de connexion sont celles qui permmettent d'accéder à l'interface web d'Odoo
        self.port = 8069
        self.url = "http://localhost:8069"
        self.db = "apa3"
        self.username = ''
        self.password = ''
        self.uid = None
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

    def ask_user_name(self):
        """
        Demande le nom d'utilisateur à l'utilisateur
        """
        while not self.username:
            name = input("Saisissez votre login : ")
            self.username = name
            print() # saut de ligne

    def ask_password(self):
        """
        Demande le mot de passe à l'utilisateur
        """
        while not self.password:
            passwd = getpass("Password: ")
            self.password = passwd
            print() # saut de ligne

    def _validate_uid(self):
        """
        Vérifie si l'utilisateur est connecté
        """
        if self.username and self.password:
            self.uid = self.common.authenticate(
                self.db, self.username, self.password, {}
            )
            if not self.uid:
                raise RuntimeError("Mauvais uid. Réessayez !")
        else:
            raise ValueError("Le login et le mot de passe ne peuvent pas être vides !")

    def _check_access_rights(self):
        """
        Vérifie les droits d'accès de l'utilisateur
        """
        if self.models.execute_kw(
                self.db,
                self.uid,
                self.password,
                'realtor.apartment',
                'check_access_rights',
                ['read'],
                {'raise_exception': False},
        ):
            print("Vous avez accès aux appartements.\n")

    def _ask_indefinitely(self, messageToDisplay, functionsToCall) :
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

    def _access_apartment_infos(self, apartment_name):
        """
        Affiche les informations d'un appartement

        :param product_name: nom du product
        """
        infos = self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            'realtor.apartment',
            'search_read',
            [[['name', '=', apartment_name]]],
            {
                'fields': [
                    'name',
                    'date_creation',
                    'date_disponibility',
                    'expected_price',
                    'apartment_area',
                    'terrace_area',
                    'total_area',
                    'buyer',
                    'disponibility',
                ]
            },
        )
        if infos:
            print("\nVoici les informations de l'appartement demandé :\n")
            for info in infos:
                for i, j in info.items():
                    print(f"{i:20} ==> {j}")
            print()
        else:
            print("Aucun appartement ne porte ce nom !\n")

    def _access_product_infos(self, product_name):
        """
        Affiche la quantité d'un product

        :param product_name: nom du product
        """
        apartments = self.models.execute_kw(self.db, self.uid, self.password, 'realtor.apartment', 'search_read', [[]])
        products = self.models.execute_kw(self.db, self.uid, self.password, 'product.template', 'search_read', [[]])
        for apartment in apartments:
            for product in products:
                if (product.get("apartment_id") != False
                        and apartment.get("name") == product.get("apartment_id")[1]
                        and product.get("apartment_id")[1] == product_name):
                    print(" − Quantité disponible :", product.get("quantity"))

    # La gestion de l'erreur d'un appartement inexistant est gérée dans la fonction showApartmentInfos

    def _inputs_to_make_offer(self, apartment_name):
        """
        Affiche les informations d'un appartement et demande à l'utilisateur s'il veut faire une offre

        :param apartment_name: nom de l'appartement
        """
        self._access_apartment_infos(apartment_name)
        # self._access_product_infos(apartment_name)
        userEntry = input("Voulez-vous faire une offre pour cet appartement ? (y/n) ")
        userEntry.lower()
        if userEntry == "y":
            # apartment_name = input("Entrez le nom de l'appartement pour lequel vous voulez faire l'offre : ")
            new_offer_price = input("Entrez le prix de votre offre : ")
            user_name = input("Entrez votre nom : ")
            op._make_offer(new_offer_price, apartment_name, user_name)
        elif userEntry == "n":
            print("Vous n'avez pas fait d'offre.\n")
        else:
            print("Vous n'avez pas fait d'offre.\n")

    def _make_offer(self, new_offer_price, apartment_name, user_name):
        """
        Gère une offre faite pour un appartement

        :param new_offer_price: le prix de la nouvelle offre
        :param apartment_name: le nom de l'appartement pour lequel l'offre est faite
        :param user_name: le nom de l'utilisateur qui fait l'offre
        :return:
        """
        # Gets the actual offer price through 'search_read'
        actual_offer_price = self.models.execute_kw(self.db, self.uid, self.password, 'realtor.apartment', 'search_read', [
            [['best_offer_price', '=', new_offer_price], ['name', '=', apartment_name]]])
        # Gets the apartment id of the actual offer
        idActualApart = actual_offer_price[0].get("id")
        # Gets the connected user id
        self.models.execute_kw(self.db, self.uid, self.password, 'res.partner', 'search_read', [[['name', '=', user_name]]])
        # If the new offer price is higher than the actual offer price, the new offer price is set as the best offer price
        if actual_offer_price[0]['best_offer_price'] < int(new_offer_price):
            # Creates a res.partner record with the user_name, whether it exists or not
            self.models.execute_kw(self.db, self.uid, self.password, 'res.partner', 'create',
                                   [{'name': user_name, 'apartment': idActualApart, 'offer_price': new_offer_price}])
            # Updates the best offer price of the apartment
            self.models.execute_kw(self.db, self.uid, self.password, 'realtor.apartment', 'write',
                                   [[idActualApart], {'best_offer_price': new_offer_price}])
            print("L'offre a été prise en compte")


def main():
    try:
        print("\nBienvenue dans l'API XMLRPC d'Odoo. Entrez 'CTRL + C' pour quitter à n'importe quel moment !\n")
        op = OdooParser()
        op.ask_user_name()
        op.ask_password()
        op._validate_uid()
        op._check_access_rights()

        message_to_display = "Entrez le nom de l'appartement dont vous cherchez les informations ou 'q' pour quitter cet écran : "
        functions_to_call = [op._access_apartment_infos]
        op._ask_indefinitely(message_to_display, functions_to_call)

        message_to_display = "Entrez le nom du produit dont vous cherchez les informations ou 'q' pour quitter cet écran : "
        functions_to_call = [op._access_apartment_infos, op._access_product_infos]
        op._ask_indefinitely(message_to_display, functions_to_call)

        message_to_display = "Entrez le nom de l'appartement pour lequel vous voulez faire une offre ou q pour quitter cet écran : "
        functions_to_call = [op._inputs_to_make_offer]
        op._ask_indefinitely(message_to_display, functions_to_call)

    except KeyboardInterrupt:
        print("\n\n Au revoir !\n")
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    main()






# # Paramètres de connexion
# url = "http://localhost:8069"
# db = "apa3"
# username = "53212@etu.he2b.be"
# password = "admin"
#
# # Récupération de la version d’ODOO installée
# common = xmlrpc.client.ServerProxy(
#     '{}/xmlrpc/2/common'.format(url))
#
# # Connexion de l’utilisateur
# uid = common.authenticate(db, username, password, {})
#
# # Référence à model.Models
# models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
#
# #
# # # def __init__(self):
# # #
# # #     # Paramètres de connexion
# # #     url = "http://localhost:8069"
# # #     db = "apa3"
# # #     username = input("Saisissez login : ")
# # #     password = input("Saisissez password : ")
# # #     self.port = 8069
# # #
# # #     # Connexion de l’utilisateur
# # #     uid = common.authenticate(db, username, password, {})
# #
# def hasRightsToAccess(modelName) :
#     """
#     Vérifie si l'utilisateur a les droits d'accès à un modèle
#
#     :param modelName: nom du modèle à accéder
#     :return: True si l'utilisateur a les droits d'accès
#     """
#     try:
#         hasRight = models.execute_kw(db, uid, password, modelName, 'check_access_rights', ['read'], {'raise_exception': False})
#         return True
#     except:
#         print("Vous n'avez pas accès au modèle ", modelName)
#
# def askIndefinitely(messageToDisplay, functionsToCall) :
#     """
#     Affiche un message et demande à l'utilisateur de saisir une valeur jusqu'à ce qu'il saisisse une valeur valide et ce, indéfiniment
#
#     :param messageToDisplay: message à afficher à l'utilisateur
#     :param functionsToCall: fonction(s) à appeler
#     """
#     continuer = True
#     while continuer:
#         userEntry = input(messageToDisplay)
#         if userEntry == "q":
#             continuer = False
#         else:
#             for functionToCall in functionsToCall:
#                 functionToCall(userEntry)
#
# def showApartmentInfos(apartmentName) :
#     """
#     Affiche les informations d'un appartement
#
#     :param apartmentName: nom de l'appartement
#     """
#     apartments = models.execute_kw(db, uid, password,'realtor.apartment', 'search_read', [[]])
#     i = 0
#     for apartment in apartments:
#
#         if apartment.get("name") == apartmentName:
#             print(" − name : ", apartment.get("name"))
#             print(" − description : ", apartment.get("description"))
#             print(" − expected_price : ", apartment.get("expected_price"))
#             print(" − apartment_area : ", apartment.get("apartment_area"))
#             print(" − terrace_area : ", apartment.get("terrace_area"))
#         else:
#             i = i + 1 # Compteur pour savoir si l'appartement existe ou non
#         if i == len(apartments):
#             print("L'appartement n'existe pas")
#     if i == 0:
#         print("Il n'y a aucun appartement")
#
# def showProductInfos(productName) :
#     """
#     Affiche les informations d'un product
#
#     :param productName: nom du product
#     """
#     apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
#     products = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[]])
#     for apartment in apartments:
#         for product in products:
#             if (product.get("apartment_id") != False
#                     and apartment.get("name") == product.get("apartment_id")[1]
#                     and product.get("apartment_id")[1] == productName):
#                 print(" − Quantité disponible :", product.get("quantity"))
#
#     # La gestion de l'erreur d'un appartement inexistant est gérée dans la fonction showApartmentInfos
#
# # Vérification des droits d’accès
# if hasRightsToAccess("realtor.apartment") :
#     functionsToCall = [showApartmentInfos]
#     askIndefinitely("Saisissez le nom de l'appartement que vous souhaitez ou q si vous voulez continuer : ", functionsToCall)
#
#
# # Rechercher le product avec l'ID spécifié
# if hasRightsToAccess("product.template") :
#     functionsToCall = [showApartmentInfos, showProductInfos]
#     askIndefinitely("Saisissez le nom du produit que vous souhaitez ou q si vous voulez continuer : ", functionsToCall)

#
#
#
#
# def createAppart(name, expected_price, apartment_area, terrace_area, total_area, best_offer_price):
#     models.execute_kw(db, uid, password, 'realtor.apartment', 'create', [{'name': name, 'description': 'description', 'expected_price': expected_price, 'apartment_area': apartment_area, 'terrace_area': terrace_area, 'total_area': total_area, 'best_offer_price': best_offer_price}])
#
# # name = input("name ? ")
# # expected_price = input("expected_price ? ")
# # apartment_area = input("apartment_area ? ")
# # terrace_area = input("terrace_area ? ")
# # total_area = input("total_area ? ")
# # best_offer_price = input("best_offer_price ? ")
#
# # createAppart(name, expected_price, apartment_area, terrace_area, total_area, best_offer_price)
#
#

# #
# #
# #
# #
# # 
# def makeOffer(new_offer_price, apartment_name, user_name):
#     # Gets the actual offer price through 'search_read'
#     actual_offer_price = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[['best_offer_price', '=', new_offer_price], ['name', '=', apartment_name]]])
#     print(actual_offer_price)
#     # Gets the apartment id of the actual offer
#     idActualApart = actual_offer_price[0].get("id")
#     # Gets the user id of the actual offer through 'search_read'
#     models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['name', '=', user_name]]])
#     # If the new offer price is higher than the actual offer price, the new offer price is set as the best offer price
#     if actual_offer_price[0]['best_offer_price'] < int(new_offer_price) :
#         # Creates a res.partner record with the user name, whether it exists or not
#         models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': user_name, 'apartment': idActualApart, 'offer_price': new_offer_price}])
#         # Updates the best offer price of the apartment
#         models.execute_kw(db, uid, password, 'realtor.apartment', 'write', [[idActualApart], {'best_offer_price': new_offer_price}])
#         print("L'offre a été prise en compte")
#
# # apartment_name = input("apartment_name ? ")
# # new_offer_price = input("new_offer_price ? ")
# # user_name = input("user_name ? ")
# if hasRightsToAccess("realtor.apartment") :
#     makeOffer(400000, "Medium Apartment", "53212@etu.he2b.be")
