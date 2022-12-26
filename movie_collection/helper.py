import uuid

from django.http import Http404

from .constants import *
from .serializers import CollectionSerializer


class Helper:
    @staticmethod
    def get_movie_list(response, c_uuid, user_id):
        all_movies = []
        data = {
            'collection_name': response['collection_name'],
            'collection_description': response['collection_description'],
            'user': user_id,
            'collection_uuid': c_uuid
        }
        for movie in response['movies']:
            data.update(movie)
            all_movies.append(data)

        return all_movies


    @staticmethod
    def add_movie_to_collection(data):
        try:
            serializer = CollectionSerializer(data=data, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return HTTP_STATUS_200
        except Exception as e:
            raise Http404(f"{e}")

    @staticmethod
    def get_response(movie_collection, c_uuid):
        collection_name = movie_collection[0]['collection_name']
        collection_description = movie_collection[0]['collection_description']
        response = [{key: val for key, val in sub.items() if
                     key not in DROP_COLUMNS} for sub in
                    movie_collection]
        response = {
            'collection_name': collection_name,
            'collection_description': collection_description,
            'collection_uuid': c_uuid,
            'movies': response

        }
        return response

    def format_create_data(self, response, user_id):
        c_uuid = str(uuid.uuid4())
        return self.get_movie_list(response, c_uuid, user_id)

