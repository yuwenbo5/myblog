# Generated by Django 2.1 on 2018-08-17 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('logo', models.ImageField(default='logo', upload_to='article_logo', verbose_name='文章logo')),
                ('desc', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('type', models.CharField(default='normal', max_length=20)),
                ('cate_id', models.SmallIntegerField(default=0)),
                ('look_nums', models.SmallIntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('create_id', models.CharField(max_length=50)),
                ('create_time', models.DateTimeField()),
                ('operate_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('img', models.ImageField(default='banner', upload_to='banner_img', verbose_name='首页轮播')),
                ('desc', models.CharField(max_length=255)),
                ('sort', models.SmallIntegerField()),
                ('operate_id', models.CharField(max_length=30)),
                ('operate_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Cate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cate_name', models.CharField(max_length=200)),
                ('cate_desc', models.CharField(max_length=255)),
                ('pid', models.IntegerField()),
                ('sort', models.SmallIntegerField(default=0)),
                ('operate_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=200)),
                ('desc', models.CharField(default='', max_length=255)),
                ('operate_id', models.CharField(max_length=32)),
                ('operate_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.IntegerField()),
                ('comment_content', models.TextField()),
                ('comment_id', models.CharField(max_length=50)),
                ('comment_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.TextField()),
                ('type', models.CharField(default='base', max_length=20)),
                ('create_time', models.DateTimeField()),
                ('operate_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('desc', models.CharField(max_length=255)),
                ('file_path', models.FileField(default='file', upload_to='myfile/%Y/%m', verbose_name='文献')),
                ('operate_id', models.CharField(max_length=32)),
                ('operate_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='FriendsLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_name', models.CharField(max_length=30)),
                ('link_url', models.CharField(max_length=200)),
                ('link_desc', models.CharField(max_length=255)),
                ('link_status', models.CharField(default='', max_length=10)),
                ('link_sort', models.SmallIntegerField(default=0)),
                ('operate_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=30)),
                ('p_img', models.ImageField(default='photo', upload_to='myphotos/%Y/%m', verbose_name='相册')),
                ('upload_id', models.CharField(max_length=20)),
                ('upload_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=32)),
                ('user_password', models.CharField(max_length=32)),
                ('user_email', models.CharField(max_length=50)),
                ('user_type', models.CharField(default='normal', max_length=20)),
                ('create_time', models.DateTimeField()),
            ],
        ),
    ]
