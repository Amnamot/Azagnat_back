from django.contrib import admin
from .models import *

@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'percent']

@admin.register(EasyMint)
class EasyMintAdmin(admin.ModelAdmin):
    list_display = ['code']

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
    list_display = ["id"]


@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ['id']



@admin.register(SelectImages)
class SelectImagesAdmin(admin.ModelAdmin):
    list_display = ['id']


admin.site.register(Returned)
admin.site.register(Address)
admin.site.register(MintActive)


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'token_id', 'contract', 'date_minted']

@admin.register(RefferalCode)
class RefferalCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'paid', 'deals']

@admin.register(Ambassador)
class AmbassadorAdmin(admin.ModelAdmin):
    list_display = ['address','name', 'discount', 'royality', 'code']


@admin.register(MintCount)
class MintCountAdmin(admin.ModelAdmin):
    list_display = ['general_sum']

@admin.register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']

@admin.register(FontPrice)
class FontPriceAdmin(admin.ModelAdmin):
    list_display = ['price']

@admin.register(EnvPrice)
class EnvironmentPriceAdmin(admin.ModelAdmin):
    list_display = ['price']
