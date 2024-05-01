from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import TodoItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.


# class based views for the todo app
class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todolist')

def custom_logout(request):
    logout(request)
    return redirect('login')
class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todolist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todolist')
        return super(RegisterPage,self).get(*args, **kwargs)
    
class TodoList(LoginRequiredMixin, ListView):
    model = TodoItem
    template_name = 'todo/index.html'
    context_object_name = 'todolist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todolist'] = context['todolist'].filter(user=self.request.user)
        context['count'] = context['todolist'].filter(complete=False).count()
        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['todolist'] = context['todolist'].filter(title__startswith=search_input)
        context['search_input'] = search_input
        return context

class TodoDetail(LoginRequiredMixin,DetailView):
    model = TodoItem
    template_name = 'todo/detail.html'
    context_object_name = 'todoitem'

class TodoCreate(LoginRequiredMixin,CreateView):
    model = TodoItem
    template_name = 'todo/form.html'
    fields = ['title','description','complete']
    success_url = reverse_lazy('todolist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate,self).form_valid(form)

class TodoUpdate(LoginRequiredMixin,UpdateView):
    model = TodoItem
    template_name = 'todo/form.html'
    fields = ['title','description','complete']
    success_url = reverse_lazy('todolist')

class TodoDelete(LoginRequiredMixin,DeleteView):
    model = TodoItem
    context_object_name = 'todoitem'
    template_name = 'todo/delete.html'
    success_url = reverse_lazy('todolist')

    