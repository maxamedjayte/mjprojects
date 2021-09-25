# Generated by Django 3.2.7 on 2021-09-25 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('darulxadith_system', '0011_alter_ardada_sanaddugsiyedka'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mulaaxadaat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cinwanka', models.TextField()),
                ('faahfahin', models.TextField()),
                ('waqtiga', models.DateField(auto_now=True)),
                ('magacaArdayga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darulxadith_system.ardada')),
            ],
        ),
    ]
