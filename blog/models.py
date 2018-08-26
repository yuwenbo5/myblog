from django.db import models

# Create your models here.

#创建博客基本信息配置表
class Config(models.Model):
    name = models.CharField(max_length=100)
    value = models.TextField()
    type = models.CharField(max_length=20,default='base')
    create_time = models.DateTimeField()
    operate_time = models.DateTimeField()

    def __str__(self):
        return self.name

#创建用户表
class User(models.Model):
    user_id = models.CharField(max_length=32)
    user_password = models.CharField(max_length=32)
    user_email = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20, default='normal')
    create_time = models.DateTimeField()

    def __str__(self):
        return self.user_id

#创建首页轮播表
class Banner(models.Model):
    name = models.CharField(max_length=20)
    img = models.ImageField(upload_to='banner_img',verbose_name='首页轮播',default='banner')
    desc = models.CharField(max_length=255)
    sort = models.SmallIntegerField()
    operate_id = models.CharField(max_length=30)
    operate_time = models.DateTimeField()

#创建博客分类表
class Cate(models.Model):
    cate_name = models.CharField(max_length=200)
    cate_desc = models.CharField(max_length=255)
    pid = models.IntegerField()
    sort = models.SmallIntegerField(default=0)
    operate_time = models.DateTimeField()

    def __str__(self):
        return self.cate_desc

#创建文章列表
class Article(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='article_logo',verbose_name='文章logo',default='logo')
    desc = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(max_length=20,default='normal')
    cate_id = models.SmallIntegerField(default=0)
    look_nums = models.SmallIntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    create_id = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    operate_time = models.DateTimeField()

    def __str__(self):
        return self.title

#创建文章评论表
class Comment(models.Model):
    aid = models.IntegerField()
    comment_content = models.TextField()
    comment_id = models.CharField(max_length=50)
    comment_time = models.DateTimeField()

    def __str__(self):
        return self.comment_content

#创建友情链接表
class FriendsLink(models.Model):
    link_name = models.CharField(max_length=30)
    link_url = models.CharField(max_length=200)
    link_desc = models.CharField(max_length=255)
    link_status = models.CharField(max_length=10,default='')
    link_sort = models.SmallIntegerField(default=0)
    operate_time = models.DateTimeField()

    def __str__(self):
        return self.link_name

#创建网页收藏表
class Collection(models.Model):
    title = models.CharField(max_length=30)
    url = models.CharField(max_length=200)
    desc = models.CharField(max_length=255,default='')
    operate_id = models.CharField(max_length=32)
    operate_time = models.DateTimeField()

#创建文献收集表
class Document(models.Model):
    name = models.CharField(max_length=60)
    desc = models.CharField(max_length=255)
    file_path = models.CharField(max_length=150)
    operate_id = models.CharField(max_length=32)
    operate_time = models.DateTimeField()

#创建相册表
class Photos(models.Model):
    name = models.CharField(max_length=50,default='')
    desc = models.CharField(max_length=100,default='')
    logo = models.CharField(max_length=200,default='')
    picture_nums = models.SmallIntegerField(default=0)
    operate_id = models.CharField(max_length=32,default='administrator')
    operate_time = models.DateTimeField()

#创建相册图片表
class Picture(models.Model):
    name = models.CharField(max_length=30)
    img = models.CharField(max_length=100)
    pid = models.IntegerField(default=1)
    status = models.SmallIntegerField()
    operate_id = models.CharField(max_length=32)
    operate_time = models.DateTimeField()