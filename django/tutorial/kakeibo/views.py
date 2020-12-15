from django.shortcuts import render
from . forms import KakeiboForm  #forms.pyからKakeiboFormをインポート
from django.urls import reverse_lazy
# Create your views here.
from django.db import models
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Category, Kakeibo


#一覧表示用のDjango標準ビュー(ListView)を承継して一覧表示用のクラスを定義
class KakeiboListView(ListView):
   #利用するモデルを指定
   model = Kakeibo
   #データを渡すテンプレートファイルを指定
   template_name = 'kakeibo/kakeibo_list.html'

   #家計簿テーブルの全データを取得するメソッドを定義
   def queryset(self):
       return Kakeibo.objects.all()

#Create用のclass
class KakeiboCreateView(CreateView):

    #利用するモデルを指定
    model = Kakeibo
    #利用するフォームクラス名を指定
    form_class = KakeiboForm
    #登録処理が正常終了した場合の遷移先を指定
    success_url = reverse_lazy('kakeibo:create_done')

def create_done(request):
   #登録処理が正常終了した場合に呼ばれるテンプレートを指定
   return render(request, 'kakeibo/create_done.html')


#Update用のclass
class KakeiboUpdateView(UpdateView):
   #利用するモデルを指定
   model = Kakeibo
   #利用するフォームクラス名を指定
   form_class = KakeiboForm
   #登録処理が正常終了した場合の遷移先を指定
   success_url = reverse_lazy('kakeibo:update_done')

def update_done(request):
    #更新処理が正常終了した場合に呼ばれるテンプレートを指定
    return render(request, 'kakeibo/update_done.html')


#Delete用のclass
class KakeiboDeleteView(DeleteView):

    #利用するモデルを指定
    model = Kakeibo
    #削除処理が正常終了した場合の遷移先を指定
    success_url = reverse_lazy('kakeibo:delete_done')

def delete_done(request):

    return render(request, 'kakeibo/delete_done.html')

#円グラフ
def show_circle_graph(request):

    #全データ取得
    total=Kakeibo.objects.aggregate(sum=models.Sum('money'))['sum']

    #カテゴリ毎の合計金額を求める
    #まずはカテゴリ名のリストデータを生成する。
    category_list =[]
    #全カテゴリ名をテーブルから取得する。
    category_data = Category.objects.all()
    #ループ処理でカテゴリ名のリストを作成する。
    for item in category_data:
        category_list.append(item.category_name)

    
    category_dict = {}   #カテゴリ毎の割合を格納する辞書型を定義
    for i,item in enumerate(category_list):
        category_total = Kakeibo.objects.filter(category__category_name=category_list[i])\
        .aggregate(sum=models.Sum('money'))
        
        #ここからが割合を求める部分
        if category_total['sum']!=None:
            ratio = int((category_total['sum'] / total) *100)
            category_dict[item] = ratio
        else:
            ratio = 0
            category_dict[item] = ratio

    return render(request, 'kakeibo/kakeibo_circle.html',{'category_dict': category_dict,} )