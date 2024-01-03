from decouple import config
from newscollector.utils import insert_to_db
import requests
import pandas as pd 
from elasticsearch_dsl import Search
from datetime import datetime,timedelta,date
from news_app.get_env_values import get_secret
import json



categories = json.loads(get_secret('NY_CATEGORY'))


def getdata_nytimes():
    ApiKey = get_secret('NYTIMES_KEY')

    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q={category}&begin_date={begin_date}&api-key={api_key}"
    for category in categories:
        try:
            response = requests.get(url.format(category=category, begin_date = get_begin_date(category), api_key = ApiKey))
            response.raise_for_status()  
            data = response.json()
            if data:
                if 'response' in data.keys():
                    df=manipulate_data(data['response']['docs'],category)
                scrap_data=df.to_dict(orient='records')
                status=insert_to_db(scrap_data)
                print(status)
            else:
                print("Failed to fetch API data.")
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            status = e
    return status

def manipulate_data(data,category):
    df = pd.DataFrame.from_records(data) 
    df['category'] = category
    
    df.rename(columns = {'lead_paragraph':'content', 
                    'headline':'title',
                        'web_url':'source_url',
                        'pub_date':'publishedAt',
                        'byline':'author',
                        'snippet':'description',
                    },
            inplace = True)

    df['title']= df['title'].apply(lambda x: x['print_headline'])
    df['author']= df['author'].apply(lambda x: x['original'])
    df =clean_data(df)
    df.fillna('No Data', inplace=True)
    df=remove_duplicate(df,category)
    df=df[['content', 'title','source_url','publishedAt','author','description','source','category']]
    return df
 


def get_begin_date(category):
    try:
        search = Search(using='default', index='news')
        search = search.query('match', category=category)
        search = search.sort('-publishedAt')
        search = search[:1]
        response = search.execute()
        if len(response) > 0:
            res = response[0].publishedAt
            dt_object = datetime.fromisoformat(res[:-6])
            return f'{dt_object.year}{dt_object.month}{dt_object.day}'
        else :
            return str(date.today()-timedelta(days = 1)).replace('-','')
    except:
        return str(date.today()-timedelta(days = 1)).replace('-','')


def remove_duplicate(df,category):
    try:
        search = Search(using='default', index='news')
        search = search.query('match', category=category)
        search = search.sort('-publishedAt')
        search = search[:1]
        response = search.execute()
        if len(response) > 0:
            res = response[0].publishedAt
            df = df[(df['publishedAt'] > res) & (df['category'] == category)]
    except:
        pass
    return df


def clean_data(df):
    return df.dropna(subset=['title','description'])