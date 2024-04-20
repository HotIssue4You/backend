import base64

from django.shortcuts import render
from .models import *
from django.utils import timezone

from visualization import make_wordcloud_with_title, generate_graph_from, make_barplot_with_frequency_of_noun_title, make_donutchart_with_ratio_of_noun_title

# Create your views here.
def index(request):
    if request.method == 'GET':
        cloud_png = make_wordcloud_with_title(
            input_before_datetime="2024-04-18 07:00",
            input_after_datetime="2024-04-18 07:30",
        )
        wordcloud = generate_graph_from(cloud_png)
        context = {
            "wordcloud" : wordcloud,
            "display" : "none",
        }
        return render(request,'mainpage/index.html', context)

    elif request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')
        # wordcloud = WordCloud.objects.get() # day-selectd와 time-select 조건에 맞는 워드클라우드 가져오기
        cloud_png = make_wordcloud_with_title(
            input_before_datetime=start,
            input_after_datetime=end
        )
        wordcloud = generate_graph_from(cloud_png)
        context = {
            "start" : start,
            "end" : end,
            "wordcloud" : wordcloud,
            "display" : "block"
        }
        return render(request, 'mainpage/index.html', context)


def detail(request, start, end):
    # 시간대에 맞는
    # 전처리 후 데이터를 받아와서
    # 막대 그래프나 도넛 그래프로 생성
    # 아래 top 5 키워드
    bar_graph = ""
    donut_graph = ""
    top_5 = ""

    bar_png = make_barplot_with_frequency_of_noun_title(
        input_before_datetime=start,
        input_after_datetime=end
    )
    bar_graph = generate_graph_from(bar_png)

    donut_png, top_5 = make_donutchart_with_ratio_of_noun_title(
        input_before_datetime=start,
        input_after_datetime=end
    )
    donut_graph = generate_graph_from(donut_png)
    context = {
        "bar_graph" : bar_graph,
        "donut_graph" : donut_graph,
         "top_5" : top_5,
    }
    return render(request, 'mainpage/detail.html', context)