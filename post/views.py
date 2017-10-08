from math import ceil
from pickle import dumps, loads

from django.shortcuts import render, redirect

from post.models import Article, Comment
from post.helper import log_client_ip, counter
from post.helper import redis


def home(request):
    page = int(request.GET.get('page', 1)) - 1
    articles = Article.objects.all()[page * 5: (page+1) * 5]
    pages = ceil(Article.objects.all().count() / 5)

    return render(request, 'home.html',
                  {'articles': articles,
                   'pages': range(1, pages + 1)})


@log_client_ip
@counter
def detail(request):
    aid = int(request.GET.get('aid'))

    key = 'ARTICLE-%s' % aid
    print('get from redis')
    article = redis.get(key)
    if article is None:
        print('get from db')
        article = Article.objects.get(id=aid)
        print('set to redis')
        redis.set(key, dumps(article, 4))
    else:
        print('loads bin string')
        article = loads(article)

    comments = Comment.objects.filter(aid=aid)
    return render(request, 'detail.html',
                  {'article': article, 'comments': comments})


def edit(request):
    if request.method == "GET":
        aid = int(request.GET.get('aid'))
        article = Article.objects.get(id=aid)
        return render(request, 'edit.html', {"article": article})
    else:
        aid = int(request.POST.get('aid'))
        content = request.POST.get('content')
        article = Article.objects.get(id=aid)
        article.content = content
        article.save()
        return redirect('/post/detail/?aid=%s' % aid)


def delete(request):
    aid = int(request.GET.get('aid'))
    article = Article.objects.get(id=aid)
    article.delete()
    return redirect('/post/home/')


def search(request):
    keyword = request.POST.get('keyword')
    articles = Article.objects.filter(title__icontains=keyword)

    return render(request, 'home.html', {'articles': articles})


def comment(request):
    aid = int(request.POST.get('aid'))
    name = request.POST.get('name')
    comment = request.POST.get('comment')

    Comment.objects.create(aid=aid, name=name, content=comment)
    return redirect('/post/detail/?aid=%s' % aid)


def blockers(request):
    return render(request, 'blockers.html')
