from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from django.db.models import F
from elasticsearch_dsl import Q,Search
import pandas as pd



from .models import Comments,Reactions

from decouple import config
from news_app.get_env_values import get_secret
from newscollector.documents import NewsDocument
from .utils import (get_display_data,
                    custom_pagination)


connection = get_secret('CONNECTION')
index = get_secret("INDEX")


class CategoryPage(View):
    def get(self,request,*args, **kwargs):
        category = request.GET.get('category')
        page = int(request.GET.get('page',1))
        page_size = 16
        return_type = request.GET.get('type','')
        user_id=None
        if request.user.is_authenticated:
            user_id = request.user.id
        search = Search(using=connection, index=index)
        if category:
            if category == 'All':
                search = search.sort('-publishedAt')
            else:
                search = search.query('match', category=category) 
        if search:
            outcome=get_display_data(page,page_size,search,user_id)
            total_page = (int(outcome['count'])/16)+1
            if return_type == 'json':
                return JsonResponse(outcome['data'],safe=False)
            return render(request,'category.html',{"count":outcome['count'],'Categorydata':outcome['data'],'Category':category,'total_page':total_page,'page':page})
        return redirect(request.get_full_path())

class LandingPage(View):
    def get(self,request,*args, **kwargs):
        page = request.GET.get('page',1)
        page_size = 16
        user_id=None
        if request.user.is_authenticated:
            user_id = request.user.id
        search = Search(using=connection, index=index)
        search = search.sort('-publishedAt')
        Latestdata=get_display_data(page,page_size,search,user_id)
        search = search.query('match', category='trending')
        Trendingdata=get_display_data(page,page_size,search,user_id)
        return render(request,'index.html',{"count":Latestdata['count'],'Latestdata':Latestdata['data'],'Trendingdata':Trendingdata['data']})

class SearchingPage(View):
    def get(self,request,*args, **kwargs):
        q = request.GET.get('q')
        page = int(request.GET.get('page',1))
        page_size = 16
        return_type = request.GET.get('type','')
        search = Search(using=connection, index=index)
        if q:
            qry =   Q('fuzzy', title={'value': q, 'fuzziness': 'AUTO'} ) | \
                Q('fuzzy', content={'value': q, 'fuzziness': 'AUTO'} ) | \
                Q('fuzzy', description={'value': q, 'fuzziness': 'AUTO'} )
            search = search.query(qry)
        else:
            search = search.sort('-publishedAt')
        response,count = custom_pagination(search,page,page_size)
        final_res = list(response.to_dict()['hits']['hits'])
        if final_res:
            df = pd.DataFrame(final_res)
            df.rename(columns={'_id': 'news_id'}, inplace=True)
            if '_source' in df.columns:
                data_df=pd.DataFrame(df['_source'].tolist())
                df = pd.concat([df, data_df], axis=1)
            cols = set(df.columns.to_list())
            unwanted_cols = {'_ignored','_index','_score','sort'}
            common_cols = unwanted_cols.intersection(cols)
            df.drop(common_cols,axis=1, inplace=True)
            df = df[['news_id','title','description','publishedAt','category']]
            df.fillna('default',inplace=True)
            data = df.to_dict(orient='records')
            if return_type == 'json':
                return JsonResponse(data,safe=False)
        total_page = (int(count)/16)+1
        return render(request,'search.html',{"count":count,'data':data,'query':q,'total_page':total_page,'page':page})

class AllNews(View):
    def get(self,request,*args, **kwargs):
        page = request.GET.get('page',1)
        page_size = 28
        user_id=None
        if request.user.is_authenticated:
            user_id = request.user.id
        search = Search(using=connection, index=index)
        search = search.sort('-publishedAt')
        outcome=get_display_data(page,page_size,search,user_id)
        total_page = int(outcome['count'])/28
        return render(request,'base.html',{"count":outcome['count'],'data':outcome['data'],'category': 'All','total_page':total_page,'page':page})


class GetNewsDetails(View):
    def get(self,request,*args,**kwargs):
        id = request.GET.get('id')
        data = NewsDocument.get(id=id)
        comments_count = Comments.objects.filter(is_delete=False,news_id=id).count()
        reaction_count = Reactions.objects.filter(is_delete=False,news_id=id).count()
        reaction_type = None
        if request.user.is_authenticated:
            user_reaction = Reactions.objects.filter(is_delete=False,news_id=id).values_list('reaction_type', flat=True)
            if user_reaction.exists():
                reaction_type = user_reaction[0]
        res = {
            "title":data.title,
            "content":data.content,
            "publishedAt":data.publishedAt,
            "author":data.author,
            "description":data.description,
            "category":data.category,
            "reaction_count":reaction_count,
            "comments_count":comments_count,
            "news_id":id,
            "reaction_type":reaction_type
        }
        search = Search(using=connection, index=index)
        result = search.query('match', category=data.category)
        sub_data=get_display_data(1,7,result)
        return render(request,'postdetail.html',{'data':res,'sub_data':sub_data['data']})