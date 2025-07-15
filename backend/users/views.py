from django.shortcuts import render
# from django.views.generic import RegisterView

# Create your views here.
def chat(request):
    
    return render(request, "base.html")

def EmployeeRegistration(request):

    return render(request, "users/register-employee.html")