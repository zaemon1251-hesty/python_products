from django.db import models
from datetime import datetime

# Create your models here.



class Category(models.Model):   
    class Meta:
       #テーブル名
       db_table ="category"
       verbose_name ="カテゴリ"         #追加
       verbose_name_plural ="カテゴリ"

    #カラム名の定義
    category_name = models.CharField(max_length=255,unique=True)

    def __str__(self):
       return self.category_name



#カテゴリごとに件数を集計する
class Manager(models.Manager):
    def sum_by_category(self):

        result = self.values_list("category").annotate(count=models.Count("category"))

        return dict(result)




class Kakeibo(models.Model):
    objects = Manager()

    class Meta:
       #テーブル名
       db_table ="kakeibo"
       verbose_name ="家計簿"         #追加
       verbose_name_plural ="家計簿"

    #カラムの定義
    date = models.DateField(verbose_name="日付",default=datetime.now)
    category = models.ForeignKey(Category, on_delete = models.PROTECT, verbose_name="カテゴリ")
    money = models.IntegerField(verbose_name="金額", help_text="単位は日本円")
    memo = models.CharField(verbose_name="メモ", max_length=500)

    def __str__(self):
        return self.memo

