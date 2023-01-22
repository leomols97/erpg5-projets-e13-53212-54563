import xmlrpc.client
from django.shortcuts import render, redirect


def index(request):
  """
Affiche la liste des appartements avec leurs détails

:param request
"""
  password = request.session['password'] # Problème de sécurité pusique l'on récupère le password avec la variable 'session'
  url = "http://localhost:8069"
  db = "dbProject"
  uid = request.session['uid']

  

  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
  # apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])

  #création d'un dictionnaire car il y avait un problème pour récupérer la quantité des products
  apartDicos = {}
  apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
  products = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[]])
  for apartment in apartments:
        for product in products:
            if (product.get("apartment_id") != False
                    and apartment.get("name") == product.get("apartment_id")[1]): # get("apartment_id")[1] permet de récupérer le nom de l'appartement
                apartDicos[apartment.get("name")] = product.get("quantity") # "name" est le nom de l'appartement dans la clef du dictionnaire
                print(apartDicos[apartment.get("name")])

  request.session['apartDicos'] = apartDicos
  return render(request, 'apartmentPurchase/index.html', {'apartments': apartments})



def makeOffer(request, new_offer_price, apartment_name, user_name):
    """
    Gère une offre faite pour un appartement

    :param new_offer_price: le prix de la nouvelle offre
    :param apartment_name: le nom de l'appartement pour lequel l'offre est faite
    :param user_name: le nom de l'utilisateur qui fait l'offre
    """
    password = request.session['password']
    url = "http://localhost:8069"
    db = "dbProject"
    uid = request.session['uid']

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    



    # Gets the actual offer price through 'search_read'
    actual_offer_price = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[['best_offer_price', '=', new_offer_price], ['name', '=', apartment_name]]])
    # Gets the apartment id of the actual offer
    idActualApart = actual_offer_price[0].get("id")
    # Gets the connected user id
    models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['name', '=', user_name]]])
    # If the new offer price is higher than the actual offer price, the new offer price is set as the best offer price
    if actual_offer_price[0]['best_offer_price'] < int(new_offer_price) :
        # Creates a res.partner record with the user name, whether it exists or not
        models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': user_name, 'apartment': idActualApart, 'offer_price': new_offer_price}])
        # Updates the best offer price of the apartment
        models.execute_kw(db, uid, password, 'realtor.apartment', 'write', [[idActualApart], {'best_offer_price': new_offer_price}])



def verification(request):
  """
vérifie la valeur de retour du post et gère en fonction l'offre pour
l'appartement donné

:param request:
"""
  password = request.session['password']
  url = "http://localhost:8069"
  db = "dbProject"
  uid = request.session['uid']
  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
  apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
  # formulaire en POST, donc, il faut get le nom de l'acheteur
  # via la balise input dont le name est 'acheteur' dans le formulaire
  acheteur = request.POST.get('acheteur')

  # ceci permet de ne pas créer 2 fois la même offre pour un même appartement. Si l'offre existe, on ne la crée pas.
  # Si l'offre n'existe pas, on la met à 1 qui est la valeur par défaut lorsque l'on récupère 'offer' en post dans la variable 'request'
  for apartment in apartments:
      # on récupère la valeur de l'input dont le name est le nom de l'appartement (name="{{ apart.name }}") et on assigne le nom à offer
      offer = request.POST.get(apartment.get("name"))

      # si l'offre est différente de 1, c'est qu'elle existe et on ne la crée pas
      offer = offer or "1"
      # Si offer existe, offer reste offer et prends le nom de l'appart. Sinon, offer prends la valeur 1
      if(offer != "1"):
        makeOffer(request, offer, apartment.get("name"), acheteur)


  return redirect('/apartmentPurchase/')