import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ads, Category


# Create your views here.
class DefaultView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(View):
    def get(self, request):
        ads = Ads.objects.all()
        response = [{"id": i.id,
                     "name": i.name,
                     "author": i.author,
                     "price": i.price}
                    for i in ads]
        return JsonResponse(data=response, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        ad_data = json.loads(request.body)
        ad = Ads()

        ad.name = ad_data['name']
        ad.author = ad_data['author']
        ad.price = ad_data['price']
        ad.description = ad_data['description']
        ad.address = ad_data['address']
        ad.is_published = ad_data['is_published']

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad.save()

        return JsonResponse(data={"id": ad.id,
                                  "name": ad.name,
                                  "author": ad.author,
                                  "price": ad.price,
                                  "description": ad.description,
                                  "address": ad.address,
                                  "is_published": ad.is_published}, json_dumps_params={'ensure_ascii': False})


class AdView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse(data={"id": ad.id,
                                  "name": ad.name,
                                  "author": ad.author,
                                  "price": ad.price,
                                  "description": ad.description,
                                  "address": ad.address,
                                  "is_published": ad.is_published}, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        cats = Category.objects.all()
        response = [{"id": i.id,
                     "name": i.name, }
                    for i in cats]
        return JsonResponse(data=response, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        cat_data = json.loads(request.body)
        cat = Category()

        cat.name = cat_data['name']

        try:
            cat.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        cat.save()

        return JsonResponse(data={"id": cat.id,
                                  "name": cat.name}, json_dumps_params={'ensure_ascii': False})


class CatView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse(data={"id": cat.id,
                                  "name": cat.name, },
                            json_dumps_params={'ensure_ascii': False})
