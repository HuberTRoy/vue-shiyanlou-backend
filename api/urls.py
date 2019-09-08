from django.urls import path

from . import views

urlpatterns = [
    path('v2/courses/', views.courses, name='courses'),
    path('v2/courses/<int:courseId>/', views.course, name='course'),
    path('v2/courses/<int:courseId>/labs/', views.courseLabs, name='courseLabs'),
    path('v2/courses/categories/', views.categories, name='categories'),
    path('v2/courses/<int:courseId>/follow/', views.follow, name='follow'),
    path('v2/courses/userstatus/', views.courseUserStatus, name='courseUserStatus'),
    path('v2/courses/<int:courseId>/join/', views.join, name='joinCourse'),

    path('v2/index/categories/', views.indexCategories, name='indexCategories'),
    path('v2/index/banner-pictures/', views.indexBanner, name='indexBanner'),
    path('v2/index/louplus/', views.louplus, name='louplus'),
    path('v2/index/classfication-courses/', views.classficationCourses, name='classficationCourses'),
    path('v2/index/bootcamps/', views.indexBootcamps, name='indexBootcamps'),
    path('v2/index/paths/', views.indexPaths, name='indexPath'),

    path('v2/fringe/recent-activities/', views.recentActivities, name='recentActivities'),
    path('v2/fringe/recent-louplus-courses/', views.recentLouplus, name='recentLouplus'),    
    
    path('v2/questions/', views.questions, name='questions'),
    path('v2/questions/<int:questionId>/', views.question, name='question'),
    path('v2/questions/<int:questionId>/answers/', views.questionAnswers, name='questionAnswers'),
    path('v2/questions/<int:questionId>/related-questions/', views.relatedQuestions, name='relatedQuestions'),

    path('v2/paths', views.paths, name='paths'),
    path('v2/paths/<int:pathId>/', views.path, name='path'),
    path('v2/paths/<int:pathId>/stages/', views.stages, name='pathStages'),

    path('v2/comments/', views.comment, name='comments'),

    path('v2/labreports/', views.labreports, name='labreports'),

    path('v2/auth/login', views.login, name='login'),

    path('v2/user/', views.userInfo, name='user'),

    path('v2/users/<int:userId>/courses/', views.userStudiedCourses, name='userStudiedCourses'),
]

