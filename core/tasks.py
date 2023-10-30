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
from jinja2 import Environment as Env, FileSystemLoader, select_autoescape
from celery import shared_task
from aza.settings import RPC, DOMEN, DEBUG
from django.db import IntegrityError
import os
import random

def send_sol(to, s):
    solana_client = Client(random.choice(RPC))


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
    if 'p' in data['get_par']:
        try:
            Promocode.objects.get(code=f'{DOMEN}?p='+data['get_par']['p'])
        except Promocode.DoesNotExist:
            return
    elif 'e' in data['get_par']:
        try:
            EasyMint.objects.get(code=f'{DOMEN}?e='+data['get_par']['e'])
        except EasyMint.DoesNotExist:
            return
        
    if "font" in data:
        font = Font.objects.get(url=data["font"])
    else:
        font = Font.objects.get(id=2)
    
    if "env" in data:
        environment = Environment.objects.get(url=data["env"])
    else:
        environment = Environment.objects.get(id=2)

    try:
        name = data['userObj']['name']
        date = data['userObj']['date']
        gender = 'Man' if data['userObj']['gender'] == '0' else 'Woman'
        lang = 'English' if data['userObj']['language'] == '0' else 'Russian'

        config_len = str(MintCount.objects.get(id=1).general_sum)
        if len(config_len) < 5:
            config_len = str((5 - len(config_len)) * '0') + config_len


        path = os.path.join("/var/www/token/" if not DEBUG else "token/", config_len)

        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        
        with open(f"/var/www/token/{config_len}/avatar.txt" if not DEBUG else f"token/{config_len}/avatar.txt", 'w') as f:
            f.write(data['userObj']['imgData'])
        result = subprocess.run(f'bundlr upload {f"/var/www/token/{config_len}/avatar.txt" if not DEBUG else f"token/{config_len}/avatar.txt"} -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
        avatar_link = result.stdout.decode().split()[5]
        
        if data['idBodyColor'] == '2':
            if 'customImgData' in data:
                with open(f"/var/www/token/{config_len}/custom.png" if not DEBUG else f"token/{config_len}/custom.png", "wb") as fh:
                    fh.write(base64.b64decode(data['customImgData']))
                result = subprocess.run(f'bundlr upload {f"/var/www/token/{config_len}/custom.png" if not DEBUG else f"token/{config_len}/custom.png"} -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
                body = ['', data['metalness'], data['roughness'], '', result.stdout.decode().split()[5], '', '', '']
                
        elif data['idBodyColor'] == '1':
            if 'customBodyColor' in data:
                body = [data['customBodyColor'], data['metalness'], data['roughness'], '', '', '', '', '']
                
        elif data['idBodyColor'] == '3':
            if 'selectedImgId' in data:
                body = ['', data['metalness'], data['roughness'], '', SelectImages.objects.last().data[0]["backgroundImages"][int(data["selectedImgId"])]["path"], '', '', '']
        
        elif data['idBodyColor'] == '4':
            if 'selectedMaterialId' in data:
                mater = Materials.objects.last().data[int(data['selectedMaterialId'])]
                body = ['', data['metalness'], data['roughness'], mater["roughnessMap"], mater["map"], mater["normalMap"]]
                if "displacementMap" not in mater:
                    body.append('')
                else:
                    body.append(mater["displacementMap"])
                if "displacementScale" not in mater:
                    body.append('')
                else:
                    body.append(mater["displacementScale"])
                
        elif data['idBodyColor'] == '0':
            body = ['#1c1c1c', data['metalness'], data['roughness'], '', '', '', '', '']


        
        if 'idBackground' in data:
            if data['idBackground'] == '1':
                if 'backgroundColor' in data:
                    background = [data['backgroundColor'], '', '', '', '', '', '']
                    
            elif data['idBackground'] == '2':
                if 'backgroundColor1' in data and 'backgroundColor2' in data:
                    background = ['', data['backgroundColor1'], data['backgroundColor2'], '', '', '', '']
                    
            elif data['idBackground'] == '3':
                if 'backgroundColor3' in data and 'backgroundColor4' in data:
                    background = ['', '', '', data['backgroundColor3'], data['backgroundColor4'], '', '']
                    
            elif data['idBackground'] == '4':
                if 'customBgImgData' in data:
                    with open(f"/var/www/token/{config_len}/custom.txt" if not DEBUG else f"token/{config_len}/custom.txt",'w') as f:
                        f.write(data['customBgImgData'])
                    result = subprocess.run(f'bundlr upload {f"/var/www/token/{config_len}/custom.txt" if not DEBUG else f"token/{config_len}/custom.txt"} -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
                    background = ['', '', '', '', '', result.stdout.decode().split()[5], '']
                    
            elif data['idBackground'] == '5':
                if 'selectedBgImgId' in data:
                    background = ['', '', '', '', '', '', SelectImages.objects.last().data[0]["backgroundImages"][int(data["selectedBgImgId"])]["path"]]
                    

            elif data['idBackground'] == '0':
                background = ['#0A3104', '', '', '', '', '', '']
        else:
            data['idBackground'] = '0'
            background = ['#0A3104', '', '', '', '', '', '']
                
        
        
        if 'tickerColor' in data:
            ticker = data['tickerColor']
        else:
            ticker = '#004f20'

        with open("data/add-materials.json", "r") as f:
            hats = json.load(f)
        
        hat_data = {}

        if data["model"] == None:
            model = Models.objects.last().data[0]
            model_name = model["name"]
            model_link = model["local-path"]
            curve = model["Bend"]
            speed = model["speed"]
            shiftGlass = model["shiftGlass"]
            fontSize = model["fontSize"]
            LocX = model["LocX"]
            LocY = model["LocY"]
            PosZ = model["PosZ"]
            if "hat" in model:
                hat_data["add-name"] = "Hat"
                hat_data["add-color"] = hats[model["hat"]]["color"]
                hat_data["add-metalness"] = hats[model["hat"]]["metalness"]
                hat_data["add-roughness"] = hats[model["hat"]]["roughness"]
                hat_data["add-r-map"] = hats[model["hat"]]["roughnessMap"]
                hat_data["add-albedo"] = hats[model["hat"]]["map"]
                hat_data["add-normal"] = hats[model["hat"]]["normalMap"]
                hat_data["add-disp"] = hats[model["hat"]]["displacementMap"]
                hat_data["add-dispScale"] = hats[model["hat"]]["displacementScale"]
                hat_data["add-envMapIntensity"] = hats[model["hat"]]["envMapIntensity"]
                hat_data["flipY"] = hats[model["hat"]]["flipY"]

            
        else:
            model = Models.objects.last().data[int(data["model"])]
            model_name = model["name"]
            model_link = model["local-path"]
            curve = model["Bend"]
            speed = model["speed"]
            shiftGlass = model["shiftGlass"]
            fontSize = model["fontSize"]
            LocX = model["LocX"]
            LocY = model["LocY"]
            PosZ = model["PosZ"]
            if "hat" in model:
                hat_data["add-name"] = "Hat"
                hat_data["add-color"] = hats[model["hat"]]["color"]
                hat_data["add-metalness"] = hats[model["hat"]]["metalness"]
                hat_data["add-roughness"] = hats[model["hat"]]["roughness"]
                hat_data["add-r-map"] = hats[model["hat"]]["roughnessMap"]
                hat_data["add-albedo"] = hats[model["hat"]]["map"]
                hat_data["add-normal"] = hats[model["hat"]]["normalMap"]
                hat_data["add-disp"] = hats[model["hat"]]["displacementMap"]
                hat_data["add-dispScale"] = hats[model["hat"]]["displacementScale"]
                hat_data["add-envMapIntensity"] = hats[model["hat"]]["envMapIntensity"]
                hat_data["flipY"] = hats[model["hat"]]["flipY"]


        env = Env(
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
        

        rendered_page = template.render(
            user_name = name,
            birthday = date,
            avatar = avatar_link,
            ball_name = model_name,
            ball_url = model_link,
            body_pam = body,
            back_pam = background,
            back_type = int(data['idBackground'])-1 if data['idBackground']!='0' else data['idBackground'],
            curve_radius = curve,
            speed = speed,
            shiftGlass = shiftGlass,
            fontSize = fontSize,
            LocY = LocY,
            LocX = LocX,
            PosZ = PosZ,
            tick = ticker,
            env = environment.url,
            font = font.url,
            ticker_path = tick_path,
            hat = True if "hat" in model else False,
            hat_data = json.dumps([hat_data])
        )

        with open(f"/var/www/token/{config_len}/token.html" if not DEBUG else f"token/{config_len}/token.html", 'w', encoding="utf8") as file:
            file.write(rendered_page)
        
        result = subprocess.run(f'bundlr upload {f"/var/www/token/{config_len}/token.html" if not DEBUG else f"token/{config_len}/token.html"} -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
        html = result.stdout.decode().split()[5] + '?ext=html'
        with open(f"/var/www/token/{config_len}/screenshot.png" if not DEBUG else f"token/{config_len}/screenshot.png", "wb") as fh:
            fh.write(base64.b64decode(data['screenshot']))
        result = subprocess.run(f'bundlr upload {f"/var/www/token/{config_len}/screenshot.png" if not DEBUG else f"token/{config_len}/screenshot.png"} -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
        screenshot = result.stdout.decode().split()[5] + '?ext=png'
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
        a.append({'trait_type' : 'Environment', 'value': environment.name})
        a.append({'trait_type' : 'Font', 'value': font.name})

        value = '#1c1c1c'
        if data['idBodyColor'] == '1':
            value = data['customBodyColor']
        elif data['idBodyColor'] == '2':
            value = data["bodyCustomName"]
        elif data['idBodyColor'] == '3':
            value = SelectImages.objects.last().data[0]["bodyImages"][int(data["selectedImgId"])]["name"]
        elif data['idBodyColor'] == '4':
            value = Materials.objects.last().data[int(data['selectedMaterialId'])]["name"]

        a.append({'trait_type' : 'Body_view', 'value': value})
        value = '#0A3104'
        if data['idBackground'] == '1':
            value = data['backgroundColor']
        elif data['idBackground'] == '2':
            value = data['backgroundColor1'] + ' ' + data['backgroundColor2']
        elif data['idBackground'] == '3':
            value = data['backgroundColor3'] + ' ' + data['backgroundColor4']
        elif data['idBackground'] == '4':
            value = data["backgroundCustomName"]
        elif data['idBackground'] == '5':
            value = SelectImages.objects.last().data[0]["backgroundImages"][int(data["selectedBgImgId"])]["name"]
        
        a.append({'trait_type' : 'Background', 'value': value})
        if 'tickerColor' in data:
            a.append({'trait_type' : 'Ticker', 'value': ticker})
        else:
            a.append({'trait_type' : 'Ticker', 'value': ticker})
        metadata['attributes'] = a
        with open(f"/var/www/token/{config_len}/metadata.json" if not DEBUG else f"token/{config_len}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        
        result = subprocess.run(f'bundlr upload {f"/var/www/token/{config_len}/metadata.json" if not DEBUG else f"token/{config_len}/metadata.json"} -h https://node1.bundlr.network -w wallet.json -c arweave', shell=True, stdout=subprocess.PIPE)
        metadata_url = result.stdout.decode().split()[5]
        d = {}
        d['name'] = f"Azagnat #{config_len}"
        d['symbol'] = 'AZGT'
        d['uri'] = metadata_url
        d['seller_fee_basis_points'] = 777
        d['creators'] = [{"address": "AzagnattdNF4kiZnQDDXhmpQ9FgGUb9ZGTJouEACjGj7", "verified": True, "share": 100}]
        with open(f"/var/www/token/{config_len}/ex.json" if not DEBUG else f"token/{config_len}/ex.json", 'w') as f:
            json.dump(d, f, indent=4, ensure_ascii=False)

        res = subprocess.run(f"metaboss mint one -r {random.choice(RPC)} --keypair {'/root/azagnat/id.json' if not DEBUG else 'id.json'} --nft-data-file {f'/var/www/token/{config_len}/ex.json' if not DEBUG else f'token/{config_len}/ex.json'} --receiver {publickey}", shell=True, stdout=subprocess.PIPE)
        contract = res.stdout.decode().split()[5]
    except BaseException as e:
        ob = NotMinted()
        ob.token_id = MintCount.objects.get(id=1).general_sum
        ob.data = d
        if 'r' in data['get_par']:
            ob.code = f"r={data['get_par']['r']}"
        elif 'p' in data['get_par']:
            ob.code = f"p={data['get_par']['p']}"
        elif 'a' in data['get_par']:
            ob.code = f"a={data['get_par']['a']}"
        elif 'e' in data['get_par']:
            ob.code = f"e={data['get_par']['e']}"
    else:
        config = Config()
        config.address_id = publickey
        config.name = name
        config.token_id = MintCount.objects.get(id=1).general_sum
        config.metadata = d
        config.cost = "{:.3f}".format(data['global_price'])
        config.contract = contract        
        config.save()

        ref_code = RefferalCode()
        ref_code.config = Address.objects.get(address=publickey)
        ref_code.code = generator(8)
        try:
            ref_code.save()
        except IntegrityError:
            pass
        
        if 'r' in data['get_par']:
            a = RefferalCode.objects.get(code=data['get_par']['r'])
            res = send_sol(a.config.address, int((data['global_price'] * 0.1) * 1000000000))
            r = RefferalCode.objects.get(code=data['get_par']['r'])
            r.paid = r.paid + (data['global_price'] * 0.1)
            r.deals = r.deals + 1
            r.save()
            re = Returned.objects.get(id=1)
            re.count = re.count + (data['global_price'] * 0.1)
            re.save()
        elif 'p' in data['get_par']:
            p = Promocode.objects.get(code=f'{DOMEN}?p='+data['get_par']['p'])
            p.delete()
        elif 'a' in data['get_par']:
            a = Ambassador.objects.get(code=f'{DOMEN}?a='+data['get_par']['a'])
            res = send_sol(a.address.address, int((data['global_price'] * a.royality / 100) * 1000000000))
            re = Returned.objects.get(id=1)
            re.count = re.count + (data['global_price'] * a.royality / 100)
            re.save()
        elif 'e' in data['get_par']:
            e = EasyMint.objects.get(code=f'{DOMEN}?e='+data['get_par']['e'])
            e.delete()

    return config_len
        

