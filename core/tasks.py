import json
from .models import *
import random
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
import subprocess
import base64
from jinja2 import Environment, FileSystemLoader, select_autoescape
from celery import shared_task
from aza.settings import RPC, DOMEN
from django.db import IntegrityError

def send_sol(to, s):
    solana_client = Client(RPC)


    with open('id.json', 'r') as f:
        lines = json.load(f)
    key_from_file = [int(x) for x in lines]

    keypair = Keypair(key_from_file[:32])

    txn = Transaction().add(transfer(TransferParams(
    from_pubkey=keypair.public_key, to_pubkey=PublicKey(to), lamports=s)))
    resp = solana_client.send_transaction(txn, keypair)
    return resp

def generator(n):
    s = ''
    for i in range(n):
        s = s + str(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz0123456789')[0])
    return s


@shared_task(bind=True)
def minttask(self, data, publickey):
    try:
        name = data['userObj']['name']
        date = data['userObj']['date']
        gender = 'Man' if data['userObj']['gender']=='0' else 'Woman'
        lang = 'English' if data['userObj']['language']=='0' else 'Russian'
        
        
        with open('core/token/avatar.txt', 'w') as f:
            f.write(data['userObj']['imgData'])
        result = subprocess.run('bundlr upload core/token/avatar.txt -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
        avatar_link = result.stdout.split()[5].decode('utf8').replace("'", '"')
        
        if data['idBodyColor'] == '2':
            if 'customImgData' in data:
                with open("core/token/custom.png", "wb") as fh:
                    fh.write(base64.b64decode(data['customImgData']))
                result = subprocess.run('bundlr upload core/token/custom.png -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
                body = ['',data['metalness'],data['roughness'],'',result.stdout.split()[5].decode('utf8').replace("'", '"'),'','','']
                
        elif data['idBodyColor'] == '1':
            if 'customBodyColor' in data:
                body = [data['customBodyColor'],data['metalness'],data['roughness'],'','','','','']
                
        elif data['idBodyColor'] == '3':
            if 'selectedImgId' in data:
                body = ['',data['metalness'],data['roughness'],'',SelectImageBody.objects.get(id=int(data['selectedImgId'])+1).link,'','','']
        
        elif data['idBodyColor'] == '4':
            if 'selectedMaterialId' in data:
                mater = Materials.objects.get(id=int(data['selectedMaterialId'])+1)
                body = ['',data['metalness'],data['roughness'],mater.roughness,mater.albedo,mater.normal]
                if mater.displacement == None:
                    body.append('')
                else:
                    body.append(mater.displacement)
                if mater.displacescale == None:
                    body.append('')
                else:
                    body.append(mater.displacescale)
                
        elif data['idBodyColor'] == '0':
            body = ['#1c1c1c',data['metalness'],data['roughness'],'','','','','']


        
        if 'idBackground' in data:
            if data['idBackground'] == '1':
                if 'backgroundColor' in data:
                    background = [data['backgroundColor'],'','','','','','']
                    
            elif data['idBackground'] == '2':
                if 'backgroundColor1' in data and 'backgroundColor2' in data:
                    background = ['',data['backgroundColor1'],data['backgroundColor2'],'','','','']
                    
            elif data['idBackground'] == '3':
                if 'backgroundColor3' in data and 'backgroundColor4' in data:
                    background = ['','','',data['backgroundColor3'],data['backgroundColor4'],'','']
                    
            elif data['idBackground'] == '4':
                if 'customBgImgData' in data:
                    with open('core/token/custom.txt','w') as f:
                        f.write(data['customBgImgData'])
                    result = subprocess.run('bundlr upload core/token/custom.txt -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
                    background = ['','','','','',result.stdout.split()[5].decode('utf8').replace("'", '"'),'']
                    
            elif data['idBackground'] == '5':
                if 'selectedBgImgId' in data:
                    background = ['','','','','','',SelectImageBackground.objects.get(id=int(data['selectedBgImgId'])+1).link]
                    

            elif data['idBackground'] == '0':
                background = ['#0A3104','','','','','','']
        else:
            data['idBackground'] = '0'
            background = ['#0A3104','','','','','','']
                
        
        
        if 'tickerColor' in data:
            ticker = data['tickerColor']
        else:
            ticker = '#004f20'
        
        if 'mId' not in data:
            model = Models.objects.get(id=1)
            model_name = model.name
            model_link = model.link
            curve = model.curve_radius
        else:
            model = Models.objects.get(id=int(data['mId'])+1)
            model_name = model.name
            model_link = model.link
            curve = model.curve_radius
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        template = env.get_template('core/token/render.html')
        
        if lang == 'English':
            with open("tick_eng_link.json", "r") as f:
                tick_path = random.choice(json.load(f))
        else:
            with open("tick_rus_link.json", "r") as f:
                tick_path = random.choice(json.load(f))
        

        config_len = str(MintCount.objects.get(id=1).general_sum)
        if len(config_len) < 5:
            config_len = str((5 - len(config_len)) * '0') + config_len

        rendered_page = template.render(
            user_name = name,
            birthday = date,
            avatar = avatar_link,
            user_number = '#' + config_len,
            ball_name = model_name,
            ball_url = model_link,
            body_pam = body,
            back_pam = background,
            back_type = int(data['idBackground'])-1 if data['idBackground']!='0' else data['idBackground'],
            curve_radius = curve,
            tick = ticker,
            ticker_path = tick_path,
            hat = True if model_link == 'https://arweave.net/54_M2OvAOnO-vKmL34wE0QxPFKcl6KgHIlWxBotnpS4' else False
        )
        type_body = ['Default','Custom color', 'Custom image', 'Select image', 'Material']
        type_back = ['Default','Single color', 'Linear gradient', 'Radial gradient', 'Custom image', 'Select image']
        with open('core/token/token.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)
        
        result = subprocess.run('bundlr upload core/token/token.html -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
        html = result.stdout.split()[5].decode('utf8').replace("'", '"') + '?ext=html'
        with open("core/token/screenshot.png", "wb") as fh:
            fh.write(base64.b64decode(data['screenshot']))
        result = subprocess.run('bundlr upload core/token/screenshot.png -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
        screenshot = result.stdout.split()[5].decode('utf8').replace("'", '"') + '?ext=png'
        metadata = {}
        metadata['name'] = f"Azagnat #{config_len}"
        metadata['symbol'] = 'AZGT'
        metadata['description'] = 'Non-fungible Magic Ball'
        metadata['image'] = screenshot
        metadata['animation_url'] = html
        metadata['external_url'] = 'https://azagnat.top'
        a = []
        a.append({'trait_type' : 'Name', 'value': name})
        a.append({'trait_type' : 'Date of Birth', 'value': date})
        a.append({'trait_type' : 'Gender', 'value': gender})
        a.append({'trait_type' : 'Language', 'value': lang})
        a.append({'trait_type' : 'Ball_name', 'value': model_name})
        value = '#1c1c1c'
        if data['idBodyColor'] == '1':
            value = data['customBodyColor']
        elif data['idBodyColor'] == '2':
            value = 'Custom image'
        elif data['idBodyColor'] == '3':
            value = SelectImageBody.objects.get(id=int(data['selectedImgId'])+1)
        elif data['idBodyColor'] == '4':
            value = Materials.objects.get(id=int(data['selectedMaterialId'])+1).name

        a.append({'trait_type' : 'Body_view', 'value': value})
        value = '#0A3104'
        if data['idBackground'] == '1':
            value = data['backgroundColor']
        elif data['idBackground'] == '2':
            value = data['backgroundColor1'] + ' ' + data['backgroundColor2']
        elif data['idBackground'] == '3':
            value = data['backgroundColor3'] + ' ' + data['backgroundColor4']
        elif data['idBackground'] == '4':
            value = 'Custom image'
        elif data['idBackground'] == '5':
            value = SelectImageBackground.objects.get(id=int(data['selectedBgImgId'])+1).name
        
        a.append({'trait_type' : 'Background', 'value': value})
        if 'tickerColor' in data:
            a.append({'trait_type' : 'Ticker', 'value': ticker})
        else:
            a.append({'trait_type' : 'Ticker', 'value': ticker})
        metadata['attributes'] = a
        with open('core/token/metadata.json', 'w') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        
        result = subprocess.run('bundlr upload core/token/metadata.json -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
        metadata_url = result.stdout.split()[5].decode('utf8').replace("'", '"')
        d = {}
        d['name'] = f"Azagnat #{config_len}"
        d['symbol'] = 'AZGT'
        d['uri'] = metadata_url
        d['seller_fee_basis_points'] = 777
        d['creators'] = [{"address": "AzagnattdNF4kiZnQDDXhmpQ9FgGUb9ZGTJouEACjGj7", "verified": True, "share": 100}]
        with open('core/token/ex.json', 'w') as f:
            json.dump(d, f, indent=4, ensure_ascii=False)

        res = subprocess.run(f"metaboss mint one -r {RPC} --keypair id.json --nft-data-file core/token/ex.json --receiver {publickey}", shell=True, stdout=subprocess.PIPE)
        contract = res.stdout.split()[5].decode('utf8').replace("'", '"')
    except BaseException as e:
        raise self.retry(exc=e, countdown=2) 
    else:
        config = Config()
        config.address_id = publickey
        config.token_id = MintCount.objects.get(id=1).general_sum
        config.metadata = metadata
        config.avatar = data['userObj']['imgData']
        if data['idBackground'] == '4':
            config.background = data['customBgImgData']
        if data['idBodyColor'] == '2':
            config.body_view = data['customImgData']
        config.html = html
        config.cost = "{:.3f}".format(data['global_price'])
        config.contract = contract
        if 'r' in data['get_par']:
            config.whatref = data['get_par']['r']
        elif 'p' in data['get_par']:
            config.whatpro = data['get_par']['p']
        elif 'a' in data['get_par']:
            config.whatamb = data['get_par']['a']
        config.base_cost = BasePrice.objects.get(id=1).price
        config.save()

        ref_code = RefferalCode()
        ref_code.config = Address.objects.get(address=publickey)
        ref_code.code = generator(8)
        try:
            ref_code.save()
        except IntegrityError:
            pass
        
        if 'r' in data['get_par']:
            baseprice = BasePrice.objects.get(id=1).price
            a = RefferalCode.objects.get(code=data['get_par']['r'])
            res = send_sol(a.config.address.address, int((baseprice*0.1)*1000000000))
            r = RefferalCode.objects.get(code=data['get_par']['r'])
            r.paid = r.paid + (baseprice*0.1)
            r.deals = r.deals + 1
            r.save()
            re = Returned.objects.get(id=1)
            re.count = re.count + (baseprice*0.1)
            re.save()
        elif 'p' in data['get_par']:
            p = Promocode.objects.get(code=f'{DOMEN}?p='+data['get_par']['p'])
            p.delete()
        elif 'a' in data['get_par']:
            baseprice = BasePrice.objects.get(id=1).price
            a = Ambassador.objects.get(code=f'{DOMEN}?a='+data['get_par']['a'])
            res = send_sol(a.address.address, int((baseprice*a.percent/100)*1000000000))
            re = Returned.objects.get(id=1)
            re.count = re.count + (baseprice*0.2)
            re.save()
        elif 'e' in data['get_par']:
            e = EasyMint.objects.get(code=f'{DOMEN}?p='+data['get_par']['e'])
            e.delete()

    return config_len
        

