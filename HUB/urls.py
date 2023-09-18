from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('quiz/<int:id>/<str:type>/', views.quiz, name='quiz'),
    path('Chat', views.Chat , name = 'Chat' ),

    #API routess
    path('get_quiz_questions/<int:research_paper_id>/', views.get_quiz_questions, name='get_quiz_questions'),
    path('ppr_update', views.ppr_update, name="ppr_update"),
    path('qz_update', views.qz_update, name="qz_update"),
    path('art_update', views.art_update, name="art_update"),
    path('artq_update', views.artq_update, name="artq_update")
]

