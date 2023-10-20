from typing import Any
from django.db import models
import os
import json
import random
from aza.settings import DOMEN

def generator(n):
    s = ''
    for i in range(n):
        s = s + str(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz0123456789')[0])
    return s

class Address(models.Model):
    address = models.CharField(max_length=100, unique=True, primary_key=True)
    date_auth = models.DateTimeField(auto_now_add=True)
    date_in = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = "Addresses"


    def __str__(self):
        return self.address


class Config(models.Model):
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=256)
    metadata = models.JSONField()
    token_id = models.PositiveIntegerField()
    avatar = models.CharField(max_length=5200000)
    background = models.CharField(max_length=5200000, null=True, blank=True)
    body_view = models.CharField(max_length=5200000, null=True, blank=True)
    html = models.URLField()
    cost = models.FloatField()
    whatref = models.CharField(null=True, blank=True, max_length=8)
    whatpro = models.CharField(null=True, blank=True, max_length=8)
    whatamb = models.CharField(null=True, blank=True, max_length=8)
    contract = models.CharField(max_length=500, primary_key=True)
    date_minted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Config'
        verbose_name_plural = "Configs"

    def __str__(self):
        return self.contract



class RefferalCode(models.Model):
    config = models.OneToOneField(
        Address,
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=10, unique=True)
    paid = models.FloatField(default=0)
    deals = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '1. Refferal code'
        verbose_name_plural = "1. Refferal codes"

    def __str__(self):
        return self.code


class Promocode(models.Model):
    code = models.URLField(unique=True, null=True, blank=True)
    percent = models.PositiveIntegerField()


    def save(self):
        if self.code == None:
            self.code = DOMEN + '?p=' + generator(8)
        
        super().save()

    class Meta:
        verbose_name = '3. Promocode'
        verbose_name_plural = "3. Promocodes"

    def __str__(self):
        return self.code


class Ambassador(models.Model):
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=128)
    code = models.URLField(unique=True, null=True, blank=True)
    discount = models.IntegerField()
    royality = models.IntegerField()


    def save(self):
        if self.code == None:
            self.code = DOMEN + '?a=' + generator(8)
        
        super().save()

    class Meta:
        verbose_name = '2. Ambassador'
        verbose_name_plural = "2. Ambassadors"

    def __str__(self):
        return self.code
    

class EasyMint(models.Model):
    code = models.URLField(unique=True, null=True, blank=True)


    def save(self):
        if self.code == None:
            self.code = DOMEN + '?e=' + generator(8)
        
        super().save()

    class Meta:
        verbose_name = '4. Easy mint code'
        verbose_name_plural = "4. Easy mint codes"

    def __str__(self):
        return self.code

    
#==============================
#images and glb

class Models(models.Model):
    data = models.JSONField(default=[
        {
            "name": "Ostan",
            "local-path": "https://arweave.net/RxtNv0UnhR7dUICf8ZjqMa7IlTpgHMilM055tx_5syk",
            "price": 0.0,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Hiron",
            "local-path": "https://arweave.net/1t1qEGTTEiNHUjQZNzEvVTr9iGdHM7rY7kB1_PMQisU",
            "price": 0.01,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Vesta",
            "local-path": "https://arweave.net/5zGsUDLdYTkkPB_pdvJDxAM-UbqUmDU4KbHtCEKqjcY",
            "price": 0.02,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Beroz",
            "local-path": "https://arweave.net/koa1zxvzpfTtyBlLamuIENU5Li_gj50irMvivHl-nqI",
            "price": 0.02,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Vega",
            "local-path": "https://arweave.net/7RP_jxbF3V4G-ht1HXWmRjwSwnsL-tbL_n0gXeQw9wE",
            "price": 0.03,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Joulupukki",
            "local-path": "https://arweave.net/54_M2OvAOnO-vKmL34wE0QxPFKcl6KgHIlWxBotnpS4",
            "hat": 0,
            "price": 0.03,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Maradona",
            "local-path": "https://arweave.net/kSQLBRS6dWyXnn1z4WTRu4mLiyPHRLe7bg4SkUh940o",
            "price": 0.03,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Star",
            "local-path": "https://arweave.net/Kg2PcSqR6yi4EnS40VNwaX-C7cFg-2kgBQR8hB2Eivw",
            "price": 0.03,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Pokeball",
            "local-path": "https://arweave.net/jIIRbgLKUNCMMV-66UHHy2VtB4-vJSm-qvTCw-S7qJk",
            "price": 0.03,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Icosa",
            "local-path": "https://arweave.net/6yCVyyCK159gbEi56-hNH9TQl1NYr-_qWxbcxt4YSok",
            "price": 0.03,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        },
        {
            "name": "Rock",
            "local-path": "https://arweave.net/4Ki4RFg_ZmBmuCVonuqSbPRj5PJgqxcl0jYkOV33Lxs",
            "hat": 1,
            "price": 0.03,
            "PozZ" : 32,
            "LocY" : -10,
            "LocX" : -14,
            "Bend" : -30,
            "shiftGlass": 0.1,
            "fontSize": 5,
            "speed": 10
        }
    ])

    def save(self):
        super().save()

        with open("data/models.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

        

        
    class Meta:
        verbose_name = 'Model'
        verbose_name_plural = "Models"

class Hat(models.Model):
    data = models.JSONField(default=[
    {
        "color" : "#ffffff",
        "metalness": 1,
        "roughness": 1,
        "roughnessMap"  : "https://arweave.net/wUqIxu-by-swZPuCg1raaYBJEr8RvCNNGGRnVf25Bh4",
        "map" : "https://arweave.net/6k2vpDLjLj5IJci_yOuU2wSWKv3FRPQ_d6gqqjWXUEQ",
        "normalMap" : "https://arweave.net/HbEPamzgLLte07Z7B0H3YzJ0vfIang6H5ijgjZI4AeM",
        "displacementMap"   : "",
        "displacementScale" : "",
        "envMapIntensity" : 2,
        "flipY": True
    },
    {
        "color" : "#ffffff",
        "metalness": 1,
        "roughness": 1,
        "roughnessMap"  : "https://arweave.net/7UySi14E_ZTqRQlzjI9THLCE49JGw1OZT-glWyzltsQ",
        "map" : "https://arweave.net/gRGm6t1jY9JQckEEaznTpa6YlnRl4P8140hGKdBG0lc",
        "normalMap" : "https://arweave.net/dL72U0-qz-yn4sZnhJO29F1PH84WHRI-QfY0664rV00",
        "displacementMap"   : "",
        "displacementScale" : "",
        "envMapIntensity" : 2,
        "flipY": False
    },
    {
        "color": "#ffffff",
        "metalness": 1,
        "roughness": 1,
        "roughnessMap":      "https://arweave.net/uFQL34uuYCBIOkB-SWYldLcuijEBcyVz5R1nqyQBoeo", 
        "map":               "https://arweave.net/h54414i1wpY1e3ezqFe6xBD55HnJ-9hjAV-OvATAauM",
        "normalMap":         "https://arweave.net/wNg7XexkW-EZCLQB2XUi9Lzousa2yd5hjV8pH-bZBT4",
        "displacementMap":   "",
        "displacementScale": "",
        "envMapIntensity": 2,
        "flipY": False
    }
    ])

    def save(self):
        super().save()

        with open("data/add-materials.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

        

        
    class Meta:
        verbose_name = 'Hat'
        verbose_name_plural = "Hats"

class Materials(models.Model):
    data = models.JSONField(default=[
        {
            "id": 0,
            "name": "Golden scr.",
            "map": "https://arweave.net/Q4ZEe6PeFpXdYTa2NHOFUeCQQHKoJDxedLnVajQ7J5g",
            "normalMap": "https://arweave.net/2ZE6DAGKlabJl5dYSzqAjglm-NcpheVYsZbgrndPI60",
            "roughnessMap": "https://arweave.net/PxXXrrZrtvoFPzXjeBmj-WI7EIYNvZB4B-g7A9532Os",
            "metalness": 1.0,
            "roughness": 1.0,
            "price": 0.1
        },
        {
            "id": 1,
            "name": "Violet crystal",
            "map": "https://arweave.net/9C-XpPo21lj9aSm78GBw3zX3k_t-ilOkjqARp-5xEGM",
            "normalMap": "https://arweave.net/ndw1EPyUxH7jhB4uJOIFtFdKW4s3XjDmRftS9a_yHqY",
            "roughnessMap": "https://arweave.net/27kLNmoQxER3L3xvlNYgH7RoTmpDLNZzYLR4yNpbR3c",
            "metalness": 0.16,
            "roughness": 1.0,
            "price": 0.2
        },
        {
            "id": 2,
            "name": "Metal scr.",
            "map": "https://arweave.net/c9xN9FVzfqzSA3X91DsuRdAdal0rj1b7S3Zez9dFtYc",
            "normalMap": "https://arweave.net/SpJ8tilMij2OT3MNVTnSA3QJtrWzVRyLYJFVHlxEcsY",
            "roughnessMap": "https://arweave.net/Xxlj0jZo_m_IsIYPUX7UpjCbwD8nvJ7_ddigw7n35LY",
            "metalness": 1.0,
            "roughness": 1.0,
            "price": 0.3
        },
        {
            "id": 3,
            "name": "Wood",
            "map": "https://arweave.net/vP8OH4j93GiuZAfnEuDVIkBjeN9NqkaIMceU-1DysxQ",
            "normalMap": "https://arweave.net/5-fjpVJ03Qjly6X7s0lePnM_BY3SlYGsAJOBqoygKMQ",
            "roughnessMap": "https://arweave.net/Qdu9D0r440jg1KVSztrtcm_NnaaAGXbDzGxPXm3stlc",
            "metalness": 0.0,
            "roughness": 1.0,
            "price": 0.4
        },
        {
            "id": 4,
            "name": "Walnut wood",
            "map": "https://arweave.net/zgMfoEvrEYVOMlaPIQ0OMfo0DbFICsziwSWn9Y-_8gE",
            "normalMap": "https://arweave.net/vQto9YanPRzhnHEFRRePXD-zWTePG3-MxyQ5FpBOuFo",
            "roughnessMap": "https://arweave.net/ch5QLG55OQylBESvDHNj8ZylPwjRdiUBAk2ZUuaNAzA",
            "metalness": 0.0,
            "roughness": 1.0,
            "price": 0.5
        },
        {
            "id": 5,
            "name": "Concrete",
            "map": "https://arweave.net/2G8tSc1nNUCcXdMBfAgk7p0rrR_BPfxHl9xX_kn0uBg",
            "normalMap": "https://arweave.net/QLjfu2ZXjRHKk53rju19OWK9Jcz_qzhUI4EfEVhbfFU",
            "roughnessMap": "https://arweave.net/qhLCsN71I50LYx04daXjuUV6MnADqbBz66Cyzkj4tyg",
            "metalness": 0.35,
            "roughness": 1.0,
            "price": 0.6
        },
        {
            "id": 6,
            "name": "Darck cracks",
            "map": "https://arweave.net/J940vo41iFWwAbuCbQgwYkkOg3gKMsRVtt0iqmObz9c",
            "normalMap": "https://arweave.net/zhME-6ll9DFpmUNHL6asMP6Ppt6C3GoMilIUieAXALc",
            "roughnessMap": "https://arweave.net/YN8UpVjpVtry-Fba7zvuJfkJ5YIGVEfQoaDjtfrVV8M",
            "metalness": 1.0,
            "roughness": 1.0,
            "price": 0.7
        },
        {
            "id": 7,
            "name": "Plastic line",
            "map": "https://arweave.net/k53jsVxDwEpjAFAIdv1v4QrcjIg8FP6RXTSL7uJTRrM",
            "normalMap": "https://arweave.net/OL2upxh1lwiHNYgEIJgcyZtUm0XcUrJ-uD8aUW-XmtY",
            "roughnessMap": "https://arweave.net/OlRIUwBh4GHkOFWvcCuxqBx4nAbWg_G4nob4PNxqMlY",
            "metalness": 0.0,
            "roughness": 1.0,
            "price": 0.8
        },
        {
            "id": 8,
            "name": "Cow fur",
            "map": "https://arweave.net/xXVB5_jIMOV6tYkj97jTkOeMO705I-nNWoqQMalJpAw",
            "normalMap": "https://arweave.net/4mMS1WFL3EJpYDuBq4yWIMY2zF7WjDRFiDo_XMtB7jk",
            "roughnessMap": "https://arweave.net/gGVTkHfDmOBZSlWjdo06JsX2UINvmXNCORMyH6VvLbo",
            "metalness": 0.0,
            "roughness": 1.0,
            "price": 0.9
        },
        {
            "id": 9,
            "name": "Maple wood",
            "map": "https://arweave.net/sCfPurEYWsJNTTKGtSlsAFffborVu-tw6YfOHAzokWw",
            "normalMap": "https://arweave.net/9ZUIIxkY_fFKEgAVmwa3ydFyeMtSk1GXM3kfh-kkP18",
            "roughnessMap": "https://arweave.net/7rzU5hXd6s1710rbirwXDq2r5xFtymRW_mGRaWeYfLA",
            "metalness": 0.1,
            "roughness": 1.0,
            "price": 0.11
        },
        {
            "id": 10,
            "name": "Oxidized copper",
            "map": "https://arweave.net/KOYLiS6W73noAJT6QoFD5lXG78IDRp3-JPx0ZrY0lmE",
            "normalMap": "https://arweave.net/dhlLVWMqOfYtvQ-ZfVgNky5Id4MfHpAPwBNxYFTSo74",
            "roughnessMap": "https://arweave.net/bYE4v_8R2ZXVaS_H_qMLV7D8Z-cNlUUMDFEdAzQhf6Y",
            "metalness": 1.0,
            "roughness": 1.0,
            "price": 0.12
        },
        {
            "id": 11,
            "name": "Carbon fiber",
            "map": "https://arweave.net/CCdiegpZ4SELC0yyL1v_hY9e3r-Jjtx505kDOTmNjWY",
            "normalMap": "https://arweave.net/fivUFYgY925qZP1FJzBI0MVr4oOhjvOTPxn8RuMFzXQ",
            "roughnessMap": "https://arweave.net/otqnMrH2UKG2rj92fzDwnzCYhWlxcpcklyJqPxXN36o",
            "metalness": 0.6,
            "roughness": 1.0,
            "price": 0.13
        },
        {
            "id": 12,
            "name": "Copper hammered",
            "map": "https://arweave.net/-8T9bGZSNkDSOTa-JbsbFdJqO2fz97rmjBXB7n_7iDo",
            "normalMap": "https://arweave.net/-8T9bGZSNkDSOTa-JbsbFdJqO2fz97rmjBXB7n_7iDo",
            "roughnessMap": "https://arweave.net/0XaJnw_bYjyM4PxKdRuU9zV5GdVlJfoXCafHktdxK9s",
            "metalness": 1.0,
            "roughness": 1.0,
            "price": 0.14
        },
        {
            "id": 13,
            "name": "Terracotta",
            "map": "https://arweave.net/xSZYDoRZmjeTm-3vUljUIY7hTueGJmAXXYZC1tB2yTo",
            "normalMap": "https://arweave.net/xk8PlCVwIrohYkmvs1TyFR5540p36ThkKjqdyuaj0uA",
            "roughnessMap": "https://arweave.net/5R-HpS43Rpf7Y3u2bEwF7WMnF_cTbyQMK-cSekTlcY4",
            "metalness": 0.0,
            "roughness": 1.0,
            "price": 0.15
        },
        {
            "id": 14,
            "name": "Lava",
            "map": "https://arweave.net/XdR3tA31mfbhtjEgdklD9wA9pTHRu2-15F7wmoE42k4",
            "normalMap": "https://arweave.net/nMxQRxOPK1yz5BSeAfXPQa5nDY8u3v6FFTs3IRSGMHg",
            "roughnessMap": "https://arweave.net/pvshVP-3hE7CxH8mc6iG1-Z0P3ya87to27VMZplRhdA",
            "metalness": 0.0,
            "roughness": 1.0,
            "displacementMap": "https://arweave.net/-c3mBq36Czwwy7gSOvPTIXeO_fAa45XhbcTa3Cs1c90",
            "displacementScale": 3,
            "price": 0.16
        },
        {
            "id": 15,
            "name": "Worn metal",
            "map": "https://arweave.net/fsB5H5CJaF2Zd-Y2DyHQv_JEhVg8JVsM0QuLEo015Q8",
            "normalMap": "https://arweave.net/UVHVYMesFZqJ82pn_isNsFmFoYc1_DnjujIw72Ezl6A",
            "roughnessMap": "https://arweave.net/47FfaK7cCWf5DQUpmtFZdXJUGjwgm2h6Ni-3LZA8NGI",
            "metalness": 1.0,
            "roughness": 1.0,
            "price": 0.17
        },
        {
            "id": 16,
            "name": "Steel",
            "map": "https://arweave.net/pS6dtrWrGbm0lUOXPwxfpRFOZvuWdmK151aFCA8d-6w",
            "normalMap": "https://arweave.net/aSnk-oArHDZGub6nikaOqjasswsmEjzWVQbXo1h37RQ",
            "roughnessMap": "https://arweave.net/HwwUgIXbxmjP1sgY78UXnZlc04UG_3mcoq86OiuhunY",
            "metalness": 1.0,
            "roughness": 1.0,
            "price": 0.18
        },
        {
            "id": 17,
            "name": "Organic",
            "map": "https://arweave.net/EKDRDMgCmBRAFBcRUc408B5sgrAVOtbqvs-BG3BBrz4",
            "normalMap": "https://arweave.net/Fg6WkZw6pM-R46FXwU53EHCG9nJ-0jWAujrSL438G7Y",
            "roughnessMap": "https://arweave.net/T1TP0ywrL2Su76laSXllbierzIt3aU9cW72EgMMe1FY",
            "metalness": 0.0,
            "roughness": 0.0,
            "displacementMap": "https://arweave.net/ANrApmpVZLe22dFD0vtN1prBAuw2WHCvHAz9zRb9MPY",
            "displacementScale": 5,
            "price": 0.19
        },
        {
            "id": 18,
            "name": "Marble red",
            "map": "https://arweave.net/FtDFuo7HTeZYDaUnhFvUYWBP-dYmZsBSqHdw1QrloPw",
            "normalMap": "https://arweave.net/D_gKYN-n0XhfwO94o4IPPdFKoGEhga2eZrI9-cIkxMY",
            "roughnessMap": "https://arweave.net/jxoeGdQmjrlRoEp4i0Xuf9UYICVDBWTuB3pZxs3DlXo",
            "metalness": 0.0,
            "roughness": 1.0,
            "price": 0.21
        },
        {
            "id": 19,
            "name": "Marble green",
            "map": "https://arweave.net/S3xHWnMWPanVV7OC7fqWIL2AR1pdJ1COoXoQXWPDQ_Q",
            "normalMap": "https://arweave.net/P4Dr7XW24yaf_1u9PRFyIgXANEeFRVdOjSTOaLvfDqo",
            "roughnessMap": "https://arweave.net/6R10dM_fNOVnuUhFZVlO7aX9Mz1Ez5Mhfut4_AMVG4Y",
            "metalness": 0.0,
            "roughness": 1.0,
            "price": 0.22
        },
        {
            "id": 20,
            "name": "Light gold",
            "map": "https://arweave.net/O3DRWDUNmHfUcu-Tq4E3KBAnZ0IG3FKZ06hmK6mYlek",
            "normalMap": "https://arweave.net/prT866HUBFbcVXmQFxIAvKF7OqFaV8L8d95Aj6ObXLA",
            "roughnessMap": "https://arweave.net/MChiRBPght-rvVMv3zgbQ7Z4fRDujHROpR4c6Px9HL0",
            "metalness": 1.0,
            "roughness": 0.9,
            "price": 0.22
        },
        {
            "id": 21,
            "name": "Ice cracked",
            "map": "https://arweave.net/eUZmapK_yJKuJfsOJGqv4aJ-gtz0SqQIIA6AHW4z8As",
            "normalMap": "https://arweave.net/XpGMccqJDajYZCSJsz9inu2y-ORoSGz_5orspIqpdro",
            "roughnessMap": "https://arweave.net/js33fvuZ-v_czgPRsa5qjOnCxthLctk_y4vwc-wYrUA",
            "metalness": 0.0,
            "roughness": 1.0,
            "price": 0.23
        },
        {
            "id": 22,
            "name": "Gold scuffed",
            "map": "https://arweave.net/g35MLuP93y3ufO6vW-5kd7WRZ-wBA_LkxWum6iuYj-0",
            "normalMap": "https://arweave.net/Wd2kjCTXvPQNoTMGXHt1w9i4goyO7bjFKp4zp8wTKvg",
            "roughnessMap": "https://arweave.net/FldPeIjz1DdBpl7XVlBBR9QfcKLi80cQcJt5E91ua5s",
            "metalness": 1.0,
            "roughness": 1.0,
            "price": 0.24
        }
    ])


    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = "Materials"

    def save(self):
        super().save()

        with open("data/materials.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def __str__(self):
        return "Materials"

class SelectImages(models.Model):
    data = models.JSONField(default=[
        {
            "bodyImages": [
                {
                    "name": "Abstract",
                    "path": "https://arweave.net/6OI5En58KTZr1hOgT-2HA_D1F1D_Ez91zUGu0p4mWx4"
                },
                {
                    "name": "Cloud",
                    "path": "https://arweave.net/cGVeFLPzPAni2yYVxyjh0ZMLk5rwAcAHIYNhpM_jdy8"
                },
                {
                    "name": "ColorDrops",
                    "path": "https://arweave.net/h-X51cC49VyL80IISBUJXVJhk9jIrNrlwVmxHMyc-vc"
                },
                {
                    "name": "Colors",
                    "path": "https://arweave.net/wEZRqs5h5bnuFd2qG_audLydJIfbQ_eQci9vyt46rFE"
                },
                {
                    "name": "DarkLight",
                    "path": "https://arweave.net/ANoBvxyXIDjSF5tBl4MYNNFTVCj2SK3euaHKBhEnY94"
                },
                {
                    "name": "Drops",
                    "path": "https://arweave.net/O6F89QiI-9bZNv4O_e99_ViMAAfMF4GLUiFF0dS1YiY"
                },
                {
                    "name": "Electric sun",
                    "path": "https://arweave.net/40HoP992AT_TeOPuKxZ3L4vh0jL0sO2wKN3DTo33mB0"
                },
                {
                    "name": "Lines",
                    "path": "https://arweave.net/F0KZWfnvIfrjKEUd5fkiO81llc81Qi0EHKsXuK0V0cI"
                },
                {
                    "name": "Morning",
                    "path": "https://arweave.net/hpCqIF82L4YL58ubE6GQpsjwx_opkc6FNweFHl9r6sQ"
                },
                {
                    "name": "Mountains",
                    "path": "https://arweave.net/QaGvNN3z_w4oS1k0yI6NflPjLmwbQCox1zEzF5LilGU"
                },
                {
                    "name": "Nature",
                    "path": "https://arweave.net/QbkUU_6fSicbSs-uoGoXu5BDfeWMBd--UfNGipEb_bs"
                },
                {
                    "name": "Thunderstorm",
                    "path": "https://arweave.net/CDFKexn6E8WgPqawQ8W_EA5xdzLNuHd5y7E2n1BVLvw"
                },
                {
                    "name": "Leaf",
                    "path": "https://arweave.net/YItsiDb7qGuP4lQqE_QqfMzX6FFLkpEVTN5fd2xQtnw"
                },
                {
                    "name": "Butterfly",
                    "path": "https://arweave.net/kmRR3YIFdWdf9-uvjZO0CcB2vUBWkUOiH95DxSrDjnw"
                },
                {
                    "name": "Tiles",
                    "path": "https://arweave.net/XC8dNb-K_Gpnr3cohEZxfjeH5rdnc8LofyP-tBl569k"
                }
            ],
            "backgroundImages": [
                {
                    "name": "Abstract",
                    "path": "https://arweave.net/6OI5En58KTZr1hOgT-2HA_D1F1D_Ez91zUGu0p4mWx4"
                },
                {
                    "name": "Cloud",
                    "path": "https://arweave.net/cGVeFLPzPAni2yYVxyjh0ZMLk5rwAcAHIYNhpM_jdy8"
                },
                {
                    "name": "ColorDrops",
                    "path": "https://arweave.net/h-X51cC49VyL80IISBUJXVJhk9jIrNrlwVmxHMyc-vc"
                },
                {
                    "name": "Colors",
                    "path": "https://arweave.net/wEZRqs5h5bnuFd2qG_audLydJIfbQ_eQci9vyt46rFE"
                },
                {
                    "name": "DarkLight",
                    "path": "https://arweave.net/ANoBvxyXIDjSF5tBl4MYNNFTVCj2SK3euaHKBhEnY94"
                },
                {
                    "name": "Drops",
                    "path": "https://arweave.net/O6F89QiI-9bZNv4O_e99_ViMAAfMF4GLUiFF0dS1YiY"
                },
                {
                    "name": "Electric sun",
                    "path": "https://arweave.net/40HoP992AT_TeOPuKxZ3L4vh0jL0sO2wKN3DTo33mB0"
                },
                {
                    "name": "Lines",
                    "path": "https://arweave.net/F0KZWfnvIfrjKEUd5fkiO81llc81Qi0EHKsXuK0V0cI"
                },
                {
                    "name": "Morning",
                    "path": "https://arweave.net/hpCqIF82L4YL58ubE6GQpsjwx_opkc6FNweFHl9r6sQ"
                },
                {
                    "name": "Mountains",
                    "path": "https://arweave.net/QaGvNN3z_w4oS1k0yI6NflPjLmwbQCox1zEzF5LilGU"
                },
                {
                    "name": "Nature",
                    "path": "https://arweave.net/QbkUU_6fSicbSs-uoGoXu5BDfeWMBd--UfNGipEb_bs"
                },
                {
                    "name": "Thunderstorm",
                    "path": "https://arweave.net/CDFKexn6E8WgPqawQ8W_EA5xdzLNuHd5y7E2n1BVLvw"
                },
                {
                    "name": "Leaf",
                    "path": "https://arweave.net/YItsiDb7qGuP4lQqE_QqfMzX6FFLkpEVTN5fd2xQtnw"
                },
                {
                    "name": "Butterfly",
                    "path": "https://arweave.net/kmRR3YIFdWdf9-uvjZO0CcB2vUBWkUOiH95DxSrDjnw"
                },
                {
                    "name": "Tiles",
                    "path": "https://arweave.net/XC8dNb-K_Gpnr3cohEZxfjeH5rdnc8LofyP-tBl569k"
                }
            ]
        }
    ])

    def save(self):
        super().save()

        with open("data/images.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        



#========================================
#price


class BodyViewPrice(models.Model):
    default = models.FloatField()
    custom_color = models.FloatField()
    custom_image = models.FloatField()
    select_image = models.FloatField()

    def __str__(self):
        return 'BodyViewPrice'


class BackgroundPrice(models.Model):
    default = models.FloatField()
    single_color = models.FloatField()
    linear_gradient = models.FloatField()
    radial_gradient = models.FloatField()
    custom_image = models.FloatField()
    select_image = models.FloatField()

    def __str__(self):
        return 'BackgroundPrice'

class TickerPrice(models.Model):
    default = models.FloatField()
    color = models.FloatField()

    def __str__(self):
        return 'TickerPrice'
    
class FontPrice(models.Model):
    price = models.FloatField()

class EnvPrice(models.Model):
    price = models.FloatField()


class Returned(models.Model):
    count = models.FloatField(default=0)


    def __str__(self):
        return 'Returned'
    

class MintCount(models.Model):
    general_sum = models.PositiveIntegerField(default=0)


class MintActive(models.Model):
    is_active = models.BooleanField(default=False)


class Font(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    

class Environment(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    is_active = models.BooleanField(default=True)