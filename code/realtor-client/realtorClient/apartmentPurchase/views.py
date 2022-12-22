from django.shortcuts import render
import xmlrpc.client


# # Create your views here.
# def faireineoffr(request)

#     appaeszr = request.POST['appart']
#     if off < best
#         offerNotValid = true

#     return 

# def possible(request):





def index(request):
  print('ICI')
  username = request.session['username']
  password = request.session['password']
  url = "http://localhost:8069"
  db = "apa12"
  uid = request.session['uid']

  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
  apartments = models.execute_kw(db, uid, password, 'realtor.apartment', 'search_read', [[]])

  for apartment in apartments:
            print(" − name : ", apartment.get("name"))
            print(" − description : ", apartment.get("description"))
            print(" − expected_price : ", apartment.get("expected_price"))
            print(" − apartment_area : ", apartment.get("apartment_area"))
            print(" − terrace_area : ", apartment.get("terrace_area"))

  return render(request, 'apartmentPurchase/index.html', {'apartments': apartments})

