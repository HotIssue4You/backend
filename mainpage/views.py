from django.shortcuts import render, get_object_or_404
from .models import *
from django.utils import timezone

# Create your views here.
def index(request):
    
    context = {
        "now" : timezone.localtime().strftime('%Y-%m-%d'), # 현재 시각
        "latest" : WordCloud.objects.last(), # 가장 최근 저장된 것
        "times" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    }
    return render(request, "index.html", context)