from .models import Bmi,Bmr

def userBmi(request):
    if request.user.is_authenticated:
        try:
            bmi = Bmi.objects.get(user = request.user)
            params = {
                "bmi" : bmi
            }
        except Bmi.DoesNotExist:
            params = {}
    else:
        params = {}
    return params

def userBmr(request):
    if request.user.is_authenticated:
        try:
            bmr = Bmr.objects.get(user = request.user)
            params = {
                "bmr" : bmr
            }
        except Bmr.DoesNotExist:
            params = {}
    else:
        params = {}
    return params