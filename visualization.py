import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, use
use('ps') # matplitlib backend mode, 안하면 쓰레드 충돌 발생
from wordcloud import WordCloud
from collections import Counter
from PIL import Image
import io, base64

from django.utils import timezone
from django.http import Http404, HttpResponseServerError
from django.db.utils import OperationalError
from mainpage.models import Article
from datetime import datetime
import pytz

'''
- 시각화 자료 : wordcloud, barplot, donutchart
- Test Function : change_binary_to_image
'''

'''
- merge_date_with_time
date : 날짜("2024-01-01"), str
time : 시간("15:30"), str

<역할>
입력받은 날짜와 시간을 timezone 형식으로 변경하여 반환

<예외 처리>
1. 올바른 날짜 형식이 아닐 경우 현재 시간을 반환
'''
def merge_date_with_time(date=None, time=None):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.strptime(time, '%H:%M').time()
    except:
        date = datetime.now(pytz.utc).date()
        time = datetime.now(pytz.utc).time()

    return timezone.make_aware(datetime.combine(date, time))

'''
- get_titles_within_thirty_minutes_from_django
<파라미터>
input_after_datetime : 이후 시간
input_before_datetime : 이전 시간
type : 'title' or 'noun_title', 시각화를 위한 열 선택

<역할>
이전 ~ 이후 시간의 'title' or 'noun_title' 열 시리즈를 리스트로 변환해서 반환

<예외 처리>
1. 거의 동일한 시간(3분 이내)이 들어왔을 경우 : 이전 시간 = 이후 시간 - 30분 으로 설정
2. 입력한 시간에 기사가 존재하지 않을 경우 : 404 code 반환
3. 데이터베이스 연결 오류가 발생할 경우 : 500 Code 반환
'''
def get_titles_within_thirty_minutes_from_django(input_after_datetime=None, input_before_datetime=None, type='title'):
    try:
        queryset = Article.objects.filter(created_at__lte=input_after_datetime, created_at__gte=input_before_datetime)
        titles = list(queryset.values_list(type, flat=True))
    except OperationalError as e:
        raise HttpResponseServerError("Database connection error: {}".format(e))
    
    if len(titles) == 0:
        raise Http404("No articles found within the last 30 minutes.")
    
    return titles

'''
- parse_titles
<파라미터>
titles : 'title' or 'noun_title' 리스트
(get_titles_within_thirty_minutes_from_django을 거친 데이터)

<역할>
제목 단위를 단어 단위로 쪼개 리스트로 반환
'''
def parse_titles(titles):
    return ' '.join(title for title in titles).split()

'''
- generate_binary
<역할>
현재 생성한 그래프를 바이너리로 변환하여 반환
(모든 그래프에 들어가서 함수로 만듦)

<예외 처리>
1. 이미지 저장-읽기 과정에서 오류가 발생할 경우 : 500 Code 반환
'''
def generate_binary():
    try:
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_binary = buf.read()
        plt.close()
        buf.close()
        return img_binary
    except OSError as e:
        raise HttpResponseServerError("Error while saving image: {}".format(e))

'''
- make_binary_wordcloud_with_titles
<파라미터>
input_after_datetime : 이후 시간
input_before_datetime : 이전 시간

<역할>
이전 ~ 이후 시간의 'title' 데이터를 활용한 워드 클라우드 바이너리 반환
'''
def make_wordcloud_with_title(input_after_datetime=None, input_before_datetime=None):
    titles_list = get_titles_within_thirty_minutes_from_django(
        input_before_datetime=input_before_datetime,
        input_after_datetime=input_after_datetime,
        type='title'
    )
    titles = parse_titles(titles_list)
    noun_counter = Counter(titles)
    top_nouns = dict(noun_counter.most_common(100))

    font_path = "./mainpage/static/fonts/GodoM.ttf"
    wordcloud = WordCloud(width=800, height=400,
                        background_color='white',
                        font_path=font_path,
                        colormap = 'PuBu').generate_from_frequencies(top_nouns)

    plt.figure(figsize=(10, 5)) 
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()

    return generate_binary()

'''
- make_barplot_with_noun_frequency
<파라미터>
input_after_datetime : 이후 시간
input_before_datetime : 이전 시간

<역할>
이전 ~ 이후 시간의 'noun_title' 데이터를 활용한 빈도수 막대 그래프 바이너리 반환
'''
def make_barplot_with_frequency_of_noun_title(input_after_datetime=None, input_before_datetime=None):
    noun_titles_list = get_titles_within_thirty_minutes_from_django(
        input_before_datetime=input_before_datetime,
        input_after_datetime=input_after_datetime,
        type='noun_title'
    )
    noun_titles = parse_titles(noun_titles_list)
    noun_counter = Counter(noun_titles)
    top_nouns = dict(noun_counter.most_common(10))

    sns.set_style('whitegrid')
    font_path ="./mainpage/static/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)

    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x=list(top_nouns.keys()), y=list(top_nouns.values()),
                     palette='Blues_r', legend=False, hue=list(top_nouns.keys()))
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=11, color='black', xytext=(0, 5),
                    textcoords='offset points')

    plt.xlabel('단어', fontsize=14)
    plt.ylabel('빈도수', fontsize=14)
    plt.title('단어별 뉴스 제목 빈도 분석', fontsize=18, fontweight='bold')
    plt.xticks(fontsize=12, rotation=30)
    plt.yticks(fontsize=12)
    plt.ylim(0, max(top_nouns.values()) * 1.2)
    plt.tight_layout()

    return generate_binary()

'''
- make_donutchart_with_noun_ratio
<파라미터>
input_after_datetime : 이후 시간
input_before_datetime : 이전 시간

<역할>
이전 ~ 이후 시간의 'noun_title' 데이터를 활용한 비율 도넛 차트 바이너리 반환

<예외 처리>
1. 단어 개수가 10개 미만인 경우 : 단어 전체로 그래프 생성
'''
def make_donutchart_with_ratio_of_noun_title(input_after_datetime=None, input_before_datetime=None):
    noun_titles_list = get_titles_within_thirty_minutes_from_django(
        input_before_datetime=input_before_datetime,
        input_after_datetime=input_after_datetime,
        type='noun_title'
    )
    noun_titles = parse_titles(noun_titles_list)
    noun_counter = Counter(noun_titles)
    top_nouns = dict(noun_counter.most_common(len(noun_counter)))

    sns.set_style('whitegrid')
    font_path ="./mainpage/static/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)

    data = list(top_nouns.values())
    labels = list(top_nouns.keys())

    plt.figure(figsize=(6, 5))
    if len(data) < 10:
        plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90,
                labeldistance=1.035, colors=sns.color_palette("Blues"))
    else:
        plt.pie(data[:10], labels=labels[:10], autopct='%1.1f%%', startangle=90,
                labeldistance=1.035, colors=sns.color_palette("Blues"))

    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    plt.gca().add_artist(centre_circle)
    plt.title('단어별 뉴스 제목 비율 분석', fontsize=18, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()

    total_count = sum(data)
    top_five_noun_and_ratio = {word: round(count/total_count * 100, 2) for word, count in zip(labels[:5], data[:5])}

    return generate_binary(), top_five_noun_and_ratio

def generate_graph_from(png):
    """
    generate_binary()로부터 생성된 plot 이미지의 이진 8비트 데이터를 ASCII 7비트 이진 코드로 변환 후,
    유니코드 문자열로 변환하여 반환 -> 이미지 소스로 이용
    :param png: matplotlib.pyplot binary data
    :return:
    """
    graph = base64.b64encode(png)
    return graph.decode('utf-8')

'''
- change_binary_to_image
<역할>
바이너리 -> 이미지 변환 테스트를 위한 함수

<사용 예시>
a = make_barplot_with_noun_frequency(date, time)
change_binary_to_image(a)
'''
def change_binary_to_image(binary_data, *args):
    image = Image.open(io.BytesIO(binary_data))
    image.show()