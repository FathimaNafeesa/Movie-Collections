from django.utils.deprecation import MiddlewareMixin

from movie_collection.serializers import RequestCounterSerializer


class RequestMiddleware(MiddlewareMixin):

    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):

        response = self.get_response(request)

        return response

    @staticmethod
    def process_request(request):
        hit = request.session.get('hit', 0)
        request.session['hit']=hit
        if hit < 100:
            request.session['hit'] += 1
        else:
            raise TimeoutError

    @staticmethod
    def process_response(request, response):
        request_count = RequestCounterSerializer(data={'hits': request.session['hit']})
        if request_count.is_valid(raise_exception=True):
            status_code = response.status_code
            request.session['response'] = status_code
            request_count.save()
        return response

