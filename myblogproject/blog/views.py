from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.template.loader import render_to_string
from .models import Post
from .forms import CommentForm
from polls.models import Question, Vote

# -----------------
# R (Read) - List View (Index)
# -----------------
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 3  # Changed to 3 posts per page 
    
    def get_queryset(self):
        # Current filtering/ordering logic
        return Post.objects.all().order_by('-pub_date') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_question = Question.objects.order_by('-pub_date').first()
        context['poll_question'] = latest_question
        
        if latest_question and self.request.user.is_authenticated:
            context['user_has_voted'] = Vote.objects.filter(
                user=self.request.user, 
                question=latest_question
            ).exists()
        else:
            context['user_has_voted'] = False
            
        return context 

# -----------------
# C (Create) - New Post
# -----------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'image', 'category'] 
    
    def form_valid(self, form):
        form.instance.author = self.request.user 
        form.instance.pub_date = timezone.now()
        return super().form_valid(form)

# -----------------
# U (Update) - Edit Existing Post (Secured by Author)
# -----------------
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html' 
    fields = ['title', 'content', 'image', 'category'] 
    
    def test_func(self):
        post = self.get_object() 
        return self.request.user == post.author

# -----------------
# D (Delete) - Delete Post (Secured by Author)
# -----------------
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html' 
    success_url = reverse_lazy('blog:index')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# -----------------
# R (Read) - Detail View + Comment Submission Handler (Function-Based)
# -----------------
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Filter only active comments
    comments = post.comments.filter(active=True) 
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Return the new comment as HTML to append
                html = render_to_string('blog/comment_partial.html', {'comment': new_comment})
                return JsonResponse({'html': html, 'success': True})
                
            # Redirect to prevent form resubmission (Pattern of Post-Redirect-Get)
            return redirect(post.get_absolute_url()) 
        else:
             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': comment_form.errors})

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

# -----------------
# Like/Unlike Action View (Function-Based)
# -----------------
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = False
    
    if request.user.is_authenticated:
        # Check if the user has already liked the post
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user) # UNLIKE
            liked = False
        else:
            post.likes.add(request.user) # LIKE
            liked = True
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked, 
            'count': post.likes.count()
        })
    
    # Redirects back to the detail page after like/unlike action
    return HttpResponseRedirect(reverse('blog:detail', args=[str(pk)]))

def clear_likes(request, pk):
    print(f"Clear likes requested for post {pk}") # Debug log
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST' or request.method == 'PATCH': 
        print("Method is POST or PATCH, clearing likes...") # Debug log
        post.likes.clear()
        print(f"Likes cleared. Count: {post.likes.count()}") # Debug log
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
             return JsonResponse({'count': 0, 'success': True})
    return HttpResponseRedirect(reverse('blog:detail', args=[str(pk)]))

def category_view(request, cats):
    category_posts = Post.objects.filter(category__name__iexact=cats.replace('-', ' '))
    return render(request, 'blog/category_list.html', {'cats': cats.replace('-', ' ').title(), 'category_posts': category_posts})


class SignUpView(CreateView):
    # Uses Django's built-in form for user creation (handles fields like username, password, password confirmation)
    form_class = UserCreationForm 
    
    # The template file we will create
    template_name = 'registration/signup.html' 
    
    # After successful registration, redirect the user to the login page
    success_url = reverse_lazy('login')