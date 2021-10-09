from datetime import date, datetime, timedelta
import re
from django.core import serializers
from django import http
from darulxadith_system.models import Ardada, Mulaaxadaat, Mustawaha, Natiijada, SanadDugsiyeedka, Xaadiriska, Xalqada
from django.shortcuts import render
from django.views.generic import CreateView
from django.http import JsonResponse
from hijri_converter import Hijri, Gregorian,convert
from django.http import HttpResponse, HttpResponseRedirect
from json import dumps
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
# Create your views here.
magacyadaImtixanada=['شفوي الاول','نصف','شفوي الثاني','ءاخر']
sanadDugsiyeedkaHadda=SanadDugsiyeedka.objects.all().last()
def dashboard(request):
    ardada=Ardada.objects.all().count()
    wiilasha=Ardada.objects.filter(jinsiga='ذكر').count()
    gabdhaha=Ardada.objects.filter(jinsiga='انثي').count()
    xalqadaha=Xalqada.objects.all().count()
    xaadiriska=Xaadiriska.objects.all()
    data={
        'mulaaxadaatka':Mulaaxadaat.objects.all(),
        'wiilasha':wiilasha,
        'gabdhaha':gabdhaha,
        'xalqadaha':xalqadaha,
        'ardada':ardada,
        'xaadiriksa':xaadiriska,
        'mulaaxadaatka':Mulaaxadaat.objects.all().order_by('-id')[:10]
    }
    return render(request,'darulxadith_pr/dashboard.html',data)


def sanadDugsiyedka(request):
    if request.POST:
        fromHijriDate=request.POST.get('from-date')
        toHijriDate=request.POST.get('to-date')

        fromGregDate=convert.Hijri(int(fromHijriDate.split('-')[0]),int(fromHijriDate.split('-')[1]),int(fromHijriDate.split('-')[2])).to_gregorian()
        toGregDate=convert.Hijri(int(toHijriDate.split('-')[0]),int(toHijriDate.split('-')[1]),int(toHijriDate.split('-')[2])).to_gregorian()

        SanadDugsiyeedka.objects.create(taariikhdaBillowgaHijri=fromHijriDate,taariikhdaDhamaadkaHijri=toHijriDate,taariikhdaBillowgaMiladi=fromGregDate,taariikhdaDhamaadkaMIladi=toGregDate)
    data={
        'sanadDugsiyeedyada':SanadDugsiyeedka.objects.all()
    }
    return render(request,'darulxadith_pr/diiwangalinta_sanad_dugsiyedka.html',data)

def registerMustawa(request):
    if request.POST:
        magacaMustawaha=request.POST.get('magaca-mustawaha')
        sanadDugsiyedka=request.POST.get('sanad-dugsiyedka')
        maadoyinka=request.POST.get('maadoyinka')
        Mustawaha.objects.create(magacaMustawaha=magacaMustawaha,sanadDugsiyeedka=SanadDugsiyeedka.objects.all()[0],maadoyinka=maadoyinka)
    
    sanadDugsiyedyada=SanadDugsiyeedka.objects.all()
    mustawayasha=Mustawaha.objects.all()

    data={
        'sanadDugsiyedyada':sanadDugsiyedyada,
        'mustawayasha':mustawayasha
    }
    return render(request,'darulxadith_pr/add_mustawa.html',data)

def xogtaMustawahaan(request,pk):
    mustawahan=Mustawaha.objects.get(pk=pk)
    
    if request.POST:
        print(request.POST.get('maadoyinka'))
        mustawahan.maadoyinka=request.POST.get('maadoyinka')
        mustawahan.save()
        return JsonResponse({'response':True})
    else:
        xalqada=''
        ardada=''
        if Xalqada.objects.filter(mustawaha=mustawahan).exists():
            xalqada=Xalqada.objects.filter(mustawaha=mustawahan).all
            if Ardada.objects.filter(mustawahaArdayga=Xalqada.objects.get(mustawaha=mustawahan)).exists:
                ardada=Ardada.objects.filter(mustawahaArdayga=Xalqada.objects.get(mustawaha=mustawahan)).count
            else:
                ardada='2'
        else:
            xalqada=''
        data={
            'mustawahan':mustawahan,
            'xalqadaha':xalqada,
            'ardadaMustahaan':ardada,
        }
        return render(request,'darulxadith_pr/xogta-mustawahaan.html',data)

def addXalqad(request):
    state=''
    xalqadaha = Xalqada.objects.all()
    mustawayasha=Mustawaha.objects.all()
    
    if request.POST:
        magacaMustawaha=request.POST.get('magaca-mustawaha')
        magacaXalqada=request.POST.get('magaca-xalqada')
        if  Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=magacaMustawaha)).filter(magacaXalqada=magacaXalqada).exists():
            state="Horay ayuu u diiwangashnaa gashnaa"
            print(state)
        else:
            state="Ma diiwaangashno"
            print(state)
            Xalqada.objects.create(mustawaha=Mustawaha.objects.get(magacaMustawaha=magacaMustawaha),magacaXalqada=magacaXalqada)

   
    data={
        'mustawayasha':mustawayasha,
        'xalqadaha':xalqadaha,
        'state':state
    }
    return render(request,'darulxadith_pr/xalqadaha.html',data)

def diiwangalintaArdada(request):

    state=''
    xalqadaha = Xalqada.objects.all()
    sanadDugsiyedka=SanadDugsiyeedka.objects.all()
    if request.POST:
        magacaArdayga=request.POST.get('magaca-ardayga')
        jinsiga=request.POST.get('jinsiga')
        meeshaDhalashada=request.POST.get('meesha-dhalashada')
        waqtigaDhalashada=request.POST.get('tarikhda-dhalashada')
        numberkaArdayga=request.POST.get('numberka-ardayga')
        mustawaha=request.POST.get('mustawaha')
        magacaMasuulka=request.POST.get('magaca-masuulka')
        numberkaMasuulka=request.POST.get('numberka-masuulka')
        if Ardada.objects.filter(magacaArdayga=magacaArdayga).exists():
            state="Horay ayaad u diwaangalisay"
            
        else:
            mustwaha=mustawaha.split(",")[0]
            raqamka=mustawaha.split(",")[1]
            Ardada.objects.create(
                magacaArdayga=magacaArdayga,
                jinsiga=jinsiga,
                meeshaDhalashada=meeshaDhalashada,
                waqtigaDhalashada=waqtigaDhalashada,
                numberkaArdayga=numberkaArdayga,
                mustawahaArdayga=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=mustwaha)).get(magacaXalqada=raqamka),
                magacaMasuulka=magacaMasuulka,
                numberkaMasuulka=numberkaMasuulka)
            state="Waad diiwaangalisay Ardaygaan"
           
                        



            


            
        
    data={
        'sanadDugsiyedka':sanadDugsiyedka,
        'xalqadaha':xalqadaha,
        'state':state
    }

    return render(request,'darulxadith_pr/diiwangalinta_ardada.html',data)
def updateArdaygan(request):
    mustawaha = request.POST.get('mustawahaArdayga').split(" -- ")[0]
    raqamka = request.POST.get('mustawahaArdayga').split(" -- ")[1]
    ardaygan=Ardada.objects.get(id=request.POST.get('id'))
    ardaygan.magacaArdayga=request.POST.get('magacaArdayga')
    ardaygan.jinsiga=request.POST.get('jinsiga')
    ardaygan.meeshaDhalashada=request.POST.get('meeshaDhalashada')
    ardaygan.waqtigaDhalashada=request.POST.get('waqtigaDhalashada')
    ardaygan.numberkaArdayga=request.POST.get('numberkaArdayga')
    # ardaygan.mustawahaArdayga= Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaArdayga=mustawaha))
    ardaygan.magacaMasuulka=request.POST.get('magacaMasuulka')
    ardaygan.numberkaMasuulka=request.POST.get('numberkaMasuulka')
    # ardaygan.sanadDugsiyedka=request.POST.get('sanadDugsiyedka')
    ardaygan.tarikhdaDiwangalinta=request.POST.get('tarikhdaDiwangalinta')
    ardaygan.save()
    
    return JsonResponse({'response':True})


def deleteArdaygaan(request):
    status=False
    ardaygan=Ardada.objects.get(pk=request.POST.get('id'))
    if ardaygan.delete():
        print("")
        status=True
    else:
        status=False
    return JsonResponse({'response':status})

def xogtaArdada(request):
    ardada=Ardada.objects.all()
    data={
        'ardada':ardada
    }
    return render(request,'darulxadith_pr/xogta-ardada.html',data)

def xogtaXalqadaan(request,pk):
    return render(request,'darulxadith_pr/xogta_xalqadaan.html')

def imtixaanadka(request):
    data={
        'xalqadaha':Xalqada.objects.all(),
        'ardada':Ardada.objects.all()
    }
    return render(request,'darulxadith_pr/imtixaanadka.html',data)


def ardadaXalqadaan(request,xalqada,raqamka):
    ardadaXalqadaan=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka)
    ardada=Ardada.objects.filter(mustawahaArdayga=ardadaXalqadaan)
    data={
        'xalqadaha':Xalqada.objects.all(),
        'ardada':ardada
    }
    return render(request,'darulxadith_pr/imtixaanadka.html',data)

def qaadistaBuundoyinka(request,xalqada,raqamka,magaca_ardayga):
    imtixankaShafawi1Ardaygan=Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).filter(imtixanka=magacyadaImtixanada[0])
    imtixankaNisfigaArdaygan=Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).filter(imtixanka=magacyadaImtixanada[1])
    imtixankaShagawi2Ardaygan=Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).filter(imtixanka=magacyadaImtixanada[2])
    imtixankaAakhirArdaygan=Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).filter(imtixanka=magacyadaImtixanada[3])

    imtixanada = zip(imtixankaShafawi1Ardaygan,imtixankaNisfigaArdaygan,imtixankaShagawi2Ardaygan,imtixankaAakhirArdaygan)

    # helida maadoyinka fasalka
    ardayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)
    dhamaanMaadonyinkaArdayga=Mustawaha.objects.get(magacaMustawaha=xalqada).maadoyinka.split(",")
    mustwaha=str(ardayga.mustawahaArdayga).split(" -- ")[0]
    raqamka=str(ardayga.mustawahaArdayga).split(" -- ")[1]
   # imtixanka=Imtixaanada.objects.all()[0].magacaImtixanka
    hasImtixan= False
    if Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).exists():
        hasImtixan=True
    else:
        hasImtixan=False
    data={
        'sanadDugsiyeedyada':SanadDugsiyeedka.objects.all(),
        'mustwaha':mustwaha,
        'hasImtixan':hasImtixan,
        'raqamka':raqamka,
        'ardayga':ardayga,
        'fasalka':xalqada,
        'maadoyinka':dhamaanMaadonyinkaArdayga,
        'magacyadaImtixanada':magacyadaImtixanada,
        'sanadDugsiyeedkaHadda':sanadDugsiyeedkaHadda,
        'imtixanada':imtixanada,
        # 'imtixanka':imtixanka
    }
    return render(request,'darulxadith_pr/qaadista_buundoyinka.html',data)


def xogtaArdaygan(request,magaca_ardayga):
    imtixankaShafawi1Ardaygan=Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).filter(imtixanka=magacyadaImtixanada[0])
    imtixankaNisfigaArdaygan=Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).filter(imtixanka=magacyadaImtixanada[1])
    imtixankaShagawi2Ardaygan=Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).filter(imtixanka=magacyadaImtixanada[2])
    imtixankaAakhirArdaygan=Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).filter(imtixanka=magacyadaImtixanada[3])

    xalqada=Ardada.objects.get(magacaArdayga=magaca_ardayga).mustawahaArdayga.mustawaha.magacaMustawaha
    imtixanada = zip(imtixankaShafawi1Ardaygan,imtixankaNisfigaArdaygan,imtixankaShagawi2Ardaygan,imtixankaAakhirArdaygan)
    ardayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)
    dhamaanMaadonyinkaArdayga=Mustawaha.objects.get(magacaMustawaha=xalqada).maadoyinka.split(",")
    mustwaha=str(ardayga.mustawahaArdayga).split(" -- ")[0]
    raqamka=str(ardayga.mustawahaArdayga).split(" -- ")[1]
    xaadiriska=Xaadiriska.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga))
    hasImtixan= False
    if Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).exists():
        hasImtixan=True
    else:
        hasImtixan=False
    data={
        'xaadiriska':xaadiriska,
        'mulaaxadaatka':Mulaaxadaat.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)),
        'hasImtixan':hasImtixan,
        'sanadDugsiyeedyada':SanadDugsiyeedka.objects.all(),
        'imtixanada':imtixanada,
        'mustwaha':mustwaha,
        'raqamka':raqamka,
        'ardayga':ardayga,
        'fasalka':xalqada,
        'magacyadaImtixanada':magacyadaImtixanada,
        'ardaygan':Ardada.objects.get(magacaArdayga=magaca_ardayga),
        'imtixaanadka':Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)),
        'sanadDugsiyeedkaHadda':sanadDugsiyeedkaHadda,
        'maadoyinka':dhamaanMaadonyinkaArdayga,
    }
    return render(request,'darulxadith_pr/xogta-ardaygan.html',data)

def xadiriskaArdaygaan(request,magaca_ardaygaan):
    xaadiriska=Xaadiriska.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardaygaan))
    xaadiriskaArdaygaan=[]
    if request.POST:
        for xaadiritanka in xaadiriska:
            xaadiriskaArdaygaan=[
                {
                    'id':xaadiritanka.pk,
                    'magacaArdayga':xaadiritanka.magacaArdayga.magacaArdayga,
                    'xalqada':str(xaadiritanka.xalqada),
                    'sabti1':xaadiritanka.sabti1, 'sabti2':xaadiritanka.sabti2, 'sabti3':xaadiritanka.sabti3, 'sabti4':xaadiritanka.sabti4,
                    'axad1':xaadiritanka.axad1, 'axad2':xaadiritanka.axad2, 'axad3':xaadiritanka.axad3,'axad4':xaadiritanka.axad4,
                    'isniin1':xaadiritanka.isniin1,'isniin2':xaadiritanka.isniin2,'isniin3':xaadiritanka.isniin3,'isniin4':xaadiritanka.isniin4,
                    'talaado1':xaadiritanka.talaado1,'talaado2':xaadiritanka.talaado2,'talaado3':xaadiritanka.talaado3,'talaado4':xaadiritanka.talaado4,
                    'arbaco1':xaadiritanka.arbaco1,'arbaco2':xaadiritanka.arbaco2,'arbaco3':xaadiritanka.arbaco3,'arbaco4':xaadiritanka.arbaco4,
                    'waqtiga':xaadiritanka.waqtiga,'waqtigaLaQadayo':xaadiritanka.waqtigaLaQadayo

                
                }
            ]
        return JsonResponse({'xaadiriska':xaadiriskaArdaygaan})

        
    data={
        'xaadiriska':xaadiriska,
        'ardaygan':Ardada.objects.get(magacaArdayga=magaca_ardaygaan)
    }
    return render(request,'darulxadith_pr/xaadiriska_ardaygan.html',data)

def hasImtixanFuntion(request):
    hasImtixan= False
    if Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=request.POST.get('magacaArdayga'))).filter(sanadka=SanadDugsiyeedka.objects.get(id=request.POST.get('sanadka'))).exists():
        hasImtixan=True
    else:
        hasImtixan=False
    return JsonResponse({'hasImtixan':hasImtixan})

def helBuundoyinkaMadaKaste(request,xalqada,raqamka,magaca_ardayga):
    # helida maadoyinka fasalka
    dhamaanMaadonyinkaArdayga=Mustawaha.objects.get(magacaMustawaha=xalqada).maadoyinka.split(',')
    
    # if Natiijada.objects.filter(magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga)).exists():
    #     print("is alreadey exit")
    # else:
    
    # for madada in dhamaanMaadonyinkaArdayga:
    #     for imtixanka in magacyadaImtixanada:
    #         buundada=request.POST.get(imtixanka+madada)
    #         if request.POST.get('sanad-dugsiyedka'):
    #             sanadDugsiyedka=SanadDugsiyeedka.objects.get(taariikhdaBillowgaHijri=request.POST.get('sanad-dugsiyedka'))
    #         else:
    #             sanadDugsiyedka=sanadDugsiyeedkaHadda
    #         Natiijada.objects.create(
    #             magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga),
    #             imtixanka=imtixanka,
    #             sanadka=sanadDugsiyedka,
    #             xalqada=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka),
    #             maadada=madada,
    #             buundada=buundada,
    #             # sanadDugsiyeedka=sanadDugsiyeedkaHadda,
    #             tarikhdaLagalay=date.today()
    #             )
    #         print(madada,imtixanka,buundada)
    return JsonResponse({'data':True})
    # return HttpResponseRedirect('/ardadaXalqadaan/'+xalqada+'/'+raqamka+'/')
@csrf_exempt    
def diiwangalintaImtixaanka(request,sanaddugsiyedka,magacaArdayga):
    xalqada=Ardada.objects.get(magacaArdayga=magacaArdayga).mustawahaArdayga.mustawaha.magacaMustawaha
    raqamka=Ardada.objects.get(magacaArdayga=magacaArdayga).mustawahaArdayga.magacaXalqada
    dhamaanMaadonyinkaArdayga=Mustawaha.objects.get(magacaMustawaha=xalqada).maadoyinka.split(',')
    for madada in dhamaanMaadonyinkaArdayga:
        for imtixanka in magacyadaImtixanada:
            buundada=request.POST.get(imtixanka+madada)
            Natiijada.objects.create(
                magacaArdayga=Ardada.objects.get(magacaArdayga=magacaArdayga),
                imtixanka=imtixanka,
                sanadka=SanadDugsiyeedka.objects.get(id=sanaddugsiyedka),
                xalqada=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka),
                maadada=madada,
                buundada=buundada if buundada!=None else 0,
                # sanadDugsiyeedka=sanadDugsiyeedkaHadda,
                tarikhdaLagalay=date.today()
                )
    return HttpResponseRedirect('/qaadista_buundoyinka/'+xalqada+'/'+raqamka+'/'+magacaArdayga+'/')


def saveGareyBuundadaArdaygan(request):
    if(request.POST):
        buundada=Natiijada.objects.get(id=request.POST.get('id'))
        buundada.buundada=request.POST.get('buundada')
        buundada.save()
        return JsonResponse({})
    return JsonResponse({})

def imtixankaXalqadaha(request):
    data={
        'xalqadaha':Xalqada.objects.all()
    }
    return render(request,'darulxadith_pr/imtixanka_xalqadaha.html',data)

def imtixankaXalqadaan(request,xalqada,raqamka):
   
    xalqadaan=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka)
    imtixanadka=Natiijada.objects.filter(xalqada=xalqadaan)
    dhamaanMaadonyinkaArdayga=Mustawaha.objects.get(magacaMustawaha=xalqada).maadoyinka.split(',')
    data={
        'xalqada':xalqada,
        'raqamka':raqamka,
        'maadooyinka':dhamaanMaadonyinkaArdayga,
        'sanadDugsiyeedka':Mustawaha.objects.get(magacaMustawaha=xalqada).sanadDugsiyeedka,
    }
    return render(request,'darulxadith_pr/imtixanka_xalqadaan.html',data)

def hel_imtixankaXalqadaan(request):
    xalqada=request.POST.get('xalqada')
    raqamka=request.POST.get('raqamka')
    xalqadaan=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka)
    imtixanadka=Natiijada.objects.filter(xalqada=xalqadaan)
    dhamaanMaadonyinkaArdayga=Mustawaha.objects.get(magacaMustawaha=xalqada).maadoyinka.split(',')
    magacayadaArdayda=[]

    
    for imt in imtixanadka:
        if str(imt.magacaArdayga) not in magacayadaArdayda:
           magacayadaArdayda.append(str(imt.magacaArdayga))

    return JsonResponse({
        'magacayadaArdayda':magacayadaArdayda,
        })
def helImtixaankaArdaygaan(request):
    xalqada=request.POST.get('xalqada')
    raqamka=request.POST.get('raqamka')
    ardaygan=request.POST.get('magacayadaArdayga')
    xalqadaan=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka)
    imtixanadka=Natiijada.objects.filter(xalqada=xalqadaan)
    dhamaanMaadonyinkaArdayga=Mustawaha.objects.get(magacaMustawaha=xalqada).maadoyinka.split(',')
    buundadaArdaygaan=[]

    for maadada in dhamaanMaadonyinkaArdayga:
            totalkaMadadan=0
            for natijada in imtixanadka.filter(maadada=maadada).filter(magacaArdayga=Ardada.objects.get(magacaArdayga=ardaygan)):
                totalkaMadadan=totalkaMadadan+natijada.buundada
            buundadaArdaygaan.append(totalkaMadadan)
    return JsonResponse({
        'buundadaArdaygaan':buundadaArdaygaan,
        'xalqada':xalqada,
        'raqamka':raqamka
    })

def xaadiriska(request):
    xalqada=Xalqada.objects.all()
    data={
        'xalqadaha':xalqada,
    }
    return render(request,'darulxadith_pr/xaadiriska.html',data)





def xaadiriskaXalqadaan(request,xalqada,raqamka):
    ardada = Ardada.objects.filter(mustawahaArdayga=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka))
    data={
        'ardadaXalqadaan':ardada,
        'xalqada':xalqada,
        'raqamka':raqamka
    }
    return render(request,'darulxadith_pr/xaadiriska_xalqadaan.html',data)

def qadistaXaadiriska(request,xalqada,raqamka):
    print(request.POST)
    return JsonResponse({})


def qadistaXaadiriska(request,xalqada,raqamka):
    magacaArdada = []
    ardada = Ardada.objects.filter(mustawahaArdayga=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka))
    xogtaArdadaXaadiriska=Xaadiriska.objects.filter(xalqada=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka))
    
    for ardayga in ardada:
        magacaArdada.append(ardayga.magacaArdayga)
        
    print(magacaArdada[1])
    if(request.method == 'POST'):
        # sabti
        sabti1=request.POST.getlist('sabti1[]')
        sabti2=request.POST.getlist('sabti2[]')
        sabti3=request.POST.getlist('sabti3[]')
        sabti4=request.POST.getlist('sabti4[]')
        # axad
        axad1=request.POST.getlist('axad1[]')
        axad2=request.POST.getlist('axad2[]')
        axad3=request.POST.getlist('axad3[]')
        axad4=request.POST.getlist('axad4[]')
        # isniin
        isniin1=request.POST.getlist('isniin1[]')
        isniin2=request.POST.getlist('isniin2[]')
        isniin3=request.POST.getlist('isniin3[]')
        isniin4=request.POST.getlist('isniin4[]')
        # talaadu
        talaado1=request.POST.getlist('talaado1[]')
        talaado2=request.POST.getlist('talaado2[]')
        talaado3=request.POST.getlist('talaado3[]')
        talaado4=request.POST.getlist('talaado4[]')
        # arbaco
        arbaco1=request.POST.getlist('arbaco1[]')
        arbaco2=request.POST.getlist('arbaco2[]')
        arbaco3=request.POST.getlist('arbaco3[]')
        arbaco4=request.POST.getlist('arbaco4[]')


        try:
            if(xogtaArdadaXaadiriska.latest('waqtiga').waqtigaLaQadayo <= date.today()):
                for index,ardayga in enumerate(magacaArdada):
                    Xaadiriska.objects.create(
                        magacaArdayga = Ardada.objects.get(magacaArdayga=magacaArdada[index]),
                        xalqada = Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka),
                        sabti1 = sabti1[index], sabti2 = sabti2[index],sabti3 = sabti3[index], sabti4 = sabti4[index],
                        axad1 = axad1[index], axad2 = axad2[index],axad3 = axad3[index], axad4 = axad4[index],
                        isniin1 = isniin1[index], isniin2 = isniin2[index],isniin3 = isniin3[index], isniin4 = isniin4[index],
                        talaado1 = talaado1[index], talaado2 = talaado2[index],talaado3 = talaado3[index], talaado4 = talaado4[index],
                        arbaco1 = arbaco1[index], arbaco2=arbaco2[index],arbaco3 = arbaco3[index], arbaco4=arbaco4[index],
                        waqtiga=date.today(),
                        waqtigaLaQadayo=date.today()+timedelta(7)
                        # waqtiga= str(str(datetime.datetime(2021, 06, 23, 18, 00)).split(" ")[0]),
                        # waqtigaLaQadayo=str(str(datetime.datetime(2021, 06, 30, 18, 00)).split(" ")[0])
                        )
                return JsonResponse({'success':True})

            else:
                print("horey ayad u diwangalisay")
                return JsonResponse({'success':False})
        except:
            for index,ardayga in enumerate(magacaArdada):
                Xaadiriska.objects.create(
                    magacaArdayga = Ardada.objects.get(magacaArdayga=magacaArdada[index]),
                    xalqada = Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka),
                    sabti1 = sabti1[index], sabti2 = sabti2[index],sabti3 = sabti3[index], sabti4 = sabti4[index],
                    axad1 = axad1[index], axad2 = axad2[index],axad3 = axad3[index], axad4 = axad4[index],
                    isniin1 = isniin1[index], isniin2 = isniin2[index],isniin3 = isniin3[index], isniin4 = isniin4[index],
                    talaado1 = talaado1[index], talaado2 = talaado2[index],talaado3 = talaado3[index], talaado4 = talaado4[index],
                    arbaco1 = arbaco1[index], arbaco2=arbaco2[index],arbaco3 = arbaco3[index], arbaco4=arbaco4[index],

                    waqtiga=date.today(),
                    waqtigaLaQadayo=date.today()+timedelta(7)
                    )
                print("success in as first")
            return JsonResponse({'success':True})



    return JsonResponse({'success':False})
    # for index,ardayga in enumerate(magacaArdada):

def attendencePrint(request,xalqada,raqamka,jinsiga):
    ardada=Ardada.objects.filter(mustawahaArdayga=Xalqada.objects.filter(mustawaha=Mustawaha.objects.get(magacaMustawaha=xalqada)).get(magacaXalqada=raqamka)).filter(jinsiga=jinsiga)
    data={
        'ardada':ardada,
        'jinsiga':jinsiga,
        'xalqada':xalqada,
        'raqamka':raqamka
    }
    return render(request,'attendence_print.html',data)



def diiwangalintaMulaaxadatka(request,magaca_ardayga):
    cinwanka=request.POST.get('cinwanka'),
    faahfahin=request.POST.get('faahfahin')

    Mulaaxadaat.objects.create(
        magacaArdayga=Ardada.objects.get(magacaArdayga=magaca_ardayga),
        cinwanka=cinwanka,
        faahfahin=faahfahin
    )
    return HttpResponseRedirect('/xogta_ardaygan/'+magaca_ardayga+'/')
