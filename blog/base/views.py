from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from .models import User, Post, Comment
from django.db.models import Count
from .forms import MyUserCreationForm, PostForm


# Create your views here.
def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(
        Q(heading__icontains=q) |
        Q(writer__name__istartswith=q)
    ).annotate(n_comment=Count('comment')).order_by('-updated', '-posted')

    n_post = posts.count()

    context = {'posts': posts, 'n_post': n_post}
    return render(request, 'base/home.html', context)


@login_required(login_url='sign_in')
def post(request, pk):

    post = Post.objects.get(id=pk)

    comments = post.comment_set.all()

    n_comment = post.comment_set.all().count()

    if request.method == 'POST':
        comments = Comment.objects.create(
            post=post,
            user=request.user,
            body=request.POST.get('body'),
        )

        return redirect('post', post.id)

    context = {'post': post, 'comments': comments, 'n_comment': n_comment}

    return render(request, 'base/post.html', context)


def sign_in(request):

    page = 'sign_in'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        # try:                                          #I do not want to hint the user about the actual wrong credential
        #     user = User.objects.get(email=email)
        # except:
        #     messages.error(request, 'Invalid login credentials!')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials!')

    context = {'page': page}

    return render(request, 'base/sign_in_sign_up.html', context)


def sign_up(request):

    page = 'sign_up'

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()

            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'invalid registration details!')

    context = {'form': form, 'page': page}

    return render(request, 'base/sign_in_sign_up.html', context)


def sign_out(request):
    logout(request)
    return redirect('home')


def create_post(request):

    page = 'create'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            post = form.save(commit=False)

            post.writer = request.user
            post.heading = request.POST.get('heading')
            post.image = request.FILES.get('image')
            post.detail = request.POST.get('detail')

            if not post.image:
                post.image = 'post-avatar1.png'

            post.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {'form': form, 'page': page}

    return render(request, 'base/create_post.html', context)


def edit_post(request, pk):

    page = 'edit'

    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.user != post.writer:
        return render(request, 'base/post.html')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            if not form.cleaned_data['image']:
                form.cleaned_data['image'] = post.image

            # post.heading = request.POST.get('heading')
            # post.image = request.FILES.get('image')
            # post.detail = request.POST.get('detail')

            post.save()

            return redirect(reverse('post', args=[post.id]))

    else:
        form = PostForm(instance=post)

    context = {'form': form, 'page': page}

    return render(request, 'base/create_post.html', context)


def delete_post(request, pk):

    post = Post.objects.get(id=pk)

    obj = post.heading

    if request.user != post.writer:
        return render(request, 'base/post.html')

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    context = {'obj': obj}

    return render(request, 'base/delete.html', context)


def delete_comment(request, pk):

    comment = Comment.objects.get(id=pk)

    # obj = 'your comment'

    if request.user != comment.user:
        return render(request, 'base/post.html')

    if request.method == 'POST':
        comment.delete()
        return redirect(reverse('post',  args=[comment.post.id]))

    # context = {'obj': obj}

    # return render(request, 'base/delete.html', context)


def about(request):

    context = {}

    return render(request, 'base/about.html', context)
