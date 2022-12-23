import xmlrpc.client
from django.shortcuts import render, redirect



# # Create your views here.
# def faireineoffr(request)

#     appaeszr = request.POST['appart']
#     if off < best
#         offerNotValid = true

#     return 


def showProductInfos(apartmentName,models,db,uid,password) :
    """
    Affiche les informations d'un product

    :param productName: nom du product
    """

    a = {}
    apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
    products = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[]])
    for apartment in apartments:
        for product in products:
            if (product.get("apartment_id") != False
                    and apartment.get("name") == product.get("apartment_id")[1]
                    and product.get("apartment_id")[1] == apartmentName):
                print(" − Quantité disponible :", product.get("quantity"))
                a[apartment.get("name")] = product.get("quantity")

 
def index(request):
  username = request.session['username']
  password = request.session['password']
  url = "http://localhost:8069"
  db = "apa12"
  uid = request.session['uid']

  

  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
  apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])


  a = {}
  apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
  products = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[]])
  for apartment in apartments:
        for product in products:
            
                a[apartment.get("name")] = product.get("quantity")


  return render(request, 'apartmentPurchase/index.html', {'apartments': apartments})



def makeOffer(request, new_offer_price, apartment_name, user_name):

    password = request.session['password']
    url = "http://localhost:8069"
    db = "apa12"
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



def verif(request):
  username = request.session['username']
  password = request.session['password']
  url = "http://localhost:8069"
  db = "apa12"
  uid = request.session['uid']
  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
  apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])
  
 

  offer = None
  
  for apartment in apartments:
      offer = request.POST.get(apartment.get("name"))
      
      offer = offer or "1"
      # print(offer)
      if(offer!= "1"):
        print(apartment.get("name"))
        makeOffer(request, offer, apartment.get("name"), username)
        

  return redirect('/apartmentPurchase/')