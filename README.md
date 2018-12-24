
## 目的：Djangogirlsでブログページを作りながら、Djangoの重要な概念を整理する。

---

## 目次
- フレームワークの基礎
- Djangoの利用に際して
- アプリケーションとモデル
- admin
- URLの設定
- view
- template
- QuerySet & ORM
- CSSとStatic files（テンプレートの拡張、リンク先の設定）
- Forms（FormsからDBに登録する、DBを編集する、簡易アクセス権を付与する）

---

## [フレームワークの基礎](https://tutorial.djangogirls.org/en/django/)
- アプリケーションとモデル
Djangoではひとつのプロジェクトは複数のアプリケーションで構成される。以下のコマンドでアプリケーションを作成する。

- URLconf  
ネット上のすべてのページにはURL（Uniform Resource Locator）が設定される。このURLを使って、アプリケーションは何を表示すべきか特定することができる。Djangoでは、URLconf機能を使って、リクエストされたURLとの照合をはかり、正しいviewファイルを特定することができる。

- view  
Webサーバーにリクエストが送られると、Djangoが実際何をリクエストされたか特定しようとする。始めにURLを特定し、次に何をすべきか判明させるのである。この機能はDjangoの**urlリゾルバ**によって実現される。Djangoは上記URLconf機能によって、URLリストの一番上から下まで確認し照合作業を開始する。URLが照合すると、Djangoはリクエストをその関連する関数に渡す作業をviewと呼ぶ。  
 - (e.g.)郵便配達を例にすると、配達員が通りを歩いて一つ一つの家の住所を確認して、手紙の住所と照合作業するのと同じである。照合したら手紙をポストに投函するだろう。
  
- template
テンプレートファイルは特定のフォーマットに従った情報を再利用するための機能である。（例えば、メールを書くときを想像してみよう。宛先や内容は毎回異なるとしても、署名やフォーマットは毎回同じである。）

- CSS
Cascading Style Sheets (CSS) はウェブサイトの見た目やフォーマットを記述する言語である。

- Forms
フォームを使うことで、インターフェイスにボタンをつけたり様々なことができる。Djangoでは、スクラッチでフォームを規定することもできるし、フォームの内容をモデルに登録することでModelFormsと呼ばれるオブジェクトを作ることもできる。

---

## [Djangoの利用に際して](https://tutorial.djangogirls.org/en/installation/)
Djangoに限らず、プロジェクトを作成する際は、プロジェクト毎に仮想環境を準備するのがグッドプラクティス。  
Pythonでの仮想環境の構築手順は以下の通り。

1. まず、プロジェクトフォルダを作成する。
```
$ mkdir djangogirls
$ cd djangogirls
```

1. 次に仮想環境を起動する。
```
$python3 -m venv [myvenv]  #venvは仮想環境用のライブラリ。実行すると[myvenv]フォルダとその直下に設定ファイルが生成される。
$source [myvenv]/bin/activate  #仮想環境を起動する。
```

1. 必要なライブラリをインストールし、環境構築する。  
```
(myvenv) ~$ pip install -U pip
(myvenv) ~$ touch requirements.txt  #pipでインストールするライブラリを記述する。記述例：Django~=2.0.6
(myvenv) ~$ pip install -r requirements.txt  #requirements.txtのライブラリを順にインストールする。
```
gitやtmuxなど汎用ツールは予めシステムに入れてから仮想環境を作った方がよい？グッドプラクティスは分からん。

1. Webに公開（＝デプロイ）するため、[Pythonanywhere](https://www.pythonanywhere.com/user/b1200315/)や[Heroku](https://www.heroku.com)などにも登録しておこう。
1. Djangoのプロジェクトを作成する。[参考URL](https://tutorial.djangogirls.org/en/django_start_project/)  
下記コマンドを実行すると、カレントディレクトリにDjangoスクリプトがたくさんできる。
```
(myvenv) $ django-admin startproject [mysite] .
```
 - ./manage.py: a script that helps with management of the site. With it we will be able to start a web server on our computer without installing anything else.
 - ./mysite/settings.py: it contains the configuration of your website.
 - ./mysite/urls.py: it contains a list of patterns used by urlresolver. It's expected to be changed as follows.
    - LANGUAGE_CODE = 'ja'
    - TIME_ZONE = 'Asia/Tokyo'
    - STATIC_URL = '/static/'  #static fileの設定1
    - STATIC_ROOT = os.path.join(BASE_DIR, 'static')  #static fileの設定2
    - ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']
    - DATABASES = {'default': {~~~}}  #デフォルトではsqlite3が使われる。他のDBを使いたい場合は書換える。

1. ルートディレクトリとDBを設定する。  
```
(myvenv) ~$ python manage.py migrate
```

1. サーバーを起動する。
```
(myvenv) ~/$ python manage.py runserver
```
起動したら、ブラウザに[http://127.0.0.1:8000/](http://127.0.0.1:8000/)をリクエストするとアクセスできる。

---

## アプリケーション
Djangoではひとつのプロジェクトは複数のアプリケーションで構成される。以下のコマンドでアプリケーションを作成する。
```
$ python manage.py startapp blog
```
blog/直下に複数のファイルが生成される。  
  
また、Djangoに作成したアプリケーションを認識させるため、mysite/setting.pyに以下のように追記する。
```
INSTALLED_APPS=['django.hogehoge', 'blog',]
```

## [モデル](https://tutorial.djangogirls.org/en/django_models/)
DBに登録されるオブジェクトのことをモデルという。なお、オブジェクトは以下の特徴を持つ。
- properties: 猫だったら、「色」「猫種」「飼い主」などが考えられる。
- method: 猫だったら、「ひっかく」「寝る」「食べる」などが考えられる。

Webサイトを作るときは、「オブジェクト」と「オブジェクト同士の繋がり」を設計することがポイントになる。  
例えば、ブログを作るときは、「タイトル」「記事」「作者」などの属性があり、「発行」「削除」などのメソッドが考えられるだろう。  

## モデルの登録の仕方
blog/models.pyにクラスを書くようにして、モデルを記述していく。[⇨Django公式モデル定義URL](https://docs.djangoproject.com/en/2.0/ref/models/fields/#field-types)

```
from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):  #models.Model means that the Post is a Django Model, so Django knows that it should be saved in the DB.
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  #models.ForeignKey is a link to another model.
    title = models.CharField(max_length=200)  #models.CharField is how you define text with a limited number of characters.
    text = models.TextField()  #models.TextField is for long text without a limit.
    created_date = models.DateTimeField(default=timezone.now)  #models.DateTimeField is a date and time.
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
```

models.pyにモデルの変更を記述したら、以下のコマンドを叩いてDjangoに変更を知らせる。

```
$ python manage.py makemigrations blog
```

その後、DBにモデルを登録する。

```
$ python manage.py migrate blog
```

---

## [admin](https://tutorial.djangogirls.org/en/django_admin/)
DBを管理するadminを設定する。  
blog/admin.pyにて以下の記述を追記し、作ったPostモデルをadminページで管理できるようにする。
```
from django.contrib import admin
from .models import Post  #カレントのmodels.pyからPostモデルをインポートする。

admin.site.register(Post)
```

その後、以下のコマンドにてsuperuserアカウントを作成する。ユーザー名、Emailアドレス、パスワードを対話的に設定していく。

```
$ python manage.py createsuperuser
```


[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)にブラウザでアクセスし、上記superuserアカウントでログインできる。  
[その他参考：django公式URL](https://docs.djangoproject.com/en/2.0/ref/contrib/admin/)

---

## URLの設定
- mysite/urls.pyのurlpatternsに以下のように記述する。  

```
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```
これでadmin/とブラウザに入力すると、admin.site.urlsに飛ぶ。  

- ホームページを設定したい際は、以下の行を変えるとよい。

1. まず、任意のアプリケーションをリンク先に指定する。

```
from django.urls import path, include  #includeを使うため、インポートする。

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  #'http://127.0.0.1:8000/'のリクエストを全てblog.urlsにリダイレクトする。blog.urlsは以下で記述する。
]
```

2. 次に、任意のアプリケーションでurls.pyを作る。その後、以下のように記述する（例：blog/urls.py）。

```
from django.urls import path
from . import views  #blogアプリケーションのviewsにリダイレクトするため、インポートする。

urlpatterns = [
    path('', views.post_list, name='post_list'),  #views.post_listにリダイレクト（＝ルートURLと同義）。name=でpost_list.htmlを探す。
]
```

---

## [view](https://tutorial.djangogirls.org/en/django_views/)
A view is a place where we put the "logic" of our application. It will request information from the model you created before and pass it to a template: connect models and templates. 

- 任意のアプリケーション直下にviews.pyを置いて、ロジックを記述する。（例：blog/views.py）

```
from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):  #requestを受けてpost_list.htmlを返す。  
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')  #モデルを変数に格納する。  
    return render(request, 'blog/post_list.html', {'posts': posts})  #requestをpost_list.htmlにする。{}では、テンプレートに渡す変数を定義する。  
```

---

## [template](https://tutorial.djangogirls.org/en/html/)
テンプレートファイルは特定のフォーマットに従った情報を再利用するための機能である。（例えば、メールを書くときを想像してみよう。宛先や内容は毎回異なるとしても、署名やフォーマットは毎回同じである。）

DjangoのテンプレートはHTMLで記述される。

テンプレートは**blog/templates/blog**ディレクトリに保存しよう。そして、**post_list.html**というテンプレートファイルを作ろう。  

HTMLで.htmlファイルに記述すれば、それが表示されるようになる。

- To print a variable in Django templates, we use double curly brackets with the variable's name inside, like this:`{{ posts }}`

- また、viewの変数はリストで渡されるため、for文を書く要領で独特のかき回しをする必要がある。
```
{% for post in posts %}
    {{ post }}
{% endfor %}
```

- 「変数の属性」に繰り返しアクセスしたい際は、{% for %}と{% endfor %}の間に以下のように記述する。

```
{% for post in posts %}
    <div>
        <p>published: {{ post.published_date }}</p>
        <h2><a href="">{{ post.title }}</a></h2>
        <p>{{ post.text|linebreaksbr }}</p>  #|linebreaksbrはposts' textを段落に加工するプログラム
    </div>
{% endfor %}
```

---

## [QuerySet](https://tutorial.djangogirls.org/en/django_orm/)
A QuerySet is, in essence, a list of objects of a given Model. QuerySets allow you to read the data from the database, filter it and order it.

```
(myvenv) ~/djangogirls$ python manage.py shell

>>> from blog.models import Post
>>> Post.objects.all()  #Postモデルのオブジェクトを全て表示する。
>>> Post.objects.create(author=me, title='Sample title', text='Test')  #Postモデルに新規登録する。

>>> Post.objects.filter(title__contains='title')  #フィルタをかける。

>>> post = Post.objects.get(title="Sample title")  #publish()するための書き方。
>>> post.publish()  #publish()するための書き方。

>>> Post.objects.order_by('created_date')  #並び替える書き方。
>>> Post.objects.order_by('-created_date')  #逆順に並び替える書き方。

# SQL文はchainすることもできる。
>>> Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

```

[参考：公式URL](https://docs.djangoproject.com/en/2.0/ref/models/querysets/)



---

## [CSS](https://tutorial.djangogirls.org/en/css/)
Cascading Style Sheets (CSS) はウェブサイトの見た目やフォーマットを記述する言語である。
CSSのフォーマットは[Bootstrap](https://getbootstrap.com)がよく参照されるとのこと。

Bootstrapをインストールするには、テンプレートの**blog/templates/blog/post_list.html**の先頭に以下の2行を追記する。
```
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
```

## Static files
Static files are all your CSS and images. Django will automatically find any folders called "static" inside any of your apps' folders. Then it will be able to use their contents as static files.

CSSファイルはstaticディレクトリの下のcssディレクトリ下に作る。（例：**blog/static/css/blog.css**）  
CSSファイルを書くときは、[HTML Color Name](https://www.w3schools.com/colors/colors_names.asp)などを参照しながら、フォントを設定していく。  
- class: HTMLの複数のelementをグルーピングする。class="external_link"など。
- id: HTMLにおける特定のelementを指し示す。id="link_to_wiki_page"など。  

CSSファイルの細かい書き方は「CSSのリンク」を参考にするとよい。

- We also need to tell our HTML template that we added some CSS. Open the **blog/templates/blog/post_list.html** file in the code editor and add this line at the very beginning of it:`{% load static %}`

We're just loading static files here. 
Between the <head> and </head> tags, after the links to the Bootstrap CSS files, add this line:

`<link rel="stylesheet" href="{% static 'css/blog.css' %}">`

The browser reads the files in the order they're given, so we need to make sure this is in the right place. Otherwise the code in our file may be overriden by code in Bootstrap files. We just told our template where our CSS file is located.

Your template file should now look like this:
```
{% load static %}
<html>
    <head>
        <title>Django Girls blog</title>
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="{% static 'css/blog.css' %}">
    </head>
```
- つまり、全体に適用させたいフォントは.cssファイルに、個別に適用させたいフォントはテンプレートの.htmlファイルに記述する要領でよい。
- .htmlファイルなどの`<div>`タグにクラス名を与えて識別しやすくすることも可能。例：`<div class="page-header"></div>`

## [Template extending](https://tutorial.djangogirls.org/en/template_extending/)
Webページ内で汎用的にテンプレートを使いまわしたいとき、`base.html`ファイルを用意すればよい。（例：blog/templates/blog/base.html）

1. base.html内でHTMLを別途定義したい際は、以下の記述を記載する。
```
{% block content %}
{% endblock %}
```
1. その後、他のHTMLファイルを`blog/templates/blog/`直下にファイル保存する。
 - base.htmlに拡張することを明記する。
 - 上記2行の間に拡張したい内容を追記する。

```
{% extends 'blog/base.html' %}

{% block content %}
    <div>
    </div>
{% endblock %}
```


## [リンクの設定](https://tutorial.djangogirls.org/en/extend_your_application/)

以下の要領でリンクを記述できる。
1. リンクを貼りたい箇所に以下のようにテンプレートタグを挿入する。
```
<h1><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h1>
```
`{% url 'post_detail' pk=post.pk %}`の説明は以下の通り。
 - The `post_detail` part means that Django will be expecting a URL in **blog/urls.py** with name=post_detail
 - `pk` is short for primary key, which is a unique name for each record in a database. Because we didn't specify a primary key in our Post model, Django creates one for us (by default, a number that increases by one for each record, i.e. 1, 2, 3) and adds it as a field named pk to each of our posts. We access the primary key by writing post.pk, the same way we access other fields (title, author, etc.) in our Post object!
1. blog/urls.pyにURLの変数を追加する。次のようなURL（http://127.0.0.1:8000/post/1/ ）を設定したい場合は以下のように書く。  
`path('post/<int:pk>/', views.post_detail, name='post_detail')`
 - <int:pk>: Djangoが数値型の値を受け取り、pkという変数名でviewに返す。という意味。
1. views.pyにpost_detail用の新しい関数を用意する。こんな感じ。
```
from django.shortcuts import render, get_object_or_404  #`get_object_or_404`はページが存在しない場合のエラーハンドラ
def post_detail(request, pk):  #url.pyからpkを受取り、処理する。
    post = get_object_or_404(Post, pk=pk)  #もしpkの値が不適切な場合、エラーハンドラが走る。
    return render(request, 'blog/post_detail.html', {'post': post})
```
1. post_detail用のテンプレートを作る。

```
{% extends 'blog/base.html' %}

{% block content %}
    <div class="post">
        {% if post.published_date %}  #post.published_dateがあれば処理が走る。
            <div class="date">
                {{ post.published_date }}
            </div>
        {% endif %}
        <h2>{{ post.title }}</h2>
        <p>{{ post.text|linebreaksbr }}</p>
    </div>
{% endblock %}
```

---

## [Forms](https://tutorial.djangogirls.org/en/django_forms/)  
Postモデルの追加と編集をWebページ上でできるようにしよう。  
フォームを使うことで、インターフェイスにボタンをつけたり様々なことができる。Djangoでは、スクラッチでフォームを規定することもできるし、フォームの内容をモデルに登録することでModelFormsと呼ばれるオブジェクトを作ることもできる。
  
1. アプリケーション直下に`forms.py`ファイルを格納する。（例：**blog/forms.py**）  

```
from django import forms
from .models import Post

class PostForm(forms.ModelForm):  #フォーム名

    class Meta:  #we have class Meta, where we tell Django which model should be used to create this form
        model = Post
        fields = ('title', 'text',)
```  
1. 以下のコードを**blog/template/blog/base.html**に追記する。  
`<a href="{% url 'post_new' %}" class="top-menu"><span class="glyphicon glyphicon-plus"></span></a>`  
The class `glyphicon glyphicon-plus` is provided by the bootstrap theme we are using, and will display a plus sign for us.

1. **blog/urls.py**にURLを追加する。  
Once again we will create a link to the page, a URL, a view and a template.
`path('post/new', views.post_new, name='post_new'),`
1. **blog/views.py**に以下を追記する。
```
from .forms import PostForm
def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
```
上記でpost_editページは作れるが、実は、作ったページからDBに値を直接登録はできない。  
そのやり方はもう一つ下のセルをみると良い。

1. **blog/template/blog/post_edit.html**に以下を追記する。

```
{% extends 'blog/base.html' %}

{% block content %}
    <h2>New post</h2>
    <form method="POST" class="post-form">{% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="save btn btn-default">Save</button>
    </form>
{% endblock %}
```

  - We have to display the form. We can do that with `{{ form.as_p }}`.
  - The line above needs to be wrapped with an HTML form tag: `<form method="POST">...</form>`.
  - We need a Save button. We do that with an HTML button: `<button type="submit">Save</button>`.
  - And finally, just after the opening `<form ...>` tag we need to add `{% csrf_token %}`. This is very important, since it makes your forms secure!
  
[Formに関する公式URL](https://docs.djangoproject.com/en/2.0/topics/forms/)

## FormからDBに保存しよう。
- FormにPOSTされた値を反映するように、views.pyにif文を書き加える。

```
from .forms import PostForm
from django.shortcuts import redirect  #他のページに直接飛べるようにするライブラリ

def post_new(request):
    if request.method == "POST":  #All the fields from the form are in `request.POST` once the form has been created. 
        form = PostForm(request.POST)  #To construct the PostForm with data from the form
        if form.is_valid():  #To check if the form is correct (all required fields are set and no incorrect values have been submitted).
            post = form.save(commit=False)  #to save the form.commit option means that we don't wanna save the form yet.
            post.author = request.user
            post.published_date = timezone.now()
            post.save()  #new blog post is saved.
            return redirect('post_detail', pk=post.pk)  #post_detailに直接飛べるようにする。
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

```

## 編集機能を追加しよう
1. テンプレートに以下を追記する。（例：blog/template/blog/post_detail.html）  
`<a class="btn btn-default" href="{% url 'post_edit' pk=post.pk %}"><span class="glyphicon glyphicon-pencil"></span></a>`  
これは鉛筆ボタンを追加して、post_editにリンク先を指定する、という意味である。
1. **blog/urls.py**に以下を追記する。
` path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),`
1. **blog/views.py**にpost_edit関数を記載する。
```
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)  #エラーハンドラ
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  #エラーハンドラのインスタンスをformに渡す書き方。
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)  #エラーハンドラのインスタンスをformに渡す書き方。
    return render(request, 'blog/post_edit.html', {'form': form})
```

## アクセス権毎に表示するページを変える方法
上記のようなフォーム追加や編集が誰にでもできると安全とはいえないため、admin権限のユーザーだけに表示させるようにしたい。  

1. **blog/templates/blog/base.html**を開く。認証をつけたい箇所に{% if %}で処理を追加しよう。

```
{% if user.is_authenticated %}
    <a href="{% url 'post_new' %}" class="top-menu"><span class="glyphicon glyphicon-plus"></span></a>
{% endif %}
```
1. **blog/templates/blog/post_detail.html**を開く。認証をつけたい箇所に{% if %}で処理を追加しよう。

```
{% if user.is_authenticated %}
     <a class="btn btn-default" href="{% url 'post_edit' pk=post.pk %}"><span class="glyphicon glyphicon-pencil"></span></a>
{% endif %}
```

これで完璧な対策というわけではないが、第一歩としては上出来である。

---

## その他参考
Djangoのシェルを起動するには以下コマンドを叩くとSQL文が書けたりする。

```
(myvenv) ~/djangogirls$ python manage.py shell

>>> from blog.models import Post
>>> Post.objects.all()  #Postモデルのオブジェクトを全て表示する。
>>> Post.objects.create(author=me, title='Sample title', text='Test')  #Postモデルに新規登録する。

exit()  #抜ける。
```
