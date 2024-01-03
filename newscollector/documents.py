# from django_elasticsearch_dsl import Document, Index
from elasticsearch_dsl import Text, Date,Keyword,Index,Document

from .models import News

if Index('news').exists():
    news_index = Index('news')
else:
    news_index = Index('news')
    news_index.settings(
        number_of_shards=1,
        number_of_replicas=1
    )
    news_index.create()

@news_index.document
class NewsDocument(Document):
    title = Text()
    content = Text()
    source_url = Keyword()
    publishedAt = Date()
    author = Keyword()
    description = Text()
    source = Keyword()
    urlToImage = Keyword()
    category = Keyword()