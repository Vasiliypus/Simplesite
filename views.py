from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView 
from django.contrib.auth import logout, login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from rest_framework import permissions
from .models import Bb, Rubric        
from .serializers import RubricSerializer, BbSerializer
from ._fforms import BbForm, RegisterUserForm, LoginUserForm, ContactForm
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django import template
from django.core import paginator
from django.db.models.query_utils import select_related_descend
from django.conf.urls import url
from django.core.paginator import Paginator
#from rest_framework_swagger.views import get_swagger_view
#schema_view = get_swagger_view(title='simplesite')
import requests

#rest api

class RubricView(generics.ListAPIView):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class BbCrList(generics.ListCreateAPIView):
    queryset = Bb.objects.all()
    serializer_class = BbSerializer
    permission_classes = (IsAuthenticated,)

class APIBbViewSet(ModelViewSet):
    queryset = Bb.objects.all() 
    serializer_class = BbSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser, )

class APIRubricViewSet(ModelViewSet):
    queryset = Rubric.objects.all() 
    serializer_class = RubricSerializer
    permission_classes = ( IsAuthenticated, IsAdminUser,)

def api_rubrics(requests):
    if requests.method == 'GET':
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        return JsonResponse(serializer.data, safe=False)    

#end rest api

class BbDetailView(DetailView):
    #Вывод отдельных объявлений
    model = Bb
    def get_context_data(self, **kwargs):    
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class Homebb(ListView):
    #paginate_by = 4
    model = Bb
    template_name = 'bboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.order_by('-published')
        context['rubrics'] = Rubric.objects.all()
        return context
    
class Rubricdata(ListView):
    paginate_by = 4
    context_object_name = 'bbs'
    template_name = 'bboard/by_rubric.html'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(
                   pk=self.kwargs['rubric_id'])
        return context

class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm     
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'bboard/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) 
        return dict(list(context.items())) 

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'bboard/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) 
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('index')    

def logout_user(request):
    logout(request)
    return redirect('login')

class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'bboard/contact.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) 
        return dict(list(context.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('index')



# def index(request):
#         template = loader.get_template('bboard/index.html')
#    bbs = Bb.objects.order_by()
#    rubrics = Rubric.objects.all()
#    context = {'bbs':bbs, 'rubrics': rubrics}
#    return render(request, "bboard/index.html", context)        


# def by_rubric(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)    
#     rubrics = Rubric.objects.all()
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {'bbs':bbs, 'rubrics':rubrics,
#                 'current_rubric': current_rubric}
#   return render(request, 'bboard/by_rubric.html', context)

# def test(request):
#     objects = ['1','2', '3', '4', '5', '6', '7']
#     paginator = Paginator(objects, 2)
#     page_num = request.GET.get('page', 1)
#     page_objects = paginator.get_page(page_num)
#     name = object.list
#     print(name)
#     return render(request, 'bboard/test.html', {'page_obj':page_objects} )
    
#def register(request):
 #   return render(request, 'bboard/register.html')

#def login(request):
   # return render(request, 'bboard/login.html')
#from django.contrib.auth.forms import UserCreationForm
#from django.views.generic.base import TemplateView, DetailView
# class APIRubricCrList(generics.ListCreateAPIView):
#     queryset = Rubric.objects.all() 
#     serializer_class = RubricSerializer
# class BbView(APIView):
#     queryset = Bb.objects.all()
#     def get(self, request):
#         bbs = Bb.objects.all()
#         serializer = BbSerializer(bbs, many=True)
#         return Response({"bbs": serializer.data})

#     def post(self, request):
#         bbs = request.data.get('bbs')
#         serializer = BbSerializer(data=bbs)
#         if serializer.is_valid(raise_exception=True):
#             bbs_saved = serializer.save()
#         return Response({"success": "Bbs '{}' created successfully".
#             format(bbs_saved.title)})
# class BbView(generics.CreateAPIView):
#     queryset = Bb.objects.all()
#     serializer_class = BbSerializer



# class APIRubricDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Rubric.objects.all()
#     serializer_class = RubricSerializer
# queryset = Bb.objects.select_related('rubric')
    
    
   # def get_queryset(self):
     #  return Rubric.objects.all().select_related('rubric')