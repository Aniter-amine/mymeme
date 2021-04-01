from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import CreateView, ListView, RedirectView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Memes, MemesFavourites
from .forms import MemesForm, CommentForm
from django.shortcuts import redirect
from django.urls import reverse


# Main Page
class index(ListView):
    model = Memes
    paginate_by = 1
    ordering = ["-date"]
    template_name = 'index.html'


# Add Memes Page
class addMemes(CreateView):
    model = Memes
    form_class = MemesForm
    template_name = 'add-memes.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Trending Page
def trend(request):
    trend = Memes.objects.all().order_by("-likes")[:10]
    return render(request, "trend.html", {'trend': trend})


# Memes Details Page With Comments...
def seeMemes(request, pk):
    meme = get_object_or_404(Memes, id=pk)
    comments = meme.comments.all()

    user_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        comment_form.instance.user = request.user
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.meme = meme
            user_comment.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()
    meme.views += 1
    meme.save()
    return render(request, 'see-memes.html', {'meme': meme, 'comments': comments, 'comment_form': comment_form})


# Like Feature Api
@login_required(login_url='login')
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        meme = get_object_or_404(Memes, id=id)
        if meme.likes.filter(id=request.user.id).exists():
            meme.likes.remove(request.user)
            meme.like_count -= 1
            result = meme.like_count
            meme.save()
        else:
            meme.likes.add(request.user)
            meme.like_count += 1
            result = meme.like_count
            meme.save()

        return JsonResponse({'result': result, })


# Delete Memes Page
@login_required(login_url='login')
def deleteMemes(request, pk):
    user = request.user
    meme = Memes.objects.get(id=pk)
    if user == meme.user:
        meme.delete()
    return reverse('main:index')


# Bookmark Memes Feature
@login_required(login_url='login')
def bookmarkMemes(request, pk):
    meme = get_object_or_404(Memes, id=pk)
    if meme.favourites.filter(id=request.user.id).exists():
        meme.favourites.remove(request.user)
    else:
        meme.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# List Of User Favourites Memes
@login_required(login_url='login')
def favourites(request):
    favourites = MemesFavourites.objects.filter(
        user=request.user).order_by('-date')
    context = {'favourites': favourites}
    return render(request, "favourites.html", context)
