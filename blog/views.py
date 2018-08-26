# -*- coding:utf-8 -*-

from django.shortcuts import render
from . import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import simplejson
from django.http import HttpResponse
import html

# Create your views here.
def index(request):
    contents = {}
    # 基本配置内容
    for val in models.Config.objects.filter(type='base'):
        contents[val.name] = val

    #最新文章
    new_article_list = models.Article.objects.all()[:3]
    contents['new_article_list'] = new_article_list

    # 分类列表
    cate = models.Cate.objects.all()
    contents['cate'] = cate

    #最近收藏
    collection = models.Collection.objects.all().order_by('id')[:6]
    contents['collections'] = collection

    #友情链接
    contents['link'] = models.FriendsLink.objects.filter(link_status=1).order_by('link_sort')[:9]

    #相册展示
    contents['photos'] = models.Photos.objects.all()[:9]

    return render(request, 'blog/index.html', contents)

def about(request):
    contents = {}
    for val in models.Config.objects.filter(type='about'):
        contents[val.name] = val

    contents['cate'] = models.Cate.objects.all()

    # 友情链接
    contents['link'] = models.FriendsLink.objects.filter(link_status=1).order_by('link_sort')[:9]

    # 最近收藏
    collection = models.Collection.objects.all().order_by('id')[:6]
    contents['collections'] = collection

    #文献列表
    documents = models.Document.objects.all().order_by('-id')[:8]
    contents['documents'] = documents

    # 相册展示
    contents['photos'] = models.Photos.objects.all()[:9]

    return render(request, 'blog/about.html', contents)

def list(request):
    contents = {}
    page = request.GET.get('page')
    if page is None:
        page = 1

    cid = request.GET.get('cid')
    # 文章列表
    if cid is not None:
        article_list = models.Article.objects.filter(cate_id=cid)
    else:
        article_list = models.Article.objects.filter().all()

    paginator = Paginator(article_list,5)
    try:
        contents['article_list'] = paginator.page(page)
    except PageNotAnInteger:
        contents['article_list'] = paginator.page(1)
    except EmptyPage:
        contents['article_list'] = paginator.page(paginator.num_pages)

    contents['page'] = page
    contents['cid'] = cid

    # 分类列表
    cate = models.Cate.objects.all()
    contents['cate'] = cate

    # 最近收藏
    collection = models.Collection.objects.all().order_by('id')[:6]
    contents['collections'] = collection

    # 文献列表
    documents = models.Document.objects.all().order_by('-id')[:8]
    contents['documents'] = documents

    # 友情链接
    contents['link'] = models.FriendsLink.objects.filter(link_status=1).order_by('link_sort')[:9]

    # 相册展示
    contents['photos'] = models.Photos.objects.all()[:9]

    return render(request, 'blog/list.html', contents)

def article(request):
    aid = request.GET.get('aid')
    if aid is None:
        aid = 1
    contents = {}
    article = models.Article.objects.get(id=aid)
    contents['article'] = article
    contents['cate'] = models.Cate.objects.all()

    #相关文章
    rela_article_list = models.Article.objects.filter(cate_id=article.cate_id)[:6]
    contents['rela_article_list'] = rela_article_list

    # 文献列表
    documents = models.Document.objects.all().order_by('-id')[:8]
    contents['documents'] = documents

    # 友情链接
    contents['link'] = models.FriendsLink.objects.filter(link_status=1).order_by('link_sort')[:9]

    # 相册展示
    contents['photos'] = models.Photos.objects.all()[:9]

    return render(request, 'blog/article.html',contents)

def contact(request):
    contents = {}

    # 基本配置内容
    for val in models.Config.objects.all():
        contents[val.name] = val

    # 分类列表
    cate = models.Cate.objects.all()
    contents['cate'] = cate

    # 友情链接
    contents['link'] = models.FriendsLink.objects.filter(link_status=1).order_by('link_sort')[:9]

    # 相册展示
    contents['photos'] = models.Photos.objects.all()[:9]

    return render(request, 'blog/contact.html',contents)

#ajax获取联系地址
def ajaxPost(request):

    if request.POST.get('action') == 'getAddress':
        contents = {}
        # 基本配置内容
        for val in models.Config.objects.all():
            contents[val.name] = val.value

        return HttpResponse(simplejson.dumps(contents))
    else:
        return HttpResponse(simplejson.dumps({'code':0,'msg':'argument submit error'}))

def other(request):
    pass