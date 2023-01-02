import os

import environs as environ
import requests
from django.db.models import Count
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseNotFound
from requests.auth import HTTPDigestAuth
from django.contrib.auth import logout
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from rest_framework.views import APIView
from .constants import *
from .helper import Helper
from .models import MovieDetails, Collection, RequestsCounter
from .models import User
from .serializers import LoginUserSerializer, RegisterSerializer, CreateTaskSerializer

from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAdminUser
from .password_vulnrability_tasks import GetPassword
from .cloud_tasks import send_task

env = environ.Env()
environ.Env.read_env()

""" Index API"""


def index(request):
    return HttpResponse("Welcome to your movie collections")


"""List of Movie API"""


class ListMovieView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    template_name = 'movie_list.html'
    model = MovieDetails

    @staticmethod
    def call_movies_api(page_number=1):
        url = f"{os.environ['OS_THIRD_PARTY_URL']}{page_number}"
        result = requests.get(url, auth=HTTPDigestAuth(os.environ['OS_THIRD_PARTY_AUTH'],
                                                       os.environ['OS_THIRD_PARTY_PASSWORD']))

        response = result.json()

        return result.status_code, response

    def get(self, request, user_id, *args, **kwargs):
        try:
            page_number = request.GET.get('page', 1)
            status_code, result = self.call_movies_api(page_number)

            if status_code == HTTP_STATUS_200:
                next_page = int(page_number) + 1
                previous_page = int(page_number) - 1
                result['next'] = f'{URL}{next_page}'
                result['previous'] = f'{URL}{previous_page}'
                result['Your top genres'] = self._get_top_three_genres(user_id)
            return JsonResponse(result)
        except Exception as e:
            raise HttpResponseNotFound('<h1>Page not found</h1>')

    @staticmethod
    def _get_top_three_genres(user_id):
        data = Collection.objects.filter(user=user_id).values('genres').annotate(total=Count('genres')).order_by(
            '-total')[:3]
        return [each['genres'] for each in data]


""" Login API"""


class LoginUserView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer


"""Register API"""


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


"""Create/Edit/Delete Collection API"""


class CreateCollectionsView(generics.CreateAPIView):

    def __init__(self):
        self.helper = Helper()

    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id, *args, **kwargs):
        try:
            data = self.helper.format_create_data(request.data, user_id)
            response = self.helper.add_movie_to_collection(data)
            if response == HTTP_STATUS_200:
                return JsonResponse({'collection_uuid': data[0]['collection_uuid']})
        except Exception as e:
            raise Http404(f"{e}")

    def put(self, request, user_id, *args, **kwargs):
        try:
            data = self._format_update_data(request, user_id)
            response = self.helper.add_movie_to_collection(data)
            if response == HTTP_STATUS_200:
                return JsonResponse({"Updated Collection": data[0]['collection_uuid']})
        except Exception as e:
            raise Http404(f"{e}")

    def _format_update_data(self, response, user_id):
        c_uuid = response.GET.get('c_uuid')
        return self.helper.get_movie_list(response.data, c_uuid, user_id)

    def get(self, request, *args, **kwargs):
        try:
            collection_uuid = request.GET.get('c_uuid')
            movie_collection = Collection.objects.filter(collection_uuid=collection_uuid)
            movie_collection = list(
                movie_collection.values('collection_name', 'collection_description', 'title', 'genres',
                                        'description', ))
            response = self.helper.get_response(movie_collection, collection_uuid)
            return JsonResponse(response)
        except Exception as e:
            raise Http404(f"{e}")

    def delete(self, request, *args, **kwargs):
        try:
            collection_uuid = request.GET.get('c_uuid')
            Collection.objects.filter(collection_uuid=collection_uuid).delete()
            return HttpResponse(DELETE_SUCCESS)
        except Exception as e:
            raise Http404(f"{e}")


"""Log out API"""


class LogoutView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse(LOGOUT_SUCCESS)


"""Request Count"""


class RequestCountView(generics.ListAPIView):
    try:
        def get(self, request, *args):

            response = RequestsCounter.objects.values('hits').order_by('-id')[:1]

            for count in response:
                hits = count['hits']
            return JsonResponse({"requests": hits})
    except Exception as e:
        raise Http404(f"{e}")

    def delete(self, request, *args, **kwargs):
        try:
            requests = RequestsCounter.objects.all()
            requests.delete()
            return JsonResponse(REQUEST_COUNT_RESET_RESPONSE)
        except Exception as e:
            raise Http404(f"{e}")




class CreateTaskView(generics.CreateAPIView):
    serializer_class = CreateTaskSerializer

    def __init__(self):
        self.helper = Helper()

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        queryset = User.objects.all()
        data = self.helper.format_data_user(request.data)
        users = [each.username for each in queryset]
        user_emails = [each.email for each in queryset]

        if data['name'] in users and data['email'] in user_emails:
            response = self.create_task(data)
            if response == HTTP_STATUS_200:
                return JsonResponse({'Status': 'Created'})
        else:
            return JsonResponse({'Status': 'No such user'})

    def create_task(self, data):

        """ A simple view that triggers the task """

        send_task(data)

        return HTTP_STATUS_200


@csrf_exempt
def task_view(request):
    """ Processes a task """
    try:
        payload = request.body.decode('utf-8')

        status = GetPassword(payload['name'], payload['email']).execute()

        # get password/vulnerability script
        print(f"{payload} is completed")
        return JsonResponse({'Status': status})

    except Exception as e:

        raise Http404(f"{e}")
