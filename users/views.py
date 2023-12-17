from .models import User,Product,Warehouse,Store,ProductWarehouse,Cart,ProductCart,Order,ProductOrder
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict
from django.db.models import Q
from .forms import CustomUserCreationForm
from django.contrib.auth import login


# (...).using('finland') will switch the route of the db based on the location
# which is send by front-end

# custom authentication for login
def customAuth(username,password):
    try:
        user = User.objects.using('finland').get(username = username)
        if(user.check_password(password)):
            return user
        return 'password is incorrect'
    except User.DoesNotExist:
        try:
            user = User.objects.using('sweden').get(username = username)
            if(user.check_password(password)):
                return user
            return 'password is incorrect'
        except User.DoesNotExist:
            try:
                user = User.objects.using('default').get(username = username)
                if(user.check_password(password)):
                    return user
                return 'password is incorrect'
            except User.DoesNotExist:
                return None

# Login View (using POST method)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        res= customAuth(username,password)
        if res == 'password is incorrect':
            return HttpResponse(json.dumps({'stu':0,'message': 'Password is incorrect'}))
        if res == None:
            return HttpResponse(json.dumps({'stu':0,'message': 'User is not existed'}))
        else:
            dictObj = model_to_dict(res)
            del dictObj['date_joined']
            del dictObj['last_login']
            user = json.dumps(dictObj)
            return HttpResponse(json.dumps({'stu':1,'message': user}))
    return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))

# Register View (using POST method)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user,status = form.save()
            if(status==''):
                userHelper = User.objects.using(request.POST.get('location')).get(pk=user['id'])
                Cart.objects.using(request.POST.get('location')).create(customer=userHelper)
                return HttpResponse(json.dumps({'stu':1,'message': user}))
            return HttpResponse(json.dumps({'stu':0,'message': status}))
        else:
            return HttpResponse(json.dumps({'stu':0,'message': 'A user with that username already exists'}))
    return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))


# Get product list view (using GET method)
def getProductsList(request):
    try:
        if request.method == 'GET':
            productList = ''
            if(request.GET.get('search')==''):
                productList = list(Product.objects.using(request.GET.get('location')).filter().values())
            else:
                productList = list(Product.objects.using(request.GET.get('location')).filter(Q(name__icontains=request.GET.get('search'))).values())
            return HttpResponse(json.dumps({'stu':1,'message': productList}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Location is invalid'}))


# Get product list view (using GET method)
def getProductsListAdmin(request):
    try:
        if request.method == 'GET':
            productList = list(Product.objects.using('default').filter().values())
            return HttpResponse(json.dumps({'stu':1,'message': productList}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Location is invalid'}))


# Get product view (using GET method)
def getProduct(request):
    try:
        if request.method == 'GET':
            product = list(Product.objects.using(request.GET.get('location')).filter(pk=request.GET.get('id')).values())[0]
            return HttpResponse(json.dumps({'stu':1,'message': product}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Product not found'}))
    

# Get stores view (using GET method)
def getStores(request):
    try:
        if request.method == 'GET':
            stores = list(Store.objects.using(request.GET.get('location')).filter().values())
            return HttpResponse(json.dumps({'stu':1,'message': stores}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Product not found'}))
    

# Update product view (using POST method and UPDATE query)
def updateProduct(request):
    try:
        if request.method == 'POST':
            if(request.POST.get('location')=='default'):
                Product.objects.using('default').filter(pk=request.POST.get('id')).update(name=request.POST.get('name'),price=request.POST.get('price'))
                ProductWarehouse.objects.using('default').filter(product__id=request.POST.get('id')).update(productAmount=request.POST.get('amount'))
                return HttpResponse(json.dumps({'stu':1,'message': 'successful'}))
            else:
                try:
                    Product.objects.using(request.POST.get('location')).filter(pID=request.POST.get('pID')).update(name=request.POST.get('name'),price=request.POST.get('price'))
                    ProductWarehouse.objects.using(request.POST.get('location')).filter(warehouse_id=request.POST.get('warehouseId')).update(productAmount=request.POST.get('amount'))
                    return HttpResponse(json.dumps({'stu':1,'message': 'successful'}))
                except:
                    product = Product.objects.using(request.POST.get('location')).create(name=request.POST.get('name'),price=request.POST.get('price'),pID=request.POST.get('pID'),rating=0)
                    ProductWarehouse.objects.using(request.POST.get('location')).create(warehouse_id=request.POST.get('warehouseId'),product_id=product.id,productAmount = request.POST.get('amount'))
                    return HttpResponse(json.dumps({'stu':1,'message': 'successful'}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'stu':0,'message': 'Product not found'}))
    

# Update product view (using POST method and INSERT query)
def createProduct(request):
    try:
        if request.method == 'POST':
            if(request.POST.get('location')=='default'):
                product = Product.objects.using('default').create(name=request.POST.get('name'),price=request.POST.get('price'),rating=0)
                id=product.pk
                Product.objects.using('default').filter(pk=id).update(pID=id)
                ProductWarehouse.objects.using('default').create(product_id=id,warehouse_id=1,productAmount = request.POST.get('amount'))
                return HttpResponse(json.dumps({'stu':1,'message': id}))
            else:
                product = Product.objects.using(request.POST.get('location')).create(name=request.POST.get('name'),price=request.POST.get('price'),rating=0,pID=request.POST.get('pID'))
                ProductWarehouse.objects.using(request.POST.get('location')).create(warehouse_id=request.POST.get('warehouseId'),product_id=product.pk,productAmount = request.POST.get('amount'))
                return HttpResponse(json.dumps({'stu':1,'message': 'successful'}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'stu':0,'message': 'Product not found'}))
    


# Add product to shopping cart view (using POST method)
def addProductToShoppingCart(request):
    try:
        if request.method == 'POST':
            user = User.objects.using(request.POST.get('location')).get(pk=request.POST.get('userId'))
            product = Product.objects.using(request.POST.get('location')).get(pk=request.POST.get('productId'))
            cart = Cart.objects.using(request.POST.get('location')).get(customer=user)
            ProductCart.objects.using(request.POST.get('location')).create(product = product,cart=cart,amount=request.POST.get('amount'))
            return HttpResponse(json.dumps({'stu':1,'message': 'Product added to the shopping cart succesfully'}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Product or cart not found'}))


# Get shopping cart view (using GET method)
def getShoppingCart(request):
    try:
        if request.method == 'GET':
            user = User.objects.using(request.GET.get('location')).get(pk=request.GET.get('userId'))
            cart = Cart.objects.using(request.GET.get('location')).get(customer=user)
            productCart = list(ProductCart.objects.using(request.GET.get('location')).filter(cart__id=cart.id).values())
            return HttpResponse(json.dumps({'stu':1,'message': productCart}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Product or cart not found'}))


# Get warehouse list view (using GET method)
def getWarehousesList(request):
    try:
        if request.method == 'GET':
            warehousesList = list(Warehouse.objects.using(request.GET.get('location')).filter().values())
            return HttpResponse(json.dumps({'stu':1,'message': warehousesList}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Location is invalid'}))


# Get warehouse view (using GET method)
def getWarehouse(request):
    try:
        if request.method == 'GET':
            warehouse = list(Warehouse.objects.using(request.GET.get('location')).filter(pk=request.GET.get('id')).values())[0]
            return HttpResponse(json.dumps({'stu':1,'message': warehouse}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Warehouse not found'}))


# Get product warehouses view (using GET method)
def getProductWarehouses(request):
    try:
        if request.method == 'GET':
            warehouse = list(ProductWarehouse.objects.using(request.GET.get('location')).filter(product__id=request.GET.get('id')).values())
            return HttpResponse(json.dumps({'stu':1,'message': warehouse}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Warehouse not found'}))


# Get stores list view (using GET method)
def getStoresList(request):
    try:
        if request.method == 'GET':
            storesList = list(Store.objects.using(request.GET.get('location')).filter())
            return HttpResponse(json.dumps({'stu':1,'message': storesList}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Location is invalid'}))


# Add order list view (using POST method and also using UPDATE query)
def addOrder(request):
    try:
        if request.method == 'POST':
            user = User.objects.using(request.POST.get('location')).get(pk=request.POST.get('userId'))
            order = Order.objects.using(request.POST.get('location')).create(customer = user)
            productIds = request.POST.get('productIds').split(',')
            amounts = request.POST.get('amounts').split(',')
            for i in range(len(productIds)):
                product = Product.objects.using(request.POST.get('location')).get(pk=int(productIds[i]))
                productAmount = ProductWarehouse.objects.using(request.POST.get('location')).get(product=product).productAmount
                # update product amount in the warehouse
                ProductWarehouse.objects.using(request.POST.get('location')).filter(product=product).update(productAmount=productAmount-int(amounts[i]))
                # add order
                ProductOrder.objects.using(request.POST.get('location')).create(order = order,product=product,amount=int(amounts[i]))
            return HttpResponse(json.dumps({'stu':1,'message': 'Order submitted successfully'}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Order not submitted'}))


# Delete cart view (using GET method but using DELETE query)
def deleteCart(request):
    try:
        if request.method == 'GET':
            user = User.objects.using(request.GET.get('location')).get(pk=request.GET.get('userId'))
            cart = Cart.objects.using(request.GET.get('location')).get(customer=user)
            ProductCart.objects.using(request.GET.get('location')).filter(cart=cart).delete()
            return HttpResponse(json.dumps({'stu':1,'message': 'successfull'}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    

# Get store view (using GET method)
def getStore(request):
    try:
        if request.method == 'GET':
            store = list(Store.objects.using(request.GET.get('location')).filter(pk=request.GET.get('id')).values())[0]
            return HttpResponse(json.dumps({'stu':1,'message': store}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Store not found'}))


# Get product stores view (using GET method)
def getProductStores(request):
    try:
        if request.method == 'GET':
            store = list(Store.objects.using(request.GET.get('location')).filter(warehouse__id=request.GET.get('id')).values())
            return HttpResponse(json.dumps({'stu':1,'message': store}))
        return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))
    except:
        return HttpResponse(json.dumps({'stu':0,'message': 'Store not found'}))