# from .serializers import NewsSerializer
import pandas as pd
from .documents import NewsDocument
from elasticsearch_dsl import Search
# from newshub.views import get_reaction_count,get_comments_count

def insert_to_db(data):
    try:
        for each in data:
            NewsDocument(**each).save()
        msg = 'Data Inserted'
    except Exception as e:
        msg = str(e)

    return msg



# def get_categorised_data(category):
#     search = Search(using='default', index='news')
#     search = search.query('match', category=category)
#     search = search.sort('-publishedAt')
#     search = search[:15]
#     response = search.execute()
#     return response


# def custom_pagination(search, page, page_size):
#     try:
#         total_count = search.count()
#         start_index = (page - 1) * page_size
#         search = search.extra(size=page_size, from_=start_index)
#         response = search.execute()
#     except Exception as e:
#         response = str(e)
#         total_count = 0
#     return response,total_count


# def get_reaction_cmnt_count(news_ids):
#     try:
#         reaction = get_reaction_count(news_ids)
#         cmnt = get_comments_count(news_ids)

#         reaction_df = pd.DataFrame(reaction) if reaction.exists() else pd.DataFrame(columns=['news_id','reaction_count'])
#         cmnt_df = pd.DataFrame(cmnt) if cmnt.exists() else pd.DataFrame(columns=['news_id','cmnt_count'])
#         merged_df = pd.merge(reaction_df, cmnt_df, on='news_id', how='outer')
#     except:
#         merged_df = pd.DataFrame()
#     return merged_df
    

# def get_display_data(page,page_size,search):
#     response,count = custom_pagination(search,page,page_size)
#     final_res = list(response.to_dict()['hits']['hits'])

#     df = pd.DataFrame(final_res)
#     df.rename(columns={'_id': 'news_id'}, inplace=True)
#     # df.rename(columns={'_source': 'source'}, inplace=True)
#     data_df=pd.DataFrame(df['_source'].tolist())
#     df = pd.concat([df, data_df], axis=1)
#     cols = set(df.columns.to_list())
#     unwanted_cols = {'_ignored','_index','_score','sort'}
#     common_cols = unwanted_cols.intersection(cols)
    
#     df.drop(common_cols,axis=1, inplace=True)

#     # Get Reaction and Comment Count on the basis of news_id
#     count_df = get_reaction_cmnt_count(df.news_id.to_list())
#     merged_df = pd.merge(df, count_df, on='news_id', how='left')
#     merged_df[['reaction_count','cmnt_count']] = merged_df[['reaction_count','cmnt_count']].fillna(0)
#     data = merged_df.to_dict('records')
    
#     return {'count':count,'data':data}