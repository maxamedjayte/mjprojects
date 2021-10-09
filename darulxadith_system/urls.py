from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard),
    path('diwangalinta_sanad_dugsiyedka/',views.sanadDugsiyedka),
    path('mustawa/',views.registerMustawa,name='add_mustawa'),
    path('xalqadaha/',views.addXalqad),
    path('diwangalinta_ardada/',views.diiwangalintaArdada),
    path('xogta_ardada/',views.xogtaArdada),
    path('xogta_xalqadaan/<str:pk>/',views.xogtaXalqadaan),
    path('xogta_mustawahaan/<str:pk>/',views.xogtaMustawahaan),

    path('xogta_ardaygan/<str:magaca_ardayga>/',views.xogtaArdaygan),
    path('update_ardaygan/',views.updateArdaygan),
    path('delete_ardaygaan/',views.deleteArdaygaan),
    path('xadiriska_ardaygaan/<str:magaca_ardaygaan>/',views.xadiriskaArdaygaan),

    path('imtixaanadka/',views.imtixaanadka),
    path('ardadaXalqadaan/<str:xalqada>/<str:raqamka>/',views.ardadaXalqadaan),
    path('qaadista_buundoyinka/<str:xalqada>/<str:raqamka>/<str:magaca_ardayga>/',views.qaadistaBuundoyinka),
    path('has_imtixan/',views.hasImtixanFuntion),
    path('diiwangalinta_imtixaanka/<str:sanaddugsiyedka>/<str:magacaArdayga>/',views.diiwangalintaImtixaanka),
    path('imtixanka_xalqadaha/',views.imtixankaXalqadaha),

    path('imtixanka_xalqadaan/<str:xalqada>/<str:raqamka>/',views.imtixankaXalqadaan),
    path('hel_imtixanka_xalqadaan/',views.hel_imtixankaXalqadaan),
    path('hel_imtixaanka_ardaygaan/',views.helImtixaankaArdaygaan),



    path('diwangali_imtixana_ardagan/<str:xalqada>/<str:raqamka>/<str:magaca_ardayga>/',views.helBuundoyinkaMadaKaste),
    path('save_garenta_buundada/',views.saveGareyBuundadaArdaygan),
    path('xaadiriska/',views.xaadiriska),
    path('xaadiriska_xalqadaan/<str:xalqada>/<str:raqamka>/',views.xaadiriskaXalqadaan),

    path('qaadista_xadiriska/<str:xalqada>/<str:raqamka>/',views.qadistaXaadiriska),

    path('attendece_print/<str:xalqada>/<str:raqamka>/<str:jinsiga>/',views.attendencePrint),

    path('diiwangalinta_mulaaxadatka/<str:magaca_ardayga>/',views.diiwangalintaMulaaxadatka),

]       