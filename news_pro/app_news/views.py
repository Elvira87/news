from datetime import datetime

import django_filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from _collections import OrderedDict
from .models import News
from django.shortcuts import render


from .serializers import NewsListSerializer, NewsDetailSerializer


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_count', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))


class NewsListView(ModelViewSet):
    authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsNewsOwnerOrGet, ]
    serializer_class = NewsListSerializer
    queryset = News.objects.all()
    lookup_field = 'pk'
    filter_backends = ([django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter])
    filter_fields = ( 'created_date', 'title', 'short_description')
    search_fields = ('created_date', 'title', 'short_description')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        return context

    # Sort the products py their qualification
    def get_queryset(self):
        queryset = News.objects.all()
        order_field = self.request.GET.get('order')
        filter_fields = {}

        if self.request.GET.get('created_date'):
            filter_fields['created_date'] = self.request.GET.get('created_date')

        if self.request.GET.get('title'):
            filter_fields['title'] = self.request.GET.get('title')

        if self.request.GET.get('short_description'):
            filter_fields['short_description'] = self.request.GET.get('short_description')

        if order_field:
            queryset = queryset.order_by(order_field)

        if filter_fields:
            queryset = queryset.filter(**filter_fields)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = NewsListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class NewsDetailView(ModelViewSet):
    authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsNewsOwnerOrGet, ]
    serializer_class = NewsDetailSerializer
    queryset = News.objects.all()
    lookup_field = 'pk'
    filter_backends = ([django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter])
    filter_fields = ('created_date', 'updated_date', 'title')
    search_fields = ('created_date', 'updated_date', 'title')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        return context

    # Sort the products py their qualification
    def get_queryset(self):
        queryset = News.objects.all()
        order_field = self.request.GET.get('order')
        filter_fields = {}

        if self.request.GET.get('created_date'):
            filter_fields['created_date'] = self.request.GET.get('created_date')

        if self.request.GET.get('updated_date'):
            filter_fields['updated_date'] = self.request.GET.get('updated_date')

        if self.request.GET.get('title'):
            filter_fields['title'] = self.request.GET.get('title')

        # if self.request.GET.get('creator'):
        #     filter_fields['creator'] = self.request.GET.get('creator')

        if order_field:
            queryset = queryset.order_by(order_field)

        if filter_fields:
            queryset = queryset.filter(**filter_fields)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = NewsDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
