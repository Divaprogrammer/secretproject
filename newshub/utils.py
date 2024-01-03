# from .serializers import NewsSerializer
import pandas as pd
from newscollector.documents import NewsDocument
from elasticsearch_dsl import Search
from django.db.models import F, Value, CharField,Count
from .models import Comments,Reactions
import random

def insert_to_db(data):
    try:
        for each in data:
            NewsDocument(**each).save()
        msg = 'Data Inserted'
    except Exception as e:
        msg = str(e)

    return msg


def get_comments_count(news_ids):
    return Comments.objects.filter(
                                    is_delete=False,
                                    news_id__in=news_ids
                                ).values(
                                    'news_id'
                                ).annotate(
                                    cmnt_count = Count('id')
                                ).order_by(
                                    'news_id'
                                ).values(
                                    'news_id',
                                    'cmnt_count'
                                )
    
    
def get_reaction_count(news_ids):
    return Reactions.objects.filter(
                                    is_delete=False,
                                    news_id__in=news_ids
                                ).values(
                                    'news_id'
                                ).annotate(
                                    reaction_count = Count('id')
                                ).order_by(
                                    'news_id'
                                ).values(
                                    'news_id',
                                    'reaction_count'
                                )
def get_user_reaction(news_ids, user_id):
    return Reactions.objects.filter(
        is_delete=False,
        news_id__in=news_ids,
        user_id=user_id
    ).values(
        'news_id',
        'reaction_type'
    )



def get_categorised_data(category):
    search = Search(using='default', index='news')
    search = search.query('match', category=category)
    search = search.sort('-publishedAt')
    search = search[:15]
    response = search.execute()
    return response


def custom_pagination(search, page, page_size):
    try:
        total_count = search.count()
        if page_size < total_count:
            start_index = (page - 1) * page_size
            search = search.extra(size=page_size, from_=start_index)
        response = search.execute()
    except Exception as e:
        response = str(e)
        total_count = 0
    return response,total_count


def get_reaction_cmnt_count_and_user_reaction(news_ids,user_id=None):
    try:
        reaction = get_reaction_count(news_ids)
        cmnt = get_comments_count(news_ids)
        if user_id:
            user_reaction = get_user_reaction(news_ids,user_id)

        reaction_df = pd.DataFrame(reaction) if reaction.exists() else pd.DataFrame(columns=['news_id','reaction_count'])
        cmnt_df = pd.DataFrame(cmnt) if cmnt.exists() else pd.DataFrame(columns=['news_id','cmnt_count'])
        merged_df = pd.merge(reaction_df, cmnt_df, on='news_id', how='outer')
        if user_id:
            user_reaction_df = pd.DataFrame(user_reaction) if user_reaction.exists() else pd.DataFrame(columns=['news_id','user_reaction'])
            merged_df = pd.merge(merged_df, user_reaction_df, on='news_id', how='left')
    except:
        merged_df = pd.DataFrame()
    return merged_df


    



def get_display_data(page,page_size,search,user_id=None):
    try:
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
            
            count_df = get_reaction_cmnt_count_and_user_reaction(df.news_id.to_list(),user_id)
            merged_df = pd.merge(df, count_df, on='news_id', how='left')
            merged_df[['reaction_count','cmnt_count']] = merged_df[['reaction_count','cmnt_count']].fillna(0)

            merged_df=merged_df.astype({'reaction_count':int,'cmnt_count':int})
            merged_df.fillna('NoData',inplace=True)
            data = merged_df.to_dict('records')
            return {'count':count,'data':data}
        else :
            return {'count':0,'data':[]}
    except :
        return {'count':0,'data':[]}
