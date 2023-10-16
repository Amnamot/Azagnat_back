# Generated by Django 4.2.5 on 2023-10-16 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_materials_albedo_file_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelectImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=[{'backgroundImages': [{'name': 'Abstract', 'path': 'https://arweave.net/6OI5En58KTZr1hOgT-2HA_D1F1D_Ez91zUGu0p4mWx4'}, {'name': 'Cloud', 'path': 'https://arweave.net/cGVeFLPzPAni2yYVxyjh0ZMLk5rwAcAHIYNhpM_jdy8'}, {'name': 'ColorDrops', 'path': 'https://arweave.net/h-X51cC49VyL80IISBUJXVJhk9jIrNrlwVmxHMyc-vc'}, {'name': 'Colors', 'path': 'https://arweave.net/wEZRqs5h5bnuFd2qG_audLydJIfbQ_eQci9vyt46rFE'}, {'name': 'DarkLight', 'path': 'https://arweave.net/ANoBvxyXIDjSF5tBl4MYNNFTVCj2SK3euaHKBhEnY94'}, {'name': 'Drops', 'path': 'https://arweave.net/O6F89QiI-9bZNv4O_e99_ViMAAfMF4GLUiFF0dS1YiY'}, {'name': 'Electric sun', 'path': 'https://arweave.net/40HoP992AT_TeOPuKxZ3L4vh0jL0sO2wKN3DTo33mB0'}, {'name': 'Lines', 'path': 'https://arweave.net/F0KZWfnvIfrjKEUd5fkiO81llc81Qi0EHKsXuK0V0cI'}, {'name': 'Morning', 'path': 'https://arweave.net/hpCqIF82L4YL58ubE6GQpsjwx_opkc6FNweFHl9r6sQ'}, {'name': 'Mountains', 'path': 'https://arweave.net/QaGvNN3z_w4oS1k0yI6NflPjLmwbQCox1zEzF5LilGU'}, {'name': 'Nature', 'path': 'https://arweave.net/QbkUU_6fSicbSs-uoGoXu5BDfeWMBd--UfNGipEb_bs'}, {'name': 'Thunderstorm', 'path': 'https://arweave.net/CDFKexn6E8WgPqawQ8W_EA5xdzLNuHd5y7E2n1BVLvw'}, {'name': 'Leaf', 'path': 'https://arweave.net/YItsiDb7qGuP4lQqE_QqfMzX6FFLkpEVTN5fd2xQtnw'}, {'name': 'Butterfly', 'path': 'https://arweave.net/kmRR3YIFdWdf9-uvjZO0CcB2vUBWkUOiH95DxSrDjnw'}, {'name': 'Tiles', 'path': 'https://arweave.net/XC8dNb-K_Gpnr3cohEZxfjeH5rdnc8LofyP-tBl569k'}], 'bodyImages': [{'name': 'Abstract', 'path': 'https://arweave.net/6OI5En58KTZr1hOgT-2HA_D1F1D_Ez91zUGu0p4mWx4'}, {'name': 'Cloud', 'path': 'https://arweave.net/cGVeFLPzPAni2yYVxyjh0ZMLk5rwAcAHIYNhpM_jdy8'}, {'name': 'ColorDrops', 'path': 'https://arweave.net/h-X51cC49VyL80IISBUJXVJhk9jIrNrlwVmxHMyc-vc'}, {'name': 'Colors', 'path': 'https://arweave.net/wEZRqs5h5bnuFd2qG_audLydJIfbQ_eQci9vyt46rFE'}, {'name': 'DarkLight', 'path': 'https://arweave.net/ANoBvxyXIDjSF5tBl4MYNNFTVCj2SK3euaHKBhEnY94'}, {'name': 'Drops', 'path': 'https://arweave.net/O6F89QiI-9bZNv4O_e99_ViMAAfMF4GLUiFF0dS1YiY'}, {'name': 'Electric sun', 'path': 'https://arweave.net/40HoP992AT_TeOPuKxZ3L4vh0jL0sO2wKN3DTo33mB0'}, {'name': 'Lines', 'path': 'https://arweave.net/F0KZWfnvIfrjKEUd5fkiO81llc81Qi0EHKsXuK0V0cI'}, {'name': 'Morning', 'path': 'https://arweave.net/hpCqIF82L4YL58ubE6GQpsjwx_opkc6FNweFHl9r6sQ'}, {'name': 'Mountains', 'path': 'https://arweave.net/QaGvNN3z_w4oS1k0yI6NflPjLmwbQCox1zEzF5LilGU'}, {'name': 'Nature', 'path': 'https://arweave.net/QbkUU_6fSicbSs-uoGoXu5BDfeWMBd--UfNGipEb_bs'}, {'name': 'Thunderstorm', 'path': 'https://arweave.net/CDFKexn6E8WgPqawQ8W_EA5xdzLNuHd5y7E2n1BVLvw'}, {'name': 'Leaf', 'path': 'https://arweave.net/YItsiDb7qGuP4lQqE_QqfMzX6FFLkpEVTN5fd2xQtnw'}, {'name': 'Butterfly', 'path': 'https://arweave.net/kmRR3YIFdWdf9-uvjZO0CcB2vUBWkUOiH95DxSrDjnw'}, {'name': 'Tiles', 'path': 'https://arweave.net/XC8dNb-K_Gpnr3cohEZxfjeH5rdnc8LofyP-tBl569k'}]}])),
            ],
        ),
        migrations.DeleteModel(
            name='SelectImageBackground',
        ),
        migrations.DeleteModel(
            name='SelectImageBody',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='albedo',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='displacement',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='displacescale',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='displaceshift',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='metalness',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='name',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='normal',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='price',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='roughness',
        ),
        migrations.RemoveField(
            model_name='materials',
            name='roughness_param',
        ),
        migrations.RemoveField(
            model_name='models',
            name='bend',
        ),
        migrations.RemoveField(
            model_name='models',
            name='curve_radius',
        ),
        migrations.RemoveField(
            model_name='models',
            name='link',
        ),
        migrations.RemoveField(
            model_name='models',
            name='locX',
        ),
        migrations.RemoveField(
            model_name='models',
            name='locY',
        ),
        migrations.RemoveField(
            model_name='models',
            name='name',
        ),
        migrations.RemoveField(
            model_name='models',
            name='pozZ',
        ),
        migrations.RemoveField(
            model_name='models',
            name='price',
        ),
        migrations.RemoveField(
            model_name='models',
            name='shiftGlass',
        ),
        migrations.RemoveField(
            model_name='models',
            name='speed',
        ),
        migrations.AddField(
            model_name='materials',
            name='data',
            field=models.JSONField(default=[{'id': 0, 'map': 'https://arweave.net/Q4ZEe6PeFpXdYTa2NHOFUeCQQHKoJDxedLnVajQ7J5g', 'metalness': 1.0, 'name': 'Golden scr.', 'normalMap': 'https://arweave.net/2ZE6DAGKlabJl5dYSzqAjglm-NcpheVYsZbgrndPI60', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/PxXXrrZrtvoFPzXjeBmj-WI7EIYNvZB4B-g7A9532Os'}, {'id': 1, 'map': 'https://arweave.net/9C-XpPo21lj9aSm78GBw3zX3k_t-ilOkjqARp-5xEGM', 'metalness': 0.16, 'name': 'Violet crystal', 'normalMap': 'https://arweave.net/ndw1EPyUxH7jhB4uJOIFtFdKW4s3XjDmRftS9a_yHqY', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/27kLNmoQxER3L3xvlNYgH7RoTmpDLNZzYLR4yNpbR3c'}, {'id': 2, 'map': 'https://arweave.net/c9xN9FVzfqzSA3X91DsuRdAdal0rj1b7S3Zez9dFtYc', 'metalness': 1.0, 'name': 'Metal scr.', 'normalMap': 'https://arweave.net/SpJ8tilMij2OT3MNVTnSA3QJtrWzVRyLYJFVHlxEcsY', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/Xxlj0jZo_m_IsIYPUX7UpjCbwD8nvJ7_ddigw7n35LY'}, {'id': 3, 'map': 'https://arweave.net/vP8OH4j93GiuZAfnEuDVIkBjeN9NqkaIMceU-1DysxQ', 'metalness': 0.0, 'name': 'Wood', 'normalMap': 'https://arweave.net/5-fjpVJ03Qjly6X7s0lePnM_BY3SlYGsAJOBqoygKMQ', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/Qdu9D0r440jg1KVSztrtcm_NnaaAGXbDzGxPXm3stlc'}, {'id': 4, 'map': 'https://arweave.net/zgMfoEvrEYVOMlaPIQ0OMfo0DbFICsziwSWn9Y-_8gE', 'metalness': 0.0, 'name': 'Walnut wood', 'normalMap': 'https://arweave.net/vQto9YanPRzhnHEFRRePXD-zWTePG3-MxyQ5FpBOuFo', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/ch5QLG55OQylBESvDHNj8ZylPwjRdiUBAk2ZUuaNAzA'}, {'id': 5, 'map': 'https://arweave.net/2G8tSc1nNUCcXdMBfAgk7p0rrR_BPfxHl9xX_kn0uBg', 'metalness': 0.35, 'name': 'Concrete', 'normalMap': 'https://arweave.net/QLjfu2ZXjRHKk53rju19OWK9Jcz_qzhUI4EfEVhbfFU', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/qhLCsN71I50LYx04daXjuUV6MnADqbBz66Cyzkj4tyg'}, {'id': 6, 'map': 'https://arweave.net/J940vo41iFWwAbuCbQgwYkkOg3gKMsRVtt0iqmObz9c', 'metalness': 1.0, 'name': 'Darck cracks', 'normalMap': 'https://arweave.net/zhME-6ll9DFpmUNHL6asMP6Ppt6C3GoMilIUieAXALc', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/YN8UpVjpVtry-Fba7zvuJfkJ5YIGVEfQoaDjtfrVV8M'}, {'id': 7, 'map': 'https://arweave.net/k53jsVxDwEpjAFAIdv1v4QrcjIg8FP6RXTSL7uJTRrM', 'metalness': 0.0, 'name': 'Plastic line', 'normalMap': 'https://arweave.net/OL2upxh1lwiHNYgEIJgcyZtUm0XcUrJ-uD8aUW-XmtY', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/OlRIUwBh4GHkOFWvcCuxqBx4nAbWg_G4nob4PNxqMlY'}, {'id': 8, 'map': 'https://arweave.net/xXVB5_jIMOV6tYkj97jTkOeMO705I-nNWoqQMalJpAw', 'metalness': 0.0, 'name': 'Cow fur', 'normalMap': 'https://arweave.net/4mMS1WFL3EJpYDuBq4yWIMY2zF7WjDRFiDo_XMtB7jk', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/gGVTkHfDmOBZSlWjdo06JsX2UINvmXNCORMyH6VvLbo'}, {'id': 9, 'map': 'https://arweave.net/sCfPurEYWsJNTTKGtSlsAFffborVu-tw6YfOHAzokWw', 'metalness': 0.1, 'name': 'Maple wood', 'normalMap': 'https://arweave.net/9ZUIIxkY_fFKEgAVmwa3ydFyeMtSk1GXM3kfh-kkP18', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/7rzU5hXd6s1710rbirwXDq2r5xFtymRW_mGRaWeYfLA'}, {'id': 10, 'map': 'https://arweave.net/KOYLiS6W73noAJT6QoFD5lXG78IDRp3-JPx0ZrY0lmE', 'metalness': 1.0, 'name': 'Oxidized copper', 'normalMap': 'https://arweave.net/dhlLVWMqOfYtvQ-ZfVgNky5Id4MfHpAPwBNxYFTSo74', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/bYE4v_8R2ZXVaS_H_qMLV7D8Z-cNlUUMDFEdAzQhf6Y'}, {'id': 11, 'map': 'https://arweave.net/CCdiegpZ4SELC0yyL1v_hY9e3r-Jjtx505kDOTmNjWY', 'metalness': 0.6, 'name': 'Carbon fiber', 'normalMap': 'https://arweave.net/fivUFYgY925qZP1FJzBI0MVr4oOhjvOTPxn8RuMFzXQ', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/otqnMrH2UKG2rj92fzDwnzCYhWlxcpcklyJqPxXN36o'}, {'id': 12, 'map': 'https://arweave.net/-8T9bGZSNkDSOTa-JbsbFdJqO2fz97rmjBXB7n_7iDo', 'metalness': 1.0, 'name': 'Copper hammered', 'normalMap': 'https://arweave.net/-8T9bGZSNkDSOTa-JbsbFdJqO2fz97rmjBXB7n_7iDo', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/0XaJnw_bYjyM4PxKdRuU9zV5GdVlJfoXCafHktdxK9s'}, {'id': 13, 'map': 'https://arweave.net/xSZYDoRZmjeTm-3vUljUIY7hTueGJmAXXYZC1tB2yTo', 'metalness': 0.0, 'name': 'Terracotta', 'normalMap': 'https://arweave.net/xk8PlCVwIrohYkmvs1TyFR5540p36ThkKjqdyuaj0uA', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/5R-HpS43Rpf7Y3u2bEwF7WMnF_cTbyQMK-cSekTlcY4'}, {'displacementBias': -0.5, 'displacementMap': 'https://arweave.net/-c3mBq36Czwwy7gSOvPTIXeO_fAa45XhbcTa3Cs1c90', 'displacementScale': 3, 'id': 14, 'map': 'https://arweave.net/XdR3tA31mfbhtjEgdklD9wA9pTHRu2-15F7wmoE42k4', 'metalness': 0.0, 'name': 'Lava', 'normalMap': 'https://arweave.net/nMxQRxOPK1yz5BSeAfXPQa5nDY8u3v6FFTs3IRSGMHg', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/pvshVP-3hE7CxH8mc6iG1-Z0P3ya87to27VMZplRhdA'}, {'id': 15, 'map': 'https://arweave.net/fsB5H5CJaF2Zd-Y2DyHQv_JEhVg8JVsM0QuLEo015Q8', 'metalness': 1.0, 'name': 'Worn metal', 'normalMap': 'https://arweave.net/UVHVYMesFZqJ82pn_isNsFmFoYc1_DnjujIw72Ezl6A', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/47FfaK7cCWf5DQUpmtFZdXJUGjwgm2h6Ni-3LZA8NGI'}, {'id': 16, 'map': 'https://arweave.net/pS6dtrWrGbm0lUOXPwxfpRFOZvuWdmK151aFCA8d-6w', 'metalness': 1.0, 'name': 'Steel', 'normalMap': 'https://arweave.net/aSnk-oArHDZGub6nikaOqjasswsmEjzWVQbXo1h37RQ', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/HwwUgIXbxmjP1sgY78UXnZlc04UG_3mcoq86OiuhunY'}, {'displacementBias': -1.5, 'displacementMap': 'https://arweave.net/ANrApmpVZLe22dFD0vtN1prBAuw2WHCvHAz9zRb9MPY', 'displacementScale': 5, 'id': 17, 'map': 'https://arweave.net/EKDRDMgCmBRAFBcRUc408B5sgrAVOtbqvs-BG3BBrz4', 'metalness': 0.0, 'name': 'Organic', 'normalMap': 'https://arweave.net/Fg6WkZw6pM-R46FXwU53EHCG9nJ-0jWAujrSL438G7Y', 'price': 0.1, 'roughness': 0.0, 'roughnessMap': 'https://arweave.net/T1TP0ywrL2Su76laSXllbierzIt3aU9cW72EgMMe1FY'}, {'id': 18, 'map': 'https://arweave.net/FtDFuo7HTeZYDaUnhFvUYWBP-dYmZsBSqHdw1QrloPw', 'metalness': 0.0, 'name': 'Marble red', 'normalMap': 'https://arweave.net/D_gKYN-n0XhfwO94o4IPPdFKoGEhga2eZrI9-cIkxMY', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/jxoeGdQmjrlRoEp4i0Xuf9UYICVDBWTuB3pZxs3DlXo'}, {'id': 19, 'map': 'https://arweave.net/S3xHWnMWPanVV7OC7fqWIL2AR1pdJ1COoXoQXWPDQ_Q', 'metalness': 0.0, 'name': 'Marble green', 'normalMap': 'https://arweave.net/P4Dr7XW24yaf_1u9PRFyIgXANEeFRVdOjSTOaLvfDqo', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/6R10dM_fNOVnuUhFZVlO7aX9Mz1Ez5Mhfut4_AMVG4Y'}, {'id': 20, 'map': 'https://arweave.net/O3DRWDUNmHfUcu-Tq4E3KBAnZ0IG3FKZ06hmK6mYlek', 'metalness': 1.0, 'name': 'Light gold', 'normalMap': 'https://arweave.net/prT866HUBFbcVXmQFxIAvKF7OqFaV8L8d95Aj6ObXLA', 'price': 0.1, 'roughness': 0.9, 'roughnessMap': 'https://arweave.net/MChiRBPght-rvVMv3zgbQ7Z4fRDujHROpR4c6Px9HL0'}, {'id': 21, 'map': 'https://arweave.net/eUZmapK_yJKuJfsOJGqv4aJ-gtz0SqQIIA6AHW4z8As', 'metalness': 0.0, 'name': 'Ice cracked', 'normalMap': 'https://arweave.net/XpGMccqJDajYZCSJsz9inu2y-ORoSGz_5orspIqpdro', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/js33fvuZ-v_czgPRsa5qjOnCxthLctk_y4vwc-wYrUA'}, {'id': 22, 'map': 'https://arweave.net/g35MLuP93y3ufO6vW-5kd7WRZ-wBA_LkxWum6iuYj-0', 'metalness': 1.0, 'name': 'Gold scuffed', 'normalMap': 'https://arweave.net/Wd2kjCTXvPQNoTMGXHt1w9i4goyO7bjFKp4zp8wTKvg', 'price': 0.1, 'roughness': 1.0, 'roughnessMap': 'https://arweave.net/FldPeIjz1DdBpl7XVlBBR9QfcKLi80cQcJt5E91ua5s'}]),
        ),
        migrations.AddField(
            model_name='models',
            name='data',
            field=models.JSONField(default=[{'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': -30, 'fontSize': 5, 'local-path': 'https://arweave.net/RxtNv0UnhR7dUICf8ZjqMa7IlTpgHMilM055tx_5syk', 'name': 'Ostan', 'price': 0.0, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': -30, 'fontSize': 5, 'local-path': 'https://arweave.net/1t1qEGTTEiNHUjQZNzEvVTr9iGdHM7rY7kB1_PMQisU', 'name': 'Hiron', 'price': 0.01, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': -60, 'fontSize': 5, 'local-path': 'https://arweave.net/5zGsUDLdYTkkPB_pdvJDxAM-UbqUmDU4KbHtCEKqjcY', 'name': 'Vesta', 'price': 0.02, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': -30, 'fontSize': 5, 'local-path': 'https://arweave.net/koa1zxvzpfTtyBlLamuIENU5Li_gj50irMvivHl-nqI', 'name': 'Beroz', 'price': 0.02, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': -30, 'fontSize': 5, 'local-path': 'https://arweave.net/7RP_jxbF3V4G-ht1HXWmRjwSwnsL-tbL_n0gXeQw9wE', 'name': 'Vega', 'price': 0.03, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': -30, 'fontSize': 5, 'hat': 0, 'local-path': 'https://arweave.net/54_M2OvAOnO-vKmL34wE0QxPFKcl6KgHIlWxBotnpS4', 'name': 'Joulupukki', 'price': 0.03, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': -60, 'fontSize': 5, 'local-path': 'https://arweave.net/kSQLBRS6dWyXnn1z4WTRu4mLiyPHRLe7bg4SkUh940o', 'name': 'Maradona', 'price': 0.03, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': 60, 'fontSize': 5, 'local-path': 'https://arweave.net/Kg2PcSqR6yi4EnS40VNwaX-C7cFg-2kgBQR8hB2Eivw', 'name': 'Star', 'price': 0.03, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': 270, 'fontSize': 5, 'local-path': 'https://arweave.net/jIIRbgLKUNCMMV-66UHHy2VtB4-vJSm-qvTCw-S7qJk', 'name': 'Pokeball', 'price': 0.03, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': -120, 'fontSize': 5, 'local-path': 'https://arweave.net/6yCVyyCK159gbEi56-hNH9TQl1NYr-_qWxbcxt4YSok', 'name': 'Icosa', 'price': 0.03, 'shiftGlass': 0.1, 'speed': 10}, {'Bend': -30, 'LocX': -14, 'LocY': -10, 'PozZ': 32, 'curve_radius': 0, 'fontSize': 5, 'hat': 1, 'local-path': 'https://arweave.net/4Ki4RFg_ZmBmuCVonuqSbPRj5PJgqxcl0jYkOV33Lxs', 'name': 'Rock', 'price': 0.03, 'shiftGlass': 0.1, 'speed': 10}]),
        ),
    ]
