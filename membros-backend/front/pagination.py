from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response


class CoffePagination(pagination.PageNumberPagination):
    page_size_query_param = 'size' # variavel de itens por pagina

    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

    # versao django-tabelas
    # page_size_query_param = 'size'
    #
    # def get_paginated_response(self, data):
    #     return Response({
    #         'links': {
    #            'next': self.get_next_link(),
    #            'previous': self.get_previous_link()
    #         },
    #         'count': self.page.paginator.count,
    #         'total_pages': self.page.paginator.num_pages,
    #         'results': data
    #     })
