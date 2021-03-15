from django.urls import path
from . import views

urlpatterns = [
    path('bmr_calculator',views.bmrCalculator,name='bmr_calculator'),
    path('bmi_calculator',views.bmiCalculator,name='bmi_calculator'),

]