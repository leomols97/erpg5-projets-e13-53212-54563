import xmlrpc.client
from getpass import getpass

class OdooParser:
    def __init__(self):
        # Les informations de connexion sont celles qui permmettent d'accéder à l'interface web d'Odoo
        self.port = 8069
        self.url = "http://localhost:8069"
        self.db = "dbProject"
        self.username = ''
        self.password = ''
        self.uid = None
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

    def ask_user_name(self):
        """ Ask the username to the user """
        while not self.username:
            name = input("Saisissez votre login : ")
            self.username = name
            print() # saut de ligne

    def ask_password(self):
        """ Ask the password to the user """
        while not self.password:
            passwd = getpass("Password: ")
            self.password = passwd
            print() # saut de ligne

    def _validate_uid(self):
        """ Checks if the user is connected """
        if self.username and self.password:
            self.uid = self.common.authenticate(
                self.db, self.username, self.password, {}
            )
            if not self.uid:
                raise RuntimeError("Mauvais uid. Réessayez !")
        else:
            raise ValueError("Le login et le mot de passe ne peuvent pas être vides !")

    def _check_access_rights(self):
        """ Checks if the user has the rights to access the module """
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
        Ask indefinitely the user to enter a value until it is valid

        :param messageToDisplay: message to display to the user
        :param functionsToCall: functions to call
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
        Shows the informations of an apartment

        :param apartment_name: name of the apartment
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
                    'best_offer_price',
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
        Shows the informations of a product

        :param product_name: name of the product
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
        Shows the user the information of the apartment he entered the infos of
        and asks him to enter the informations to make an offer if he wants to

        :param apartment_name: name of the apartment to make an offer for
        """
        self._access_apartment_infos(apartment_name)
        # self._access_product_infos(apartment_name)
        userEntry = input("Voulez-vous faire une offre pour cet appartement ? (y/n) ")
        userEntry.lower()
        if userEntry == "y":
            # apartment_name = input("Entrez le nom de l'appartement pour lequel vous voulez faire l'offre : ")
            new_offer_price = input("Entrez le prix de votre offre : ")
            user_name = input("Entrez votre nom : ")
            self._make_offer(new_offer_price, apartment_name, user_name)
        elif userEntry == "n":
            print("Vous n'avez pas fait d'offre.\n")
        else:
            print("Vous n'avez pas fait d'offre.\n")

    def _make_offer(self, new_offer_price, apartment_name, user_name):
        """
        Handles an offer made for an apartment

        :param new_offer_price: price of the offer
        :param apartment_name: name of the apartment
        :param user_name: name of the user
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

        message_to_display = "Entrez le nom de l'appartement dont vous cherchez les informations ou 'q' pour quitter cet écran : "
        functions_to_call = [op._access_apartment_infos, op._access_product_infos]
        op._ask_indefinitely(message_to_display, functions_to_call)

        message_to_display = "Entrez le nom de l'appartement pour lequel vous voulez faire une offre ou 'q' pour quitter cet écran : "
        functions_to_call = [op._inputs_to_make_offer]
        op._ask_indefinitely(message_to_display, functions_to_call)
        
        print("\n\n Au revoir !\n")

    except KeyboardInterrupt:
        print("\n\n Au revoir !\n")
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    main()
