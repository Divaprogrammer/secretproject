from rest_framework.views import APIView
from django.http import HttpResponseRedirect

# from .utils import get_display_data
from django.views import View
from django.contrib import messages

from .task import news_scrapper

class NewsAPIView(APIView):
    def get(self, request, format=None):
        if request.user.is_superuser:
            news_scrapper.delay()
            messages.success(request, 'Scrappint is started')
            return HttpResponseRedirect('/')
        else :
            messages.error(request, 'You dont have permission for this tasks')
            return HttpResponseRedirect(request.path_info)



