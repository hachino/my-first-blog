# coding: UTF-8
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
import csv
from mysite.settings import BASE_DIR

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
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

def item_index(request):

    CSV_PATH = BASE_DIR + "/data/items.csv"
    ITEM_LIST = []

    with open(CSV_PATH, newline="") as data :
        reader = csv.reader(data)
        for row in reader:
            ITEM_LIST.append(row)

    # params = [1,2,3,4,5]
    return render(request, 'blog/item_index.html', {'itemlist':ITEM_LIST})