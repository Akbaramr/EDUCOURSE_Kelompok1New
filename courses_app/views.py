from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.query import QuerySet
from django.views.generic import (ListView, 
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from courses_app.models import Post
from courses_app.forms import PostForm
from user_app.models import Teacher
# Create your views here.

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = PostForm
    model = Post
    template_name = 'courses_app/post_form.html'  # Pastikan Anda menentukan template yang tepat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ambil instance Teacher untuk pengguna yang sedang login
        teacher = Teacher.objects.get(user=self.request.user)
        
        # Ambil semua post yang ditulis oleh guru ini
        context['posts'] = Post.objects.filter(author=teacher).order_by('-created_date')  # Mengurutkan berdasarkan tanggal pembuatan terbaru
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        # Mengaitkan post dengan guru yang sedang login
        post.author = Teacher.objects.get(user=self.request.user)
        post.save()  # Simpan post ke database
        return redirect('post_draft_list')  # Ganti dengan nama URL yang sesuai

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        # Simpan post terlebih dahulu
        post = form.save(commit=False)
        post.save()  # Save post ke database
        # Redirect ke halaman draft list
        return redirect('post_draft_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Post
    template_name = 'courses_app/post_draft_list.html'
    context_object_name = 'posts'  # Change default 'object_list' to 'posts'

    def get_queryset(self):
        # Get the Teacher instance related to the logged-in User
        teacher = Teacher.objects.get(user=self.request.user)
        return Post.objects.filter(author=teacher, published_date__isnull=True).order_by('created_date')
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_new')

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
