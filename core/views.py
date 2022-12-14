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
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from nacl.public import PrivateKey, PublicKey
import base58
import logging


logger = logging.getLogger('django')




month = ['','January','February','March','April','May','June','July','August','September','Octomber','November','December']

def generator(n):
    s = ''
    for i in range(n):
        s = s + str(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz0123456789')[0])
    return s

def enc(num, guide):
    old = 0
    fib_old = 0
    fib = guide

    data = []

    i = 0

    length = len(str(num))

    while i < length:
        fib_old = fib
        fib = fib + old
        char = int(str(num)[i])
        data.append((char+fib)+(fib*char))
        old = fib_old
        i+=1
    return data


def homepage(request):
    logger.info('azagnat')
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


def explorer(request):
    return render(request, 'explorer/explorer.html')

def deepconnect(request):
    secretKeyNew = PrivateKey.generate()
    p = str(base58.b58encode(bytes(secretKeyNew.public_key)))
    return render(request, 'explorer/connect.html', {'publickey': p[2:len(p)-1]})

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
    
    return JsonResponse()


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