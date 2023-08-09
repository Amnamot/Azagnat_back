from django.contrib import admin
from .models import *

@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'percent']

@admin.register(EasyMint)
class EasyMintAdmin(admin.ModelAdmin):
    list_display = ['code']

@admin.register(BasePrice)
class BasePriceAdmin(admin.ModelAdmin):
    list_display = ['price']

@admin.register(BodyViewPrice)
class BodyViewPriceAdmin(admin.ModelAdmin):
    list_display = ['default', 'custom_color', 'custom_image', 'select_image']

@admin.register(BackgroundPrice)
class BackgroundPriceAdmin(admin.ModelAdmin):
    list_display = ['default', 'single_color', 'linear_gradient', 'radial_gradient', 'custom_image', 'select_image']

@admin.register(TickerPrice)
class TickerPriceAdmin(admin.ModelAdmin):
    list_display = ['default', 'color']




@admin.register(Models)
class ModelsAdmin(admin.ModelAdmin):
    list_display = ['name', 'curve_radius', 'price']



@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ['name', 'metalness', 'roughness_param', 'price']



@admin.register(SelectImageBody)
class SelectImageBodyAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SelectImageBackground)
class SelectImageBackgroundAdmin(admin.ModelAdmin):
    list_display = ['name']



admin.site.register(Returned)
admin.site.register(Address)
admin.site.register(MintActive)


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['token_id', 'contract', 'date_minted']

@admin.register(RefferalCode)
class RafferalCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'paid', 'deals']

@admin.register(Ambassador)
class AmbassadorAdmin(admin.ModelAdmin):
    list_display = ['address', 'code']


@admin.register(MintCount)
class MintCountAdmin(admin.ModelAdmin):
    list_display = ['general_sum']

