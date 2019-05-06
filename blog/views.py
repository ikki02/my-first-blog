from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Image
from .forms import PostForm, ImageForm
import io
import re
import MeCab
from collections import Counter
import matplotlib.pyplot as plt

# Create your views here.
def paginate_query(request, queryset, count):
    paginator = Paginator(queryset, count)  # countは表示するコンテンツの数
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page_obj = paginate_query(request, posts, 3)
    return render(request, 'blog/post_list.html', {'page_obj':page_obj})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_text = re.sub('\r|\r\n|\n', '', post.text)

    # 使われている語彙の頻度分布作成
    morpheme_list = []
    m = MeCab.Tagger('-Ochasen')
    parsed_elements = m.parse(post_text)
    elements = [elements.split() for elements in parsed_elements.splitlines()]
    del elements[-1] # 文末のEOSを削除する。
    for element in elements:
        morpheme_list.append(element[2])  # 原形を抽出。表層形はelement[0]。品詞はelement[3]
    cnt_morpheme = Counter(morpheme_list)

    return render(request, 'blog/post_detail.html', {'post': post, 'morpheme': cnt_morpheme})

def post_new(request):
    # if句で最初に訪れた時と、form.postにデータがある時で
    # 挙動が変わるようにしている。
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # commit=Falseで、まだDBにトランザクションをコミットしない。
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# グラフ作成
def setPlt(pk):
    post = get_object_or_404(Post, pk=pk)
    post_text = re.sub('\r|\r\n|\n', '', post.text)

    # 使われている語彙の頻度分布作成
    morpheme_list = []
    m = MeCab.Tagger('-Ochasen')
    parsed_elements = m.parse(post_text)
    elements = [elements.split() for elements in parsed_elements.splitlines()]
    del elements[-1] # 文末のEOSを削除する。
    for element in elements:
        morpheme_list.append(element[2])  # 原形を抽出。表層形はelement[0]。品詞はelement[3]
    cnt_morpheme = Counter(morpheme_list)

    # グラフ描画
    size = 30

    morphemes_for_graph = cnt_morpheme.most_common(size)
    list_zipped = list(zip(*morphemes_for_graph))
    morphemes = list_zipped[0]
    counts = list_zipped[1]
    plt.bar(range(0, len(morphemes)), counts, align='center')
    plt.xticks(range(0, len(morphemes)), morphemes)
    plt.xlim(xmin=-1, xmax=size)
    plt.title('出現頻度上位30語')
    plt.xlabel('出現頻度が高い30語')
    plt.ylabel('出現頻度')
    plt.grid(axis='y')

# svgへの変換
def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def get_svg(request,  pk):
    setPlt(pk)       # create the plot
    svg = pltToSvg() # convert plot to SVG
    plt.cla()        # clean up plt so it can be re-used
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response

def image_new(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = ImageForm()
        obj = Image.objects.all()
    return render(request, 'blog/image_new.html', {'form': form, 'obj':obj})
