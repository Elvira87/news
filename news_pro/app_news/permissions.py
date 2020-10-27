# from rest_framework.permissions import BasePermission
# from .models import News, Users
#
#
# class IsUserOwnerOrGet(BasePermission):
#     def has_permission(self, request, view):
#         if request.method == 'GET' or request.method == 'POST':
#             return True
#         else:
#             users_a = Users.objects.get(id=view.kwargs['pk'])
#             return request.user == users_a.users
#
#
# class IsNewsOwnerOrGet(BasePermission):
#     def has_permission(self, request, view):
#         if request.method == 'GET' or request.method == 'POST':
#             return True
#         else:
#             news = News.objects.get(id=view.kwargs['pk'])
#             users_a = news.creators
#             return request.user == users_a.users