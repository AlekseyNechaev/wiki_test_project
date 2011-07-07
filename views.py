# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from djTest.articles.models import Article, Tag
from django.shortcuts import redirect, render_to_response
from django.contrib import csrf
from django.template.context import RequestContext

# Все имеющиеся статьи
def get_all_articles(request):    
    template = get_template('article_list.html')
    try:
        articles = Article.objects.all()
        context = Context({'title': 'All articles',
                           'articles': articles
                       })
              
    except Article.DoesNotExist:
        articles = [{'header':'Create you first article, for example about Mooses'}]
        context = Context({'title': 'All articles',
                           'list_empty': True,
                           'first': 'Mooses',
                           'articles': articles
                       })  
    
    html = template.render(context)
    return HttpResponse(html)

# Получение статьи по её заголовку
def get_article(request,article_header):
    template = get_template('article.html')
    try:
        article = Article.objects.get(header=article_header)
        tags = article.tags.all()
        context = Context({'title': 'Article: ' + article.header,
                           'article': 
                                {'header':article.header,
                                 'content':article.content,
                                 'tags':tags
                                }
                       })
    except Article.DoesNotExist:
        context = Context({'title': 'This article does not exists',
                           'article': 
                                {'header':'This article does not exists',
                                 'content': 'U can <a href="edit/">create it</a>' 
                                }
                       })
        
    html = template.render(context)
    return HttpResponse(html)

# Форма для редактирования/добавления статей
def edit_article(request,article_header):
    template = get_template('edit.html')
    try:
        # Статья существует - заполняем форму данными статьи
        article = Article.objects.get(header=article_header)
        tags = article.tags.all()
        context = Context(
                    {'title': 'Edit Article: ' + article.header,
                       'input': 
                            {'header': article.header,
                             'content': article.content,
                             'tags': tags
                             }
                       })
        context.update(csrf(request))
    # Статьи не существует - пустая форма, только с заголовком    
    except Article.DoesNotExist:        
        context = Context({'title': 'Edit Article: ' + article_header,
                           'input': {'header':article_header}
                           })
    html = template.render(context)

    return render_to_response(html,context)

# Добавление/обновление статьи
def add_article_to_db(request,article_header):
    #if 'header' in request.GET and 'content' in request.GET:
    #    header = request.GET['header']
    #    content = request.GET['content']
    #    tags_str = request.GET['tags']
    if request.method=='POST':
        if 'header' in request.POST and 'content' in request.POST:
            header = request.POST['header']
            content = request.POST['content']
            tags_str=request.POST['tags']
        tags_str = tags_str.replace(', ',',')
        tags_names = tags_str.split(',')
        tags = [Tag(tag=tag_name) for tag_name in tags_names]
        if Article.objects.filter(header=article_header):
            article = Article.objects.get(header=article_header)
            article.header = header
            article.content = content
            article.tags.clear()
        else:
            article = Article.objects.create(header=header,content=content)
        for tag in tags:
            try:
                tag = Tag.objects.get(tag=tag.tag)
            except Tag.DoesNotExist:
                tag.save()
            except Tag.MultipleObjectsReturned:
                pass  
            article.tags.add(tag)
        article.save()    
        
        redirect_str = '/wiki/%s/' %header 
    else:
        redirect_str = '/wiki/'
    return redirect(redirect_str) 

# Получение списка статей, содержащих определённый тег
def article_by_tag(request,tag_name):
    template = get_template('article_list.html')
    
    try:
        tag = Tag.objects.get(tag=tag_name)
        articles = tag.article_set.all()
        context = Context({'title': 'Articles by tag',
                           'articles': articles
                       })
    except Tag.DoesNotExist:
        return redirect('/wiki/')
    except Article.DoesNotExist:
        return redirect('/wiki/') 
    html = template.render(context)
    return HttpResponse(html)

def search_form(request):
    return render_to_response('search_form.html')

# Поиск по ключевому слову в заголовках статей
def search(request):
    if 'search_query' in request.GET:
        query = request.GET['search_query']
        articles = Article.objects.filter(header__icontains = query)
        template = get_template('article_list.html')
        context = Context({'title': 'Articles search',
                           'articles': articles
                       })
        html = template.render(context)
        return HttpResponse(html)
    else:
        message = 'You submitted an empty form.'
        return HttpResponse(message)
    
    