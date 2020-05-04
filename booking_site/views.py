from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, UpdateView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OnlyYouMixin
from django.contrib.auth.models import User

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import math

from selenium import webdriver
from time import sleep

from janome.tokenizer import Tokenizer as Token


def index(request):
    return render(request, "booking_site/index.html")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("booking_site:home")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'booking_site/signup.html', context)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "booking_site/users/detail.html"


class UserUpdateView(OnlyYouMixin, UpdateView):
    model = User
    template_name = "booking_site/users/update.html"
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('booking_site:users_detail', pk=self.kwargs['pk'])


@login_required
def home(request):
    books = Book1.objects.all()
    borrow = Borrow.objects.all()
    borrow_title_id = []
    borrow_user_id = []

    for i in range(len(borrow)):
        borrow_title_id.append(borrow[i].title.id)

    # 自分が借りている本のtitle_idを取得
    own_book = []
    own_borrow_title_id = Borrow.objects.filter(user=request.user.id)

    for i in range(len(own_borrow_title_id)):
        borrow_user_id.append(own_borrow_title_id[i].user_id)
        own_book.append(own_borrow_title_id[i].title_id)

    context = {
        'books': books,
        'borrow_title_id': borrow_title_id,
        'borrow_user_id': borrow_user_id,
        'own_book': own_book,
    }
    return render(request, 'booking_site/home.html', context)


@login_required
def borrow(request, pk):
    data = Book1.objects.get(pk=pk)
    book = Book1.objects.filter(id=pk)

    url = "https://booklog.jp/item/1/" + book[0].no
    rating = scraping(url)
    print(rating)

    if request.method == 'POST':
        form = BorrowForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('booking_site:home')
    else:
        form = BorrowForm(initial={
            'title': data.id,
            'user': request.user,
        })

    return render(request, 'booking_site/borrow.html', {'data': data, 'form': form, 'rating': rating, })


@login_required
def back(request, pk):
    data = Book1.objects.get(pk=pk)
    if Borrow.objects.filter(title=data.id).exists():
        Borrow.objects.filter(title=data.id).delete()

    return redirect('booking_site:home')


class BookDetailView(DetailView):
    model = Borrow
    template_name = "booking_site/detail.html"


def borrwDtail(request, pk):
    borrow = Borrow.objects.filter(title_id=pk)
    book = Book1.objects.filter(id=pk)
    user = User.objects.filter(id=borrow[0].user_id)
    # print(borrow[0].user_id)
    # print(book[0].title)
    # print(user[0].username)


    # reviews = scraping()
    # print(len(reviews))
    url = "https://booklog.jp/item/1/" + book[0].no
    rating = scraping(url)
    # print(rating)

    context = {
        'book': book,
        'borrow': borrow,
        'user': user,
        'rating': rating,
    }
    return render(request, 'booking_site/detail.html', context)


def scraping(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    rating_value = soup.find(class_="rating-value")
    rating_value = rating_value.text[:4]

    rating_stars = soup.find(class_="rating")
    rating_stars = rating_stars.find_all('img')
    stars = []
    for rating_star in rating_stars:
        if rating_star['src'] == "/img/star/star.png":
            stars.append(1)
        else:
            stars.append(0)

    # count = soup.find_all(class_="reviews")
    # count = count[0].span.get_text()
    # pages = math.ceil(int(count) / 10)

    data = {
        "rating_value": rating_value,
        "rating_stars": stars,
        # "review_count": count,
    }

    return data
'''
    reviews = []
    for p in range(0, pages):
        page = p + 1
    #     print(page)
        sufix = "?page=" + str(page) + "&perpage=10&rating=0&is_read_more=1&sort=1"
        search_url = url + sufix

        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('p', class_="review-txt")

        for d in data:
            tmp = d.get_text()
            tmp = tmp.replace(" ", "")
            tmp = tmp.replace("\n", "")
            tmp = tmp.replace("\r", "")
            tmp = tmp.replace("<br/>", "")
            tmp = tmp.replace("\u3000", "")
            reviews.append(tmp)

        sleep(1)

    t = Token()
    wakati = []
    tmp1 = []
    tmp2 = []

    for line in reviews:
        for token in t.tokenize(line):
            tmp1.append(token.surface)
            tmp2 = " ".join(tmp1)
        wakati.append(tmp2)
        tmp1 = []
    wakati = " ".join(wakati)

    parser = PlaintextParser.from_string(
        "".join(wakati), Tokenizer("japanese"))

    from sumy.summarizers.lex_rank import LexRankSummarizer
    #Lex-Rank
    LexRankSummarizer = LexRankSummarizer()
    LexRankSummarizer.stop_words = [" "]
    summary = LexRankSummarizer(document=parser.document, sentences_count=3)

    return summary
'''
