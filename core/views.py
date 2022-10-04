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
from math import sqrt
from rest_framework.views import APIView
from rest_framework.response import Response




month = ['','January','February','March','April','May','June','July','August','September','Octomber','November','December']

def generator(n):
    s = ''
    for i in range(n):
        s = s + str(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz0123456789')[0])
    return s


def homepage(request):
    token_1 = {"name": "Azagnat #00001", "image": "https://arweave.net/fZpv225Ubj9iwUOV4mGgg-_HZ1uG3mmrogP0rPzU0bY?ext=png", "symbol": "AZGT", "attributes": [{"value": "Buben", "trait_type": "Name"}, {"value": "2022-06-22", "trait_type": "Date of Birth"}, {"value": "Man", "trait_type": "Gender"}, {"value": "Russian", "trait_type": "Language"}, {"value": "Vega", "trait_type": "Ball_name"}, {"value": "Material", "trait_type": "Body_view"}, {"value": "Select image", "trait_type": "Background"}, {"value": "Custom color", "trait_type": "Ticker"}], "description": "Non-fungible Magic Ball", "external_url": "https://azagnat.art", "animation_url": "https://arweave.net/i9_WZEM_VFVSuIIxbc5l4NdKJXOC_nxoNk7ozkadm_0?ext=html"}
    token_2 = {"name": "Azagnat #00002", "image": "https://arweave.net/9xf_L3YUKvg6e93EnXeOMQNF9kZt-ylh7hCVjSedG78?ext=png", "symbol": "AZGT", "attributes": [{"value": "Millie", "trait_type": "Name"}, {"value": "2004-02-19", "trait_type": "Date of Birth"}, {"value": "Woman", "trait_type": "Gender"}, {"value": "English", "trait_type": "Language"}, {"value": "Vesta", "trait_type": "Ball_name"}, {"value": "Material", "trait_type": "Body_view"}, {"value": "Custom image", "trait_type": "Background"}, {"value": "Custom color", "trait_type": "Ticker"}], "description": "Non-fungible Magic Ball", "external_url": "https://azagnat.art", "animation_url": "https://arweave.net/tyOiQCVaa63urscZEtuZsE3L4zQfAkfzOowY7CsdDhs?ext=html"}
    token_3 = {"name": "Azagnat #00010", "image": "https://arweave.net/i79oAQkvaoFTgUnUFLj-mB6cjMPoMJlZhF80jrWbhaU?ext=png", "symbol": "AZGT", "attributes": [{"value": "blackcat", "trait_type": "Name"}, {"value": "2022-08-10", "trait_type": "Date of Birth"}, {"value": "Man", "trait_type": "Gender"}, {"value": "Russian", "trait_type": "Language"}, {"value": "Ostan", "trait_type": "Ball_name"}, {"value": "Custom color", "trait_type": "Body_view"}, {"value": "Single color", "trait_type": "Background"}, {"value": "Custom color", "trait_type": "Ticker"}], "description": "Non-fungible Magic Ball", "external_url": "https://azagnat.art", "animation_url": "https://arweave.net/GSx_OTKejNwDCyr2yJsRwtbx5w7uSWYBHr3Xj4BjlCA?ext=html"}
    try:
        config_len = str(MintCount.objects.get(id=1).general_sum + 1)
    except ObjectDoesNotExist:
        MintCount.objects.create()
        config_len = str(1)
    
    if len(config_len) < 5:
        config_len = str((5 - len(config_len)) * '0') + config_len

    percent = 'X'
    
    if ('r' in request.GET and 'p' in request.GET):
        return redirect(homepage)
    elif 'r' in request.GET:
        try:
            RefferalCode.objects.get(code=request.GET.get('r'))
            percent = 20
            is_active = True
        except ObjectDoesNotExist:
            return redirect(homepage)
    elif 'a' in request.GET:
        try:
            Ambassador.objects.get(code=f'{DOMEN}?a='+request.GET.get('a'))
            percent = 20
            is_active = True
        except ObjectDoesNotExist:
            return redirect(homepage)
    elif 'p' in request.GET:
        try:
            pro = Promocode.objects.get(code=f'{DOMEN}?p='+request.GET.get('p'))
            if pro.isactive:
                is_active = True
                percent = pro.percent
            else:
                is_active = False
        except ObjectDoesNotExist:
            return redirect(homepage)
    else:
        is_active = True
    try:
        re = Returned.objects.get(id=1)
    except ObjectDoesNotExist:
        re = Returned.objects.create()
    return render(request, 'index.html', {'id': config_len, 'percent' : percent, 'returned': "{:.3f}".format(re.count), 'is_active': is_active, 'token_1': token_1, 'token_2': token_2, 'token_3': token_3})

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

    ref_data = {
       'refs' :[]
    }
    configs = Config.objects.filter(address_id=publickey)
    for config in configs:
        data = config.refferalcode
        ref_data['refs'].append({'ref_link': f'{DOMEN}?r={data.code}', 'token_id': data.config.metadata['name'].split()[1], 'cost' : "{:.3f}".format(config.cost), 'paid' : "{:.3f}".format(data.paid), 'deals' : data.deals, 'screen' : data.config.metadata['image'], 'token_link': config.html, 'contract': config.contract})
    r = JsonResponse(ref_data)
    r.set_cookie('publickey', publickey)
    return r
     
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
        price['global_price'] = baseprice - (baseprice * 0.2)
    else:
        price['global_price'] = baseprice

    if data['model'] == None:
        price['model_price'] = .0
        price['global_price'] += price['model_price']
    else:
        price['model_price'] = Models.objects.get(id=int(data['model'])+1).price * baseprice
        price['global_price'] += price['model_price']

    try:
        if data['idBodyColor'] == '3':
            price['body_price'] = BodyViewPrice.objects.get(id=1).select_image * baseprice
            price['global_price'] += price['body_price']
        elif data['idBodyColor'] == '2':
            price['body_price'] = BodyViewPrice.objects.get(id=1).custom_image * baseprice
            price['global_price'] += price['body_price']
        elif data['idBodyColor'] == '1':
            price['body_price'] = BodyViewPrice.objects.get(id=1).custom_color * baseprice
            price['global_price'] += price['body_price']
        elif data['idBodyColor'] == '0':
            price['body_price'] = .0
            price['global_price'] += price['body_price']
        elif data['idBodyColor'] == '4':
            if data['selectedMaterialId'] == None:
                price['body_price'] = .0
            else:
                price['body_price'] = Materials.objects.get(id=int(data['selectedMaterialId'])+1).price * baseprice
                price['global_price'] += price['body_price']
    except KeyError:
        pass
    try:
        if data['idBackground'] == '5':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).select_image * baseprice
            price['global_price'] += price['bg_price']
        elif data['idBackground'] == '4':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).custom_image * baseprice
            price['global_price'] += price['bg_price']
        elif data['idBackground'] == '3':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).radial_gradient * baseprice
            price['global_price'] += price['bg_price']
        elif data['idBackground'] == '2':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).linear_gradient * baseprice
            price['global_price'] += price['bg_price']
        elif data['idBackground'] == '1':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).single_color * baseprice
            price['global_price'] += price['bg_price']
        elif data['idBackground'] == '0':
            price['bg_price'] = .0
            price['global_price'] += price['bg_price']
    except KeyError:
        pass

    if 'tickerColor' in data:
        if data['tickerColor'] == "#004f20":
            price['ticker_price'] = .0
            price['global_price'] += price['ticker_price']
        else:
            price['ticker_price'] = TickerPrice.objects.get(id=1).color * baseprice
            price['global_price'] += price['ticker_price']
    else:
        price['ticker_price'] = .0
        price['global_price'] += price['ticker_price']
    return JsonResponse(price)


class FreeDice(APIView):
    def get(self, request):
        x = 20
        y = 3
        o = 0.2
        a = (-o*x+sqrt(((o*x)**2)+(4*o*x)/y))/2
        b = y-(1/a)
        r = float("{:.2f}".format(random.uniform(0, 10)))
        k = "{:.3f}".format((1/(o*r+a))+b)
        win = float(k) * float(request.GET['bet'])
        return Response({'win': "{:.4f}".format(win)})



class PremiumDice(APIView):
    def get(self, request):
        res = {}
        x = 100
        y = 76
        o = 0.03
        a = (-o*x+sqrt(((o*x)**2)+(4*o*x)/y))/2
        b = y-(1/a)
        s = random.randint(1, 98)
        if request.GET['isunder']:
            if s < int(request.GET['select']):
                k = "{:.3f}".format((1/((o*float(request.GET['select']))+a))+b+1)
                w = float(k) * float(request.GET['bet'])
                res['win'] = w
            else:
                w = 0
                res['win'] = w
        else:
            ss = request.GET['select']*-1+99
            if s > ss:
                k = "{:.3f}".format((1/((o*float(request.GET['select']))+a))+b+1)
                w = float(k) * float(request.GET['bet'])
                res['win'] = w
            else:
                w = 0
                res['win'] = w
        return Response(res)