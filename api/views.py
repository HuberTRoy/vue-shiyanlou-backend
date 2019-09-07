from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

# def makeGET(params):
#     """
#         {params:1, params2: 2} to params=1&params2=2
#     """

baseUrl = "https://www.shiyanlou.com/api/v2/"

# auth
@csrf_exempt
def login(request):
    content = requests.post(f"{baseUrl}auth/login/", data=request.body.decode(), headers={
        'Content-Type': 'application/json'
        })
    response = JsonResponse(content.json(), safe=False)
    # 登陆失败
    if not content.json().get('comet_token'):
        return response
    # 登录成功, 设置cookies.

    # response['Access-Control-Allow-Credentials'] = True
    # response['Access-Control-Allow-Origin'] = "http://localhost:8080"
    # for cookieName, cookieValue in content.cookies:
    # response.set_cookie('session', content.cookies['session'])
    # 似乎chrome不允许设置带有端口号的cookies. 直接把 session 用Json传了吧...
    # 用Js设置。
    with_session = content.json()
    with_session['session'] = content.cookies['session']
    return JsonResponse(with_session, safe=False)

# comment
def comment(request):
    content = requests.get(f"{baseUrl}comments/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

# path
def stages(request, pathId):
    content = requests.get(f"{baseUrl}paths/{pathId}/stages")
    return JsonResponse(content.json(), safe=False)

def path(request, pathId):
    content = requests.get(f"{baseUrl}paths/{pathId}")
    return JsonResponse(content.json(), safe=False)

def paths(request):
    content = requests.get(f"{baseUrl}paths")
    return JsonResponse(content.json(), safe=False)

# qa
def relatedQuestions(request, questionId):
    content = requests.get(f"{baseUrl}questions/{questionId}/related-questions/")
    return JsonResponse(content.json(), safe=False)

def question(request, questionId):
    content = requests.get(f"{baseUrl}questions/{questionId}")
    return JsonResponse(content.json(), safe=False)

def questionAnswers(request, questionId):
    content = requests.get(f"{baseUrl}questions/{questionId}/answers/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def recentLouplus(request):
    content = requests.get(f"{baseUrl}fringe/recent-louplus-courses/")
    return JsonResponse(content.json(), safe=False)

def recentActivities(request):
    content = requests.get(f"{baseUrl}fringe/recent-activities/")
    return JsonResponse(content.json(), safe=False)

def questions(request):
    content = requests.get(f"{baseUrl}questions/", params=request.GET)
    return JsonResponse(content.json(), safe=False)


# home
def indexPaths(request):
    content = requests.get(f"{baseUrl}index/paths")
    return JsonResponse(content.json(), safe=False)

def indexBootcamps(request):
    content = requests.get(f"{baseUrl}index/bootcamps")
    return JsonResponse(content.json(), safe=False)

def classficationCourses(request):
    content = requests.get(f"{baseUrl}index/classfication-courses/")
    return JsonResponse(content.json(), safe=False)

def louplus(request):
    content = requests.get(f"{baseUrl}index/louplus/")
    return JsonResponse(content.json(), safe=False)

def indexBanner(request):
    content = requests.get(f"{baseUrl}index/banner-pictures/")
    return JsonResponse(content.json(), safe=False)

def indexCategories(request):
    content = requests.get("http://www.shiyanlou.com/api/v2/index/categories/")
    return JsonResponse(content.json(), safe=False)

# courses 
def courseLabs(request, courseId):
    content = requests.get(f"{baseUrl}courses/{courseId}/labs")
    return JsonResponse(content.json(), safe=False)

def course(request, courseId):
    content = requests.get(f"{baseUrl}courses/{courseId}")
    return JsonResponse(content.json(), safe=False)

def categories(request):
    content = requests.get("http://www.shiyanlou.com/api/v2/courses/categories/")
    return JsonResponse(content.json(), safe=False)

def courses(request):
    content = requests.get("http://www.shiyanlou.com/api/v2/courses/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def labreports(request):
    content = requests.get(f"{baseUrl}labreports/", params=request.GET)
    return JsonResponse(content.json(), safe=False)
