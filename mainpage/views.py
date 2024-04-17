from django.shortcuts import render
from .models import *
from django.utils import timezone

# Create your views here.
def index(request):
    day_select = request.GET.get('day_select')
    time_select = request.GET.get('time-select')
    # wordcloud = WordCloud.objects.get() # day_selectd와 time-select 조건에 맞는 워드클라우드 가져오기
    context = {
        "day_select" : day_select,
        "time_select" : time_select,
        # "wordcloud" : wordcloud
        "now_day" : timezone.localtime().strftime('%Y-%m-%d'), # 현재 날짜
        "now_time" : timezone.localtime().hour, # 현재 시각
        "times" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
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