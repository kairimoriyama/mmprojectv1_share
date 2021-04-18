<<<<<<< HEAD
# Generated by Django 3.1.5 on 2021-03-08 13:31
=======
# Generated by Django 3.1.5 on 2021-03-07 01:30
>>>>>>> origin/main

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemNum', models.IntegerField(blank=True, null=True)),
                ('ideaNum', models.IntegerField(blank=True, default=0, null=True)),
                ('actionNum', models.IntegerField(blank=True, default=0, null=True)),
                ('submissionDate', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('staff', models.CharField(max_length=100)),
                ('title', models.TextField(max_length=2500)),
                ('description', models.TextField(max_length=2500)),
                ('refURL1', models.URLField(blank=True, max_length=300)),
                ('refURL2', models.URLField(blank=True, max_length=300)),
                ('refURL3', models.URLField(blank=True, max_length=300)),
                ('picture1', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d')),
                ('picture2', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d')),
                ('picture3', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d')),
                ('refFile1', models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d')),
                ('refFile2', models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d')),
                ('refFile3', models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d')),
                ('discussionDate', models.DateField(blank=True, null=True)),
                ('discussionNote', models.TextField(blank=True, max_length=2500)),
                ('report', models.TextField(blank=True, max_length=2500)),
                ('inchargeDivision', models.CharField(blank=True, max_length=50)),
                ('inchargeStaff', models.CharField(blank=True, max_length=50)),
                ('completionDate', models.DateField(blank=True, null=True)),
                ('adminMemo', models.CharField(blank=True, max_length=100)),
                ('deletedItem', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item_category', to='goodidea.category')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item_dividion', to='goodidea.division')),
                ('progress', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item_progress', to='goodidea.progress')),
            ],
            managers=[
                ('objects_list', django.db.models.manager.Manager()),
            ],
        ),
    ]
