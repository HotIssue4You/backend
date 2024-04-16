from django.shortcuts import render, get_object_or_404
from .models import *
from django.utils import timezone

# Create your views here.
def index(request):
    
    context = {
        "now" : timezone.localtime().strftime('%Y-%m-%d'), # 현재 시각
        "hot" : ["연예인","정치","황사","에어컨","데브코스"], # wordcloud의 상위 5개 키워드를 가져오면 될 듯
        "times" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    }
    return render(request, "index.html", context)
