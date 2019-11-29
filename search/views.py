from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SearchForm, IndexForm
from .models import *
from django.views import View
import re
# Create your views here.


def addToIndex(itemset, doc_id):
    doc_id = str(doc_id)
    for token in itemset.keys():
        try:
            temp = dict()
            value = InvertedIndex.objects.get(word=token).list
            print(value)
            temp = value
            temp[doc_id] = str(itemset[token])
            InvertedIndex.objects.get(word=token).delete()
            InvertedIndex.objects.create(word=token, list=temp)
        except:
            frequency = str(itemset[token])
            InvertedIndex.objects.create(word=token, list={doc_id: frequency})


def addToDocuments(doc):
    d = Documents()
    d.document = doc
    d.save()
    return Documents.objects.latest('id').id

def cleandoc(doc):
    doc = doc.lower()
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    new_doc = ""
    for char in doc:
        if char not in punctuations:
            new_doc = new_doc + char
    return new_doc


def tokenize(doc):
    doc = cleandoc(doc)
    doc_id = addToDocuments(doc)
    tokens = re.split(' |\r\n+', doc)
    itemset = dict()
    for token in tokens:
        if token not in itemset.keys():
            itemset[token] = 1
        else:
            itemset[token] += 1
    addToIndex(itemset, doc_id)


def textToDocuments(text):
    docs = list()
    docs = re.split('\r\n\r\n+', text)
    for doc in docs:
        tokenize(doc)


class IndexView(View):

    def get(self, request):
        form = IndexForm()
        return render(request, 'search/index.html', {'form': form})

    def post(self, request):
        try:
            form = IndexForm(request.POST)
        except:
            context = dict()
            context['status'] = "Data too long to index. Make sure each document is less than 255 characters."
            return render('/', 'search/home.html', context)
        if form.is_valid():
            text = form.cleaned_data['Text']
            textToDocuments(text)
            return HttpResponseRedirect('/')


def findRelevantDocuments(value):
    temp_list = value
    temp = list()
    l = 10
    if len(temp_list) < 10:
        l = len(temp_list)
    for i in range(l):
        maximum = 0
        max_frequency_document = None
        for doc_id in temp_list:
            if int(temp_list[doc_id]) > maximum:
                maximum = int(temp_list[doc_id])
                max_frequency_document = doc_id
        del temp_list[max_frequency_document]
        max_frequency_document = int(max_frequency_document)
        document = Documents.objects.get(id=max_frequency_document)
        temp.append(document)
    return temp


class SearchView(View):

    def get(self, request):
        form = SearchForm()
        return render(request, 'search/searchGET.html', {'form': form})

    def post(self, request):
        context = dict()
        form = SearchForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['Word']
            word = word.lower()
            context['word'] = word
            try:
                value = InvertedIndex.objects.get(word=word).list
                temp = findRelevantDocuments(value)
                context['documents'] = temp
                return render(request, 'search/searchPOST.html', context)
            except:
                context['status'] = "Sorry no related documents found. Retry!!"
                return render(request, 'search/home.html', context)
        else:
            context['status'] = "Invalid form submission. Retry"
            return render(request, 'search/home.html', context)



class ClearView(View):

    def get(self, request):
        context = dict()
        try:
            InvertedIndex.objects.all().delete()
            Documents.objects.all().delete()
            context['status'] = "Succesfully Cleared!! Welcome again."
        except:
            context['status'] = "Error in clear. Try again"
        return render(request, 'search/home.html', context)


class HomeView(View):

    def get(self, request):
        context = dict()
        context['status'] = "Welcome to TapSearch!"
        return render(request, 'search/home.html', context)
