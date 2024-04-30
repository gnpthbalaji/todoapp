from django.urls import path
from .views import TodoList, TodoDetail, TodoCreate, TodoUpdate, TodoDelete, CustomLoginView, custom_logout, RegisterPage


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',custom_logout, name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TodoList.as_view(), name='todolist'),
    path('todolist/<int:pk>/', TodoDetail.as_view(), name='todoitem'),
    path('create-todo', TodoCreate.as_view(), name='create-todo'),
    path('todo-update/<int:pk>', TodoUpdate.as_view(), name='update-todo'),
    path('todo-delete/<int:pk>', TodoDelete.as_view(), name='delete-todo'),
]