from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import json
import random
from .tasks import minttask
from aza.settings import DOMEN

month = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'Octomber', 'November', 'December']

def generator(n):
    s = ''
    for i in range(n):
        s = s + str(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz0123456789')[0])
    return s


def homepage(request):

    try:
        config_len = str(MintCount.objects.get(id=1).general_sum + 1)
    except ObjectDoesNotExist:
        MintCount.objects.create()
        config_len = str(1)
    
    if len(config_len) < 5:
        config_len = str((5 - len(config_len)) * '0') + config_len

    is_active = True

    if len(request.GET.dict().items()) > 1:
        return redirect(homepage)
    
    if 'r' in request.GET:
        try:
            RefferalCode.objects.get(code=request.GET.get('r'))
            is_active = True
        except ObjectDoesNotExist:
            is_active = False
    elif 'a' in request.GET:
        try:
            Ambassador.objects.get(code=f'{DOMEN}?a='+request.GET.get('a'))
            is_active = True
        except ObjectDoesNotExist:
            is_active = False
    elif 'p' in request.GET:
        try:
            Promocode.objects.get(code=f'{DOMEN}?p='+request.GET.get('p'))
            is_active = True
        except ObjectDoesNotExist:
            is_active = False
    elif 'e' in request.GET:
        try:
            EasyMint.objects.get(code=f'{DOMEN}?e='+request.GET.get('e'))
            is_active = True
        except ObjectDoesNotExist:
            is_active = False
    try:
        re = Returned.objects.get(id=1)
    except ObjectDoesNotExist:
        re = Returned.objects.create()
    
    return render(request, 'index.html', {'id': config_len, 'returned': "{:.3f}".format(re.count), 'is_active': is_active, "mint_active": MintActive.objects.all().last().is_active})


def creating(request):
    return render(request, 'creating.html')

def ownership(request):
    return render(request, 'ownership.html')



@csrf_exempt
@require_POST
def auth(request):
    publickey = json.loads(request.body.decode('utf8').replace("'", '"'))['publickey']
    try:
        a = Address.objects.get(address=publickey)
        a.address = publickey
        a.save()
    except ObjectDoesNotExist:
        a = Address.objects.create(address=publickey)


    try:
        r = RefferalCode.objects.get(config=a)
        ref_data = {
            'code': r.code,
            'paid': r.paid,
            'deals': r.deals
        }
    except RefferalCode.DoesNotExist:
        ref_data = {
            'code': '',
            'paid': '',
            'deals': ''
        }

    r = JsonResponse(ref_data)
    r.set_cookie('publickey', publickey)
    return r

def cost(request, address):
    return JsonResponse({"cost": Config.objects.get(contract=address).cost})

@csrf_exempt
@require_POST
def mint(request):
    count = MintCount.objects.get(id=1)
    count.general_sum += 1
    count.save()
    data = json.loads(request.body.decode('utf8').replace("'", '"'))
    minttask.delay(data, request.COOKIES.get('publickey'))
    return HttpResponse("wait")


@csrf_exempt
@require_POST
def getprice(request):
    price = {}
    price['model_price'] = .0
    price['body_price'] = .0
    price['bg_price'] = .0
    price['ticker_price'] = .0
    baseprice = BasePrice.objects.get(id=1).price
    data = json.loads(request.body.decode('utf8').replace("'", '"'))
    if 'p' in data['get_par']:
        if Promocode.objects.get(code=f'{DOMEN}?p='+data['get_par']['p']).isactive:
            price['global_price'] = baseprice - (baseprice * (Promocode.objects.get(code=f'{DOMEN}?p='+data['get_par']['p']).percent / 100))
        else:
            price['global_price'] = baseprice
    elif 'r' in data['get_par']:
        price['global_price'] = baseprice - (baseprice * 0.2)
    elif 'a' in data['get_par']:
        price['global_price'] = baseprice - (baseprice * (Ambassador.objects.get(code=f'{DOMEN}?a='+data['get_par']['a']).percent / 100))
    else:
        price['global_price'] = baseprice

    if data['model'] == None:
        price['model_price'] = Models.objects.get(id=1).price
        price['global_price'] += price['model_price']
    else:
        price['model_price'] = Models.objects.get(id=int(data['model'])+1).price
        price['global_price'] += price['model_price']

    try:
        if data['idBody'] == '3':
            price['body_price'] = BodyViewPrice.objects.get(id=1).select_image
            price['global_price'] += price['body_price']
        elif data['idBody'] == '2':
            price['body_price'] = BodyViewPrice.objects.get(id=1).custom_image
            price['global_price'] += price['body_price']
        elif data['idBody'] == '1':
            price['body_price'] = BodyViewPrice.objects.get(id=1).custom_color
            price['global_price'] += price['body_price']
        elif data['idBody'] == '0':
            price['body_price'] = .0
            price['global_price'] += price['body_price']
        elif data['idBody'] == '4':
            if data['selectedMaterialId'] == None:
                price['body_price'] = .0
            else:
                price['body_price'] = Materials.objects.get(id=int(data['selectedMaterialId'])+1).price
                price['global_price'] += price['body_price']
    except KeyError:
        pass
    try:
        if data['idBack'] == '5':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).select_image
            price['global_price'] += price['bg_price']
        elif data['idBack'] == '4':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).custom_image
            price['global_price'] += price['bg_price']
        elif data['idBack'] == '3':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).radial_gradient
            price['global_price'] += price['bg_price']
        elif data['idBack'] == '2':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).linear_gradient
            price['global_price'] += price['bg_price']
        elif data['idBack'] == '1':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).single_color
            price['global_price'] += price['bg_price']
        elif data['idBack'] == '0':
            price['bg_price'] = .0
            price['global_price'] += price['bg_price']
    except KeyError:
        pass

    try:
        if data['tickerId'] == "0":
            price['ticker_price'] = .0
            price['global_price'] += price['ticker_price']
        else:
            price['ticker_price'] = TickerPrice.objects.get(id=1).color
            price['global_price'] += price['ticker_price']
    except KeyError:
        pass


    if 'e' in data['get_par']:
        price['global_price'] = price['global_price'] - (price['global_price'] * (90 / 100))
    return JsonResponse(price)