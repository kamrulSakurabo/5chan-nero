from django.shortcuts import render
from .models import Post
from django.views.generic import TemplateView
from .forms import SearchForm
from .search import search_data
import requests


# Create your views here.

class Search(TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        search_data()

        latest_post = Post.objects.order_by('-postDate').first()
        # form = SearchForm()
        return render(request, self.template_name, {'post': latest_post})


    # def post(self, request, *args, **kwargs):
    #     form = SearchForm(request.POST)
    #     if form.is_valid():
    #         keyword = form.cleaned_data['keyword']
    #         search_data(keyword)
    #     return render(request, self.template_name, {'form': form})
