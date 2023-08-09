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
        verbose_name = 'address'
        verbose_name_plural = "addresses"


    def __str__(self):
        return self.address


class Config(models.Model):
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE
    )
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
    base_cost = models.FloatField()
    contract = models.CharField(max_length=500, primary_key=True)
    date_minted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'config'
        verbose_name_plural = "configs"

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
        verbose_name = 'refferal_code'
        verbose_name_plural = "refferal_code"

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
        verbose_name = 'promocode'
        verbose_name_plural = "promocodes"

    def __str__(self):
        return self.code


class Ambassador(models.Model):
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE
    )
    code = models.URLField(unique=True, null=True, blank=True)
    percent = models.IntegerField(default=0)


    def save(self):
        if self.code == None:
            self.code = DOMEN + '?a=' + generator(8)
        
        super().save()

    class Meta:
        verbose_name = 'ambassador'
        verbose_name_plural = "ambassadors"

    def __str__(self):
        return self.code
    

class EasyMint(models.Model):
    code = models.URLField(unique=True, null=True, blank=True)


    def save(self):
        if self.code == None:
            self.code = DOMEN + '?e=' + generator(8)
        
        super().save()

    class Meta:
        verbose_name = 'Easy mint'
        verbose_name_plural = "Easy mints"

    def __str__(self):
        return self.code

    
#==============================
#images and glb

class Models(models.Model):
    name = models.CharField(max_length=20)
    file = models.FileField(upload_to="models")
    link = models.URLField()
    curve_radius = models.FloatField()
    price = models.FloatField()

    def save(self):
        super().save()
        if os.stat("data/models.json").st_size == 0:
            model = []
        else:
            with open("data/models.json", 'r', encoding='utf-8') as f:
                model = json.load(f)
        data = {
            "name": self.name,
            "local-path": self.file.url[1::],
            "price": self.price
        }
        if len(model)>=self.id:
            model[self.id-1] = data
        else:
            model.append(data)
        with open("data/models.json", 'w', encoding='utf-8') as f:
            json.dump(model,f,indent=4,ensure_ascii=False)
        
    class Meta:
        verbose_name = 'model'
        verbose_name_plural = "models"

    def __str__(self):
        return self.name

class Materials(models.Model):
    name = models.CharField(max_length=20, unique=True)
    albedo = models.URLField()
    normal = models.URLField()
    roughness = models.URLField()
    albedo_file = models.ImageField(upload_to=f"models/materials")
    normal_file = models.ImageField(upload_to=f"models/materials")
    roughness_file = models.ImageField(upload_to=f"models/materials")
    displacement = models.URLField(null=True, blank=True)
    displacement_file = models.ImageField(upload_to=f"models/materials", null=True, blank=True)
    metalness = models.FloatField()
    roughness_param = models.FloatField()
    displacescale = models.FloatField(null=True, blank=True)
    displaceshift = models.FloatField(null=True, blank=True)
    price = models.FloatField()


    class Meta:
        verbose_name = 'material'
        verbose_name_plural = "materials"

    def save(self):
        super().save()
        if os.stat("data/materials.json").st_size == 0:
            materials = []
        else:
            with open("data/materials.json", 'r', encoding='utf-8') as f:
                materials = json.load(f)
        data = {
            "id": self.id-1,
            "name": self.name,
            "map": ".." + self.albedo_file.url,
            "normalMap": ".." + self.normal_file.url,
            "roughnessMap": ".." + self.roughness_file.url,
            "metalness": self.metalness,
            "roughness": self.roughness_param
        }
        if len(materials)>=self.id:
            materials[self.id-1] = data
        else:
            materials.append(data)
        with open("data/materials.json", 'w', encoding='utf-8') as f:
            json.dump(materials, f, indent=4, ensure_ascii=False)
    
    def __str__(self):
        return self.name

class SelectImageBody(models.Model):
    name = models.CharField(max_length=20)
    file = models.ImageField(upload_to="body-img")
    link = models.URLField()

    def save(self):
        super().save()
        if os.stat("data/images.json").st_size == 0:
            images = [
                {
                "bodyImages": [],
                "backgroundImages": []
                }
            ]
        else:
            with open("data/images.json", 'r', encoding='utf-8') as f:
                images = json.load(f)
        data = {
            "name" : self.name,
            "path" : ".." + self.file.url
        }
        if len(images[0]['bodyImages'])>=self.id:
            images[0]['bodyImages'][self.id-1] = data
        else:
            images[0]['bodyImages'].append(data)
        

        with open("data/images.json", 'w', encoding='utf-8') as f:
            json.dump(images,f,indent=4,ensure_ascii=False)

    class Meta:
        verbose_name = 'std_body_image'
        verbose_name_plural = "std_body_images"

    def __str__(self):
        return self.name

class SelectImageBackground(models.Model):
    name = models.CharField(max_length=20)
    file = models.ImageField(upload_to="bg-img")
    link = models.URLField()

    def save(self):
        super().save()
        if os.stat("data/images.json").st_size == 0:
            images = [
                {
                "bodyImages": [],
                "backgroundImages": []
                }
            ]
        else:
            with open("data/images.json", 'r', encoding='utf-8') as f:
                images = json.load(f)
        data = {
            "name" : self.name,
            "path" : ".." + self.file.url
        }
        if len(images[0]['backgroundImages'])>=self.id:
            images[0]['backgroundImages'][self.id-1] = data
        else:
            images[0]['backgroundImages'].append(data)

        with open("data/images.json", 'w', encoding='utf-8') as f:
            json.dump(images,f,indent=4,ensure_ascii=False)

    class Meta:
        verbose_name = 'std_background_image'
        verbose_name_plural = "std_background_images"

    def __str__(self):
        return self.name



#========================================
#price

class BasePrice(models.Model):
    price = models.FloatField()


    def __str__(self):
        return "BasePrice"    

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
    


class Returned(models.Model):
    count = models.FloatField(default=0)


    def __str__(self):
        return 'returned'
    

class MintCount(models.Model):
    general_sum = models.PositiveIntegerField(default=0)


class MintActive(models.Model):
    is_active = models.BooleanField(default=False)