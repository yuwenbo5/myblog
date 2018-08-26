# -*- coding:utf-8 -*-

from django.shortcuts import render
from blog import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import simplejson
import os
import time
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from myblog import settings
from django.db.models import Q

# Create your views here.
#登录处理
def login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        import hashlib
        password = hashlib.md5(password.encode('utf8')).hexdigest()

        if models.User.objects.filter(user_id=username,user_password=password):
            user = models.User.objects.get(user_id=username)
            request.session['user_id'] = user.user_id
            request.session['user_email'] = user.user_email
            request.session['expire_time'] = time.time() + 3600 * 2

            return HttpResponseRedirect('/administrator/index/')
        else:
            return render(request,'administrator/login.html',{'code':0,'msg':'用户名或密码错误'})
    else:
        return render(request,'administrator/login.html')

#验证是否登录装饰器
def my_login_required(func):
    def login_check(request):
        # 添加超级用户
        if not models.User.objects.filter(user_type='admin'):
            import hashlib
            adminUser = models.User()
            adminUser.user_id = 'administrator'
            adminUser.user_password = hashlib.md5(b'123456').hexdigest()
            adminUser.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            adminUser.user_type = 'admin'
            adminUser.save()
            return func(request)

        if not request.session.has_key('expire_time'):
            return HttpResponseRedirect('/administrator/login/')
        else:
            if request.session.get('expire_time')<time.time():
                # request.sesstion.clear()
                # request.sesstion.flush()
                return render(request, 'administrator/login.html', {'code': 0, 'msg': '登录已过期，请重新登录'})
            else:
                return func(request)
    return login_check

#注销
def logout(request):
    request.session.clear()
    request.session.flush()
    return HttpResponseRedirect('/administrator/login/')


#管理页面开始
@my_login_required
def index(request):

    return render(request,'administrator/index.html')

@my_login_required
def setinfo(request):
    contents = {}
    if request.method == 'POST':
        banner_img = request.FILES.get('img')
        contents['home_title'] = request.POST.get('home_title')
        contents['home_desc'] = request.POST.get('content')
        contents['nick_name'] = request.POST.get('s_name')
        contents['my_job'] = request.POST.get('s_400')
        contents['my_phone'] = request.POST.get('s_phone')
        contents['qq'] = request.POST.get('s_qq')
        contents['my_email'] = request.POST.get('s_email')
        contents['weixin'] = request.POST.get('s_fax')
        contents['weibo'] = request.POST.get('s_qqu')
        contents['web_keywords'] = request.POST.get('skeywords')
        contents['web_desc'] = request.POST.get('sdescription')
        #先上传文件
        if banner_img:
            filepath = os.path.join(settings.BASE_DIR,'media','banner')
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filename = os.path.join(filepath,banner_img.name)
            f = open(filename,'wb')
            for chunk in banner_img.chunks():
                f.write(chunk)
            f.close()
            contents['banner_img'] = filename.replace(settings.BASE_DIR,'')
        #上传完成

        #保存数据,name值存在更新,不存在插入
        for key, value in contents.items():
            if models.Config.objects.filter(name=key):
                models.Config.objects.filter(name=key).update(value=value,type='base',create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),operate_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            else:
                config = models.Config()
                config.name = key
                config.value = value
                config.type = 'base'
                config.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                config.operate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                config.save()
        return render(request,'administrator/tips.html',{'code':1,'msg':'success','url':'/administrator/setinfo/','waitsecond':4})
    # 基本配置内容
    for val in models.Config.objects.filter(type='base'):
        contents[val.name] = val

    return render(request, 'administrator/setinfo.html', contents)

@my_login_required
def password(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        password = request.POST.get('newpass')
        user_email = request.POST.get('memail')
        import hashlib
        password = hashlib.md5(password.encode('utf8')).hexdigest()
        models.User.objects.filter(user_id=user_id).update(user_password = password,user_email = user_email,create_time = models.User.objects.get(user_id=user_id).create_time)

        #清除session重新登录
        request.session.clear()
        request.session.flush()
        return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/login/', 'waitsecond': 4})
    else:
        return render(request, 'administrator/password.html')

#首页轮播
@my_login_required
def adv(request):
    contents = {}
    if request.method == 'POST':
        name = request.POST.get('title')
        desc = request.POST.get('note')
        sort = request.POST.get('sort')
        img_file = request.FILES.get('img')
        operate_id = request.session.get('user_id')
        operate_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
        #上传图片
        if img_file:
            filepath = os.path.join(settings.BASE_DIR,'media','banner')
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filename = os.path.join(filepath,img_file.name)
            f = open(filename,'wb')
            for chunk in img_file.chunks():
                f.write(chunk)
            f.close()
            img = filename.replace(settings.BASE_DIR,'')
        else:
            img = ''
            #上传完成
        if request.POST.get('actionId') == 'add':
            banner = models.Banner()
            banner.name = name
            banner.img = img
            banner.desc = desc
            banner.sort = sort
            banner.operate_id = operate_id
            banner.operate_time = operate_time
            banner.save()

        if request.POST.get('actionId') == 'update':
            id = request.POST.get('id')
            if img == '':
                img = models.Banner.objects.get(id=id).img
            models.Banner.objects.filter(id=id).update(name=name,img=img,desc=desc,sort=sort,operate_id=operate_id,operate_time=operate_time)

        return render(request,'administrator/tips.html',{'code':1,'msg':'success','url':'/administrator/adv/','waitsecond':4})

    else:
        contents['banner_list'] = models.Banner.objects.all().order_by('sort')[:4]
        if request.GET.get('id') and models.Banner.objects.filter(id=request.GET.get('id')):
            contents['banner'] = models.Banner.objects.get(id=request.GET.get('id'))

        return render(request, 'administrator/adv.html', contents)

@my_login_required
def page(request):
    contents = {}
    if request.method == 'POST':
        contents['about_content'] = request.POST.get('content')
        img_file = request.FILES.get('img')
        #上传文件
        if img_file:
            filepath = os.path.join(settings.BASE_DIR,'media','about')
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filename = os.path.join(filepath,img_file.name)
            f = open(filename,'wb')
            for chunk in img_file.chunks():
                f.write(chunk)
            f.close()
            contents['about_img'] = filename.replace(settings.BASE_DIR,'')
        #文件上传完毕

        # 保存数据,name值存在更新,不存在插入
        for key, value in contents.items():
            if key == '':
                continue
            if models.Config.objects.filter(name=key):
                models.Config.objects.filter(name=key).update(value=value,type='about',create_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),operate_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
            else:
                config = models.Config()
                config.name = key
                config.value = value
                config.type = 'about'
                config.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                config.operate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                config.save()

        return render(request,'administrator/tips.html',{'code':1,'msg':'success','url':'/administrator/page/','waitsecond':4})
    else:
        for val in models.Config.objects.filter(type='about'):
            contents[val.name] = val

        return render(request, 'administrator/page.html', contents)

@my_login_required
def bloglist(request):
    page = request.GET.get('page')
    if page is None:
        page = 1
    type = {'home':'首页','normal':'列表页'}
    contents = {}
    blog_list = models.Article.objects.all().order_by('id')
    article_list = []
    i = 0
    for val in blog_list:
        val.type = type[val.type]
        val.cate = models.Cate.objects.get(id=val.cate_id).cate_name
        article_list.append(val)
    paginator = Paginator(article_list, 5)
    try:
        contents['article_list'] = paginator.page(page)
    except PageNotAnInteger:
        contents['article_list'] = paginator.page(1)
    except EmptyPage:
        contents['article_list'] = paginator.page(paginator.num_pages)

    contents['cate'] = models.Cate.objects.all()
    contents['type'] = type
    contents['page'] = page
    return render(request, 'administrator/bloglist.html', contents)

@my_login_required
def addblog(request):
    contents = {}
    type = {'home': '首页', 'normal': '列表页'}
    contents['cate'] = models.Cate.objects.all()
    contents['type'] = type

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            contents['article'] = models.Article.objects.get(id=id)
        return render(request, 'administrator/addblog.html', contents)

    if request.method == 'POST':
        title = request.POST.get('title')
        logo = ''
        cate_id = request.POST.get('cid')
        type = request.POST.get('type')
        desc = request.POST.get('note')
        content = request.POST.get('content')
        operate_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
        create_id = 'administrator'
        create_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
        img_file = request.FILES.get('logo')
        # 上传文件
        if img_file:
            filepath = os.path.join(settings.BASE_DIR, 'media', 'blog')
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filename = os.path.join(filepath, img_file.name)
            f = open(filename, 'wb')
            for chunk in img_file.chunks():
                f.write(chunk)
            f.close()
            logo = filename.replace(settings.BASE_DIR,'')

        if request.POST.get('id') and models.Article.objects.filter(id=request.POST.get('id')):
            if logo == '':
                logo = models.Article.objects.get(id=request.POST.get('id')).logo
            models.Article.objects.filter(id=request.POST.get('id')).update(title=title, logo=logo,cate_id=cate_id,type=type,desc=desc,content=content,create_id=create_id,operate_time=operate_time)
            return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/bloglist/', 'waitsecond': 4})
        else:
            blog = models.Article()
            blog.title = title
            blog.logo = logo
            blog.cate_id = cate_id
            blog.type = type
            blog.desc = desc
            blog.content = content
            blog.create_id = create_id
            blog.create_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
            blog.operate_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
            blog.save()
            return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/bloglist/', 'waitsecond': 4})

@my_login_required
def cate(request):
    contents = {}
    if request.method == 'POST':
        cate = models.Cate()
        cate.pid = 0
        cate.cate_name = request.POST.get('title')
        cate.cate_desc = request.POST.get('s_desc')
        cate.sort = request.POST.get('sort')
        cate.operate_time = time.strftime('%Y-%m-%d %H:%I:%S',time.localtime())
        cate.save()
        return render(request,'administrator/tips.html',{'code':1,'msg':'success','url':'/administrator/cate/','waitsecond':4})
    else:
        contents['cate_list'] = models.Cate.objects.all()
        return render(request, 'administrator/cate.html', contents)

@my_login_required
def cateedit(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if models.Cate.objects.filter(id=id):
            cate_name = request.POST.get('title')
            cate_desc = request.POST.get('s_desc')
            sort = request.POST.get('sort')
            operate_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
            models.Cate.objects.filter(id=id).update(cate_name=cate_name, cate_desc=cate_desc, sort=sort,operate_time=operate_time)
            return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/cate/', 'waitsecond': 4})
        else:
            return render(request, 'administrator/tips.html',{'code': 0, 'msg': '参数提交错误', 'url': '/administrator/cate/', 'waitsecond': 4})
    if request.method == 'GET':
        contents = {}
        id = request.GET.get('id')
        if models.Cate.objects.filter(id=id):
            contents['cate'] = models.Cate.objects.get(id=id)
            return render(request,'administrator/cateedit.html',contents)
        else:
            return render(request,'administrator/tips.html',{'code':0,'msg':'参数提交错误','url':'/administrator/cate/','waitsecond':4})

#文献列表
@my_login_required
def document(request):
    contents = {}
    if request.method == 'POST':
        name = request.POST.get('title')
        desc = request.POST.get('s_desc')
        document_file = request.FILES.get('file')
        operate_id = request.session.get('user_id')
        operate_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
        # 上传图片
        if document_file:
            filepath = os.path.join(settings.BASE_DIR, 'media', 'document')
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filename = os.path.join(filepath, document_file.name)
            f = open(filename, 'wb')
            for chunk in document_file.chunks():
                f.write(chunk)
            f.close()
            file_path = filename.replace(settings.BASE_DIR, '')
        else:
            file_path = ''
            # 上传完成
        if request.POST.get('actionId') == 'add':
            document = models.Document()
            document.name = name
            document.desc = desc
            document.file_path = file_path
            document.operate_id = operate_id
            document.operate_time = operate_time
            document.save()

        if request.POST.get('actionId') == 'update':
            id = request.POST.get('id')
            if file_path == '':
                file_path = models.Document.objects.get(id=id).file_path
            models.Document.objects.filter(id=id).update(name=name, file_path=file_path, desc=desc, operate_id=operate_id,operate_time=operate_time)

        return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/document/', 'waitsecond': 4})

    else:
        page = request.GET.get('page')
        if page is None:
            page = 1
        documents = models.Document.objects.all().order_by('id')[:4]
        paginator = Paginator(documents, 5)
        try:
            contents['documents'] = paginator.page(page)
        except PageNotAnInteger:
            contents['documents'] = paginator.page(1)
        except EmptyPage:
            contents['documents'] = paginator.page(paginator.num_pages)


        if request.GET.get('id') and models.Document.objects.filter(id=request.GET.get('id')):
            contents['document'] = models.Document.objects.get(id=request.GET.get('id'))

        return render(request, 'administrator/document.html', contents)

#收藏管理
@my_login_required
def collection(request):
    contents = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('s_desc')
        url = request.POST.get('url')
        operate_id = request.session.get('user_id')
        operate_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
        if request.POST.get('actionId') == 'add':
            collection = models.Collection()
            collection.title = title
            collection.desc = desc
            collection.url = url
            collection.operate_id = operate_id
            collection.operate_time = operate_time
            collection.save()

        if request.POST.get('actionId') == 'update':
            id = request.POST.get('id')
            models.Collection.objects.filter(id=id).update(title=title, url=url, desc=desc,operate_id=operate_id, operate_time=operate_time)

        return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/collection/', 'waitsecond': 4})

    else:
        page = request.GET.get('page')
        if page is None:
            page = 1
        collections = models.Collection.objects.all().order_by('id')
        paginator = Paginator(collections, 5)
        try:
            contents['collections'] = paginator.page(page)
        except PageNotAnInteger:
            contents['collections'] = paginator.page(1)
        except EmptyPage:
            contents['collections'] = paginator.page(paginator.num_pages)

        if request.GET.get('id') and models.Collection.objects.filter(id=request.GET.get('id')):
            contents['collection'] = models.Collection.objects.get(id=request.GET.get('id'))

        return render(request, 'administrator/collection.html', contents)


#友情链接
@my_login_required
def link(request):
    contents = {}
    status = {'1':'可用','0':'禁用'}
    contents['status'] = status
    if request.method == 'POST':
        link_name = request.POST.get('title')
        link_desc = request.POST.get('s_desc')
        link_url = request.POST.get('url')
        link_status = request.POST.get('status')
        link_sort = request.POST.get('sort')
        operate_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
        if request.POST.get('actionId') == 'add':
            link = models.FriendsLink()
            link.link_name = link_name
            link.link_desc = link_desc
            link.link_url = link_url
            link.link_status = link_status
            link.link_sort = link_sort
            link.operate_time = operate_time
            link.save()

        if request.POST.get('actionId') == 'update':
            id = request.POST.get('id')
            models.FriendsLink.objects.filter(id=id).update(link_name=link_name, link_desc=link_desc, link_url=link_url,link_status=link_status,link_sort=link_sort, operate_time=operate_time)

        return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/link/', 'waitsecond': 4})

    else:
        page = request.GET.get('page')
        if page is None:
            page = 1
        links_tmp = models.FriendsLink.objects.filter(link_status='1').order_by('link_sort')[:9]
        links = []
        for val in links_tmp:
            val.link_status = status[val.link_status]
            links.append(val)
        paginator = Paginator(links, 5)
        try:
            contents['links'] = paginator.page(page)
        except PageNotAnInteger:
            contents['links'] = paginator.page(1)
        except EmptyPage:
            contents['links'] = paginator.page(paginator.num_pages)

        if request.GET.get('id') and models.FriendsLink.objects.filter(id=request.GET.get('id')):
            contents['link'] = models.FriendsLink.objects.get(id=request.GET.get('id'))

        return render(request, 'administrator/link.html', contents)

@my_login_required
def photos(request):
    contents = {}
    if request.method == 'GET':
        contents['photos'] = models.Photos.objects.all().order_by('id')
        if request.GET.get('id'):
            id = request.GET.get('id')
            contents['photo'] = models.Photos.objects.get(id=id)
        return render(request,'administrator/photos.html',contents)
    if request.method == 'POST':
        name = request.POST.get('title')
        desc = request.POST.get('desc')
        operate_id = request.session.get('user_id')
        operate_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
        if request.POST.get('id'):
            if models.Photos.objects.filter(id=request.POST.get('id')):
                models.Photos.objects.filter(id=request.POST.get('id')).update(name=name,desc=desc,operate_id=operate_id,operate_time=operate_time)
                return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/photos/', 'waitsecond': 4})
            else:
                return render(request,'administrator/tips.html',{'code':0,'msg':'要更新的记录不存在','url':'/administrator/photos/','waitsecond':4})
        else:
            photos = models.Photos()
            photos.name = name
            photos.desc = desc
            photos.operate_id = operate_id
            photos.operate_time = operate_time
            photos.save()
            return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/photos/', 'waitsecond': 4})

@my_login_required
def picture(request):
    contents = {}
    if request.method == 'GET':
        contents['photos'] = models.Photos.objects.all().order_by('id')
        if request.GET.get('pid'):
            contents['photo'] = models.Photos.objects.get(id=request.GET.get('pid'))
            pictures = []
            i = 1
            for picture_item in models.Picture.objects.filter(pid=request.GET.get('pid')).order_by('id'):
                picture_item.num = i
                pictures.append(picture_item)
                i = i + 1
            contents['pictures'] = pictures
            return render(request,'administrator/picture.html',contents)
        else:
            return render(request, 'administrator/photos.html', contents)
    if request.method == 'POST':
        img_file = request.FILES.getlist('img')
        pid = request.POST.get('pid')
        operate_id = request.session.get('user_id')
        operate_time = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime())
        if img_file:
            logo = models.Photos.objects.get(id=pid).logo
            for img in img_file:
                filepath = os.path.join(settings.BASE_DIR, 'media', pid)
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                filename = os.path.join(filepath, img.name)
                f = open(filename, 'wb')
                for chunk in img.chunks():
                    f.write(chunk)
                f.close()
                file_path = filename.replace(settings.BASE_DIR, '')
                if not file_path:
                    continue
                picture = models.Picture()
                picture.name = img.name
                picture.desc = img.name
                picture.pid = pid
                picture.img = file_path
                picture.status = 1
                picture.operate_id = operate_id
                picture.operate_time = operate_time
                picture.save()
                if logo == '':
                    logo = file_path

            #更新对应相册的照片数
            picture_nums = models.Picture.objects.filter(pid=pid,status=1).count()
            models.Photos.objects.filter(id=pid).update(picture_nums=picture_nums,logo=logo)

            return render(request, 'administrator/tips.html',{'code': 1, 'msg': 'success', 'url': '/administrator/picture/?pid='+pid, 'waitsecond': 4})
        else:
            return render(request, 'administrator/tips.html',{'code': 0, 'msg': '请选择要上传的图片', 'url': '/administrator/picture/?pid='+pid, 'waitsecond': 4})

@my_login_required
def book(request):
    contents = {}

    return render(request, 'administrator/book.html', contents)


@my_login_required
def column(request):
    contents = {}

    return render(request, 'administrator/column.html', contents)

#ajax获取联系地址
@my_login_required
def ajaxPost(request):
    result = {}
    if request.POST.get('action') == 'checkOldPass':
        user_id = request.POST.get('user_id')
        old_pass = request.POST.get('old_pass')
        import hashlib
        old_pass = hashlib.md5(old_pass.encode('utf8')).hexdigest()
        if models.User.objects.filter(user_id=user_id,user_password=old_pass):
            result['code'] = 1
            result['msg'] = 'success'
        else:
            result['code'] = 0
            result['msg'] = 'error'
        return HttpResponse(simplejson.dumps(result))
    else:
        return HttpResponse(simplejson.dumps({'code':0,'msg':'argument submit error'}))

#删除操作
def delete_action(request):
    action = request.GET.get('action')
    id = request.GET.get('id')
    if action == '':
        return render(request, 'administrator/tips.html',{'code': 0, 'msg': '参数提交错误', 'url': '/administrator/setinfo/', 'waitsecond': 4})

    contents = {'code': 0, 'msg': 'error', 'url': '/administrator/'+action+'/', 'waitsecond': 4}
    if action == 'adv':
        models.Banner.objects.filter(id=id).delete()

    if action == 'cate':
        models.Cate.objects.filter(id=id).delete()

    if action == 'bloglist':
        models.Article.objects.filter(id=id).delete()

    if action == 'document':
        filename = settings.BASE_DIR + models.Document.objects.get(id=id).file_path.replace('/','\\')
        os.remove(filename)
        models.Document.objects.filter(id=id).delete()


    if action == 'collection':
        models.Collection.objects.filter(id=id).delete()

    if action == 'link':
        models.FriendsLink.objects.filter(id=id).delete()

    if action == 'photos':
        models.Photos.objects.filter(id=id).delete()

    if action == 'picture':
        filename = settings.BASE_DIR + models.Picture.objects.get(id=id).img.replace('/','\\')
        os.remove(filename)
        models.Picture.objects.filter(id=id).delete()

    contents['code'] = 1
    contents['msg'] = 'success'

    return render(request, 'administrator/tips.html',contents)



#editor文本编辑器上传
def upload_editor(request):
    result = {"error": 1, "message": "上传出错"}
    dir = request.GET.get('dir',None)
    if dir is None:
        return HttpResponse(simplejson.dumps(result), content_type="application/json")

    files = request.FILES.get("blogEditor", None)
    dir_name = 'editor'
    if files:
        allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp','txt','word','xlsx','xls','tmp']
        file_suffix = files.name.split(".")[-1]
        if file_suffix not in allow_suffix:
            return HttpResponse(simplejson.dumps({"error": 1, "message": "文件格式不正确"}), content_type="application/json")

        today = datetime.datetime.today()
        url_part = dir_name + '/%d/%d/' % (today.year, today.month)
        relative_path_file = os.path.join(dir_name, str(today.year), str(today.month))
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, relative_path_file)):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, relative_path_file))

        path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
        if not os.path.exists(path):  # 如果目录不存在创建目录
            os.makedirs(path)
        import uuid
        file_name = str(uuid.uuid1()) + "." + file_suffix
        path_file = os.path.join(path, file_name)
        file_url = settings.MEDIA_URL + url_part + file_name
        open(path_file, 'wb').write(files.file.read())
        result = {"error": 0, "url": file_url}

    return HttpResponse(simplejson.dumps(result), content_type="application/json")