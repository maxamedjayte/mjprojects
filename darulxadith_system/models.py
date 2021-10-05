from django.db import models
from django.db.models.base import Model
from django.db.models.fields import DateField
# Create your models here.
class SanadDugsiyeedka(models.Model):
    taariikhdaBillowgaHijri = models.CharField(max_length=10)
    taariikhdaDhamaadkaHijri = models.CharField(max_length=10)
    
    taariikhdaBillowgaMiladi=models.CharField(max_length=10)
    taariikhdaDhamaadkaMIladi=models.CharField(max_length=10)

    def __str__(self):
        return str(self.taariikhdaBillowgaHijri)+" -- "+str(self.taariikhdaDhamaadkaHijri)

class Mustawaha(models.Model):
    magacaMustawaha=models.CharField(max_length=100)
    sanadDugsiyeedka=models.ForeignKey(SanadDugsiyeedka,on_delete=models.CASCADE)
    maadoyinka=models.CharField(max_length=1000)
    def __str__(self) -> str:
        return self.magacaMustawaha


class Xalqada(models.Model):
    mustawaha=models.ForeignKey(Mustawaha,on_delete=models.CASCADE)
    magacaXalqada=models.CharField(max_length=255)
    def __str__(self) -> str:
        return str(self.mustawaha) +" -- "+ self.magacaXalqada


class Ardada(models.Model):
    magacaArdayga=models.CharField(max_length=255)
    jinsiga=models.CharField(max_length=10,default='lab')
    sawirkaArdayga=models.ImageField(null=True,blank=True, upload_to="images/sawirada_ardada/")
    meeshaDhalashada=models.CharField(max_length=100,null=True,blank=True)
    waqtigaDhalashada=models.CharField(max_length=100,null=True,blank=True)
    numberkaArdayga=models.IntegerField(null=True,default=0)
    mustawahaArdayga=models.ForeignKey(Xalqada,on_delete=models.CASCADE)
    magacaMasuulka=models.CharField(max_length=100,null=True,blank=True)
    numberkaMasuulka=models.IntegerField(null=True,default=0)
    sanadDugsiyedka=models.ForeignKey(SanadDugsiyeedka,on_delete=models.CASCADE,default=SanadDugsiyeedka.objects.all().last().id)
    tarikhdaDiwangalinta=models.CharField(max_length=12,blank=True,null=True)
    def __str__(self) -> str:
        return self.magacaArdayga

class Imtixaanada(models.Model):
    magacaImtixanka=models.CharField(max_length=255)
    sanadDugsiyeedka=models.ForeignKey(SanadDugsiyeedka,on_delete=models.CASCADE)
    tarikhdaLagalay=models.DateField()


    def __str__(self):
        return str(self.magacaImtixanka)

class Natiijada(models.Model):
    magacaArdayga=models.ForeignKey(Ardada,on_delete=models.CASCADE)
    sanadka=models.ForeignKey(SanadDugsiyeedka,on_delete=models.CASCADE)
    imtixanka=models.CharField(max_length=30)
    xalqada=models.ForeignKey(Xalqada,on_delete=models.CASCADE)
    maadada=models.CharField(max_length=50,null=True,blank=True)
    buundada=models.IntegerField(default=0)
    tarikhdaLagalay=models.CharField(null=True,blank=True,max_length=10)

    def __str__(self):
        return str(self.magacaArdayga)

class Xaadiriska(models.Model):
    magacaArdayga=models.ForeignKey(Ardada,on_delete=models.CASCADE)
    xalqada=models.ForeignKey(Xalqada,on_delete=models.CASCADE)
    sabti1=models.IntegerField(default=1)
    sabti2=models.IntegerField(default=1)
    sabti3=models.IntegerField(default=1)
    sabti4=models.IntegerField(default=1)
    axad1=models.IntegerField(default=1)
    axad2=models.IntegerField(default=1)
    axad3=models.IntegerField(default=1)
    axad4=models.IntegerField(default=1)
    isniin1=models.IntegerField(default=1)
    isniin2=models.IntegerField(default=1)
    isniin3=models.IntegerField(default=1)
    isniin4=models.IntegerField(default=1)
    talaado1=models.IntegerField(default=1)
    talaado2=models.IntegerField(default=1)
    talaado3=models.IntegerField(default=1)
    talaado4=models.IntegerField(default=1)
    arbaco1=models.IntegerField(default=1)
    arbaco2=models.IntegerField(default=1)
    arbaco3=models.IntegerField(default=1)
    arbaco4=models.IntegerField(default=1)
    waqtiga=models.DateField()
    waqtigaLaQadayo=models.DateField()

    def __str__(self):
        return str(self.xalqada)+"-"+ str(self.magacaArdayga)+"-"+str(self.waqtiga)

class Mulaaxadaat(models.Model):
    magacaArdayga=models.ForeignKey(Ardada,on_delete=models.CASCADE)
    cinwanka=models.TextField()
    faahfahin=models.TextField()
    waqtiga=models.DateField(auto_now=True)

    def __str__(self):
        return str(self.magacaArdayga)+self.cinwanka
