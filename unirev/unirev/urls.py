"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from main_dashboard import views as mv
from personal_dashboard import views as pv
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', mv.UserViewSet)
#router.register(r'groups', mv.GroupViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mv.main_dashboard, name="index"),
    path('about/', mv.about, name="about"),
    path('contact/', mv.contact, name="contact"),
    path('privacy/', mv.privacy, name="privacy"),
    path('feedback', mv.feedback, name="feedback"),
    path('feedback_send/', mv.feedback_send, name="feedback_send"),
    path('signin/', mv.signin, name="signin"),
    path('signup/', mv.signup, name="signup"),
    path('profile/', mv.profile, name="profile"),
    path('profile/<int:pk>/', mv.profile, name="profile_with_pk"),
    path('settings/<int:pk>/', mv.settings, name='settings'),
    path('profile_edit_name/<int:pk>/', mv.profile_edit_name, name='profile_edit_name'),
    path('profile_edit_name_ajax/', mv.profile_edit_name_ajax, name='profile_edit_name_ajax'),
    path('profile_edit_password/<int:pk>/', mv.profile_edit_password, name='profile_edit_password'),
    path('profile_edit_password_ajax/', mv.profile_edit_password_ajax, name='profile_edit_password_ajax'),
    path('profile_edit_email/<int:pk>/', mv.profile_edit_email, name='profile_edit_email'),
    path('profile_edit_email_ajax/', mv.profile_edit_email_ajax, name='profile_edit_email_ajax'),
    path('profile_edit_status/<int:pk>/', mv.profile_edit_status, name='profile_edit_status'),
    path('profile_edit_status_ajax/', mv.profile_edit_status_ajax, name='profile_edit_status_ajax'),
    path('profile_images/<int:pk>/', mv.profile_images, name='profile_images'),
    path('delete_review/', mv.delete_review, name='delete_review'),
    path('delete_comment/', mv.delete_comment, name='delete_comment'),
    path('deactivate_account/<int:pk>/', mv.deactivate_account, name='deactivate_account'),
    path('uni_homepage/<int:pk>/', mv.uni_homepage, name='uni_homepage'),  # university homepage path
    path('uni_images/<int:pk>/', mv.uni_images, name='uni_images'),  # university Images homepage path
    path('uni_reviews_post_ajax/', mv.uni_reviews_post_ajax, name='uni_reviews_post_ajax'),  # university homepage path
    path('uni_unit_of_study/<int:pk>/', mv.uni_unit_of_study, name='uni_unit_of_study'),  # unit of study list page
    path('uos_experience/<int:pk>/', mv.uos_experience, name='uos_experience'),  # UOS experience page
    path('uos_experience_post_ajax/', mv.uos_experience_post_ajax, name='uos_experience_post_ajax'),  # post exp on Uos
    path('post_comments_on_reviews/<int:pk>/', mv.post_comments_on_reviews, name='post_comments_on_reviews'),
    path('post_comments_on_reviews_ajax/', mv.post_comments_on_reviews_ajax, name='post_comments_on_reviews_ajax'),
    path('post_ratings_on_uni_ajax/', mv.post_ratings_on_uni_ajax, name='post_ratings_on_uni_ajax'),
    path('post_ratings_on_uos_ajax/', mv.post_ratings_on_uos_ajax, name='post_ratings_on_uos_ajax'),
    path('personal_dashboard/', pv.personal_dashboard, name="pv_dashboard"),
    re_path(r'^', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
