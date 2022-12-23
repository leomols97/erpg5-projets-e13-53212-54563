import xmlrpc.client
from django.shortcuts import render, redirect


def index(request):
  """
Affiche la liste des appartements avec leurs détails

:param request
"""
  password = request.session['password']
  url = "http://localhost:8069"
  db = "apa3"
  uid = request.session['uid']

  

  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
  apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])

  #création d'un dictionnaire
  a = {}
  apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
  products = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[]])
  for apartment in apartments:
        for product in products:
            if (product.get("apartment_id") != False
                    and apartment.get("name") == product.get("apartment_id")[1]):
                a[apartment.get("name")] = product.get("quantity")
                print(a[apartment.get("name")])          

  request.session['a'] = a
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
    db = "apa3"
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
  db = "apa3"
  uid = request.session['uid']
  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
  apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
  acheteur = request.POST.get('acheteur')

  offer = None
  
  for apartment in apartments:
      offer = request.POST.get(apartment.get("name"))
      
      offer = offer or "1"
      if(offer!= "1"):
        makeOffer(request, offer, apartment.get("name"), acheteur)


  return redirect('/apartmentPurchase/')