from django.test import TestCase as DjangoTest

# Create your tests here.

import unittest
from django.utils import timezone
from .models import Kakeibo, Category, Manager
from .forms import KakeiboForm


class ManagerTest(DjangoTest):
    #tmp = Kakeibo.objects.all()
    #Kakeibo.objects.all().delete()


    def setUp(self):
        fdate = timezone.now()
        Category.objects.bulk_create([
            Category(category_name="食費"),
            Category(category_name="交通費"),
            Category(category_name="雑費")
        ])
        meal = Category.objects.get(category_name="食費")
        trans = Category.objects.get(category_name="交通費")
        Kakeibo.objects.bulk_create([
            Kakeibo(date=fdate, category=meal, money=2450, memo="etc"),
            Kakeibo(date=fdate, category=trans, money=1250, memo="etc")
        ])

    def test_sum_by_category(self):
        result = Kakeibo.objects.sum_by_category()
        self.assertEqual(result, {1:1, 2:1})
    