from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import json
import random
from .tasks import minttask
from aza.settings import DOMEN, secretKeyNew
from math import sqrt
from rest_framework.views import APIView
from rest_framework.response import Response
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
import base58
import logging
from user_agents import parse

logger = logging.getLogger('django')

month = ['','January','February','March','April','May','June','July','August','September','Octomber','November','December']

def generator(n):
    s = ''
    for i in range(n):
        s = s + str(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz0123456789')[0])
    return s


def homepage(request):
    logger.info('azagnat')
    user_agent = parse(request.META['HTTP_USER_AGENT'])

    
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

    if user_agent.is_mobile:
        return render(request, 'index.html', {'id': config_len, 'percent' : percent, 'returned': "{:.3f}".format(re.count), 'is_active': is_active})
    
    if 'a' in request.GET:
        try:
            Ambassador.objects.get(code=f'{DOMEN}?a='+request.GET.get('a'))
        except ObjectDoesNotExist:
            return render(request, 'private.html')
    else:
        return render(request, 'private.html')

    
    return render(request, 'index.html', {'id': config_len, 'percent' : percent, 'returned': "{:.3f}".format(re.count), 'is_active': is_active})


def explorer(request):
    return render(request, 'explorer/explorer.html')

def deepconnect(request):
    p = str(base58.b58encode(bytes(secretKeyNew.public_key)))
    return render(request, 'explorer/connect.html', {'publickey': p[2:len(p)-1], 'secret': str(base58.b58encode(bytes(secretKeyNew)))})

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
        price['global_price'] = baseprice - (baseprice * (Ambassador.objects.get(code=f'{DOMEN}?a='+data['get_par']['a']).percent / 100))
    else:
        price['global_price'] = baseprice

    if data['model'] == None:
        price['model_price'] = .0
        price['global_price'] += price['model_price']
    else:
        price['model_price'] = Models.objects.get(id=int(data['model'])+1).price
        price['global_price'] += price['model_price']

    try:
        if data['idBodyColor'] == '3':
            price['body_price'] = BodyViewPrice.objects.get(id=1).select_image
            price['global_price'] += price['body_price']
        elif data['idBodyColor'] == '2':
            price['body_price'] = BodyViewPrice.objects.get(id=1).custom_image
            price['global_price'] += price['body_price']
        elif data['idBodyColor'] == '1':
            price['body_price'] = BodyViewPrice.objects.get(id=1).custom_color
            price['global_price'] += price['body_price']
        elif data['idBodyColor'] == '0':
            price['body_price'] = .0
            price['global_price'] += price['body_price']
        elif data['idBodyColor'] == '4':
            if data['selectedMaterialId'] == None:
                price['body_price'] = .0
            else:
                price['body_price'] = Materials.objects.get(id=int(data['selectedMaterialId'])+1).price
                price['global_price'] += price['body_price']
    except KeyError:
        pass
    try:
        if data['idBackground'] == '5':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).select_image
            price['global_price'] += price['bg_price']
        elif data['idBackground'] == '4':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).custom_image
            price['global_price'] += price['bg_price']
        elif data['idBackground'] == '3':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).radial_gradient
            price['global_price'] += price['bg_price']
        elif data['idBackground'] == '2':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).linear_gradient
            price['global_price'] += price['bg_price']
        elif data['idBackground'] == '1':
            price['bg_price'] = BackgroundPrice.objects.get(id=1).single_color
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
            price['ticker_price'] = TickerPrice.objects.get(id=1).color
            price['global_price'] += price['ticker_price']
    else:
        price['ticker_price'] = .0
        price['global_price'] += price['ticker_price']
    return JsonResponse(price)


# class FreeDice(APIView):
#     def get(self, request):
#         x = 20
#         y = 3
#         o = 0.245
#         a = (-o*x+sqrt(((o*x)**2)+(4*o*x)/y))/2
#         b = y-(1/a)
#         r = float("{:.2f}".format(random.uniform(0, 10)))
#         k = "{:.3f}".format((1/(o*r+a))+b)
#         win = float(k) * float(request.GET['bet'])

#         solana_client = Client('https://api.devnet.solana.com')


#         with open('id.json', 'r') as f:
#             lines = json.load(f)
#         key_from_file = [int(x) for x in lines]

#         keypair = Keypair(key_from_file[:32])

#         txn = Transaction().add(transfer(TransferParams(
#         from_pubkey=keypair.public_key, to_pubkey=PublicKey(request.GET['tokinId']), lamports=int(win * 1000000000))))
#         resp = solana_client.send_transaction(txn, keypair)

#         with open('wins_eng_free.json', 'r') as f:
#             text = random.choice(json.load(f))
#         text = text.replace("#name#", "jerom")
#         text = text.replace("#win#", str(win))
#         return Response({'win': text})



# class PremiumDice(APIView):
#     def get(self, request):
#         res = {}
#         x = 97
#         y = 76
#         o = 0.0099
#         a = (-o*x+sqrt(((o*x)**2)+(4*o*x)/y))/2
#         b = y-(1/a)
#         s = random.randint(1, 98)
#         if request.GET['isunder']:
#             if s <= int(request.GET['select']):
#                 k = "{:.3f}".format((1/((o*float(request.GET['select']))+a))+b+1)
#                 w = float(k) * float(request.GET['bet'])
#                 with open('wins_eng_prem.json', 'r') as f:
#                     text = random.choice(json.load(f)[0])
#                 if text.find('#name#') != -1:
#                     text.replace("#name#", "jerom")
#                 text = text.replace('#nonce#', str(s))
#                 text = text.replace("#win#", str(w))
#                 res['win'] = text

#                 solana_client = Client('https://api.devnet.solana.com')


#                 with open('id.json', 'r') as f:
#                     lines = json.load(f)
#                 key_from_file = [int(x) for x in lines]

#                 keypair = Keypair(key_from_file[:32])

#                 txn = Transaction().add(transfer(TransferParams(
#                 from_pubkey=keypair.public_key, to_pubkey=PublicKey(request.GET['tokinId']), lamports=int(w * 1000000000))))
#                 resp = solana_client.send_transaction(txn, keypair)
#             else:
#                 with open('wins_eng_prem.json', 'r') as f:
#                     text = random.choice(json.load(f)[1])
#                 text = text.replace('#nonce#', str(s))
#                 res['win'] = text
#         else:
#             ss = request.GET['select']*-1+99
#             if s > ss:
#                 k = "{:.3f}".format((1/((o*float(request.GET['select']))+a))+b+1)
#                 w = float(k) * float(request.GET['bet'])
#                 with open('wins_eng_prem.json', 'r') as f:
#                     text = random.choice(json.load(f)[0])
#                 if text.find('#name#') != -1:
#                     text.replace("#name#", "jerom")
#                 text = text.replace('#nonce#', str(s))
#                 text = text.replace("#win#", str(w))
#                 res['win'] = text
#                 solana_client = Client('https://api.devnet.solana.com')


#                 with open('id.json', 'r') as f:
#                     lines = json.load(f)
#                 key_from_file = [int(x) for x in lines]

#                 keypair = Keypair(key_from_file[:32])

#                 txn = Transaction().add(transfer(TransferParams(
#                 from_pubkey=keypair.public_key, to_pubkey=PublicKey(request.GET['tokinId']), lamports=int(w * 1000000000))))
#                 resp = solana_client.send_transaction(txn, keypair)
#             else:
#                 with open('wins_eng_prem.json', 'r') as f:
#                     text = random.choice(json.load(f)[1])
#                 text = text.replace('#nonce#', str(s))
#                 res['win'] = text
        
#         return Response(res)