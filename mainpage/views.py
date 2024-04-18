from django.shortcuts import render
from .models import *
from django.utils import timezone
from visualization import make_wordcloud_with_title

# Create your views here.
def index(request):
    start_day = request.POST.get('start_day')
    start_time = request.POST.get('start_time')
    end_day = request.POST.get('end_day')
    end_time = request.POST.get('end_time')
    # wordcloud = WordCloud.objects.get() # day-selectd와 time-select 조건에 맞는 워드클라우드 가져오기
    
    context = {
        "start_day" : start_day,
        "start_time" : start_time,
        "end_day" : end_day,
        "end_time" : end_time
        # "wordcloud" : wordcloud,
    }
    return render(request, 'mainpage/index.html', context)


def detail(request):
    # 시간대에 맞는
    # 전처리 후 데이터를 받아와서
    # 막대 그래프나 도넛 그래프로 생성
    # 아래 top 5 키워드
    bar_graph = ""
    donut_graph = ""
    top_5 = ""

    context = {
        "bar_graph" : bar_graph,
        "donut_graph" : donut_graph,
        "top_5" : ["연예인","정치","황사","에어컨","데브코스"],
    }
    return render(request, 'mainpage/detail.html', context)