from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.views.decorators.http import require_http_methods

from .forms import Search, CarForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

from .models import Car, Person
from django.views.generic import CreateView, \
    ListView, DeleteView, UpdateView

from django.views.generic.edit import UpdateView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def create_user(req):

    if req.method.lower() == "get":
        return render(request=req, template_name="my_app/signup.html",
                      context={"form": UserCreationForm()})

    elif req.method.lower() == "post":
        form = UserCreationForm(data=req.POST)
        if form.is_valid():
            form.save()
            login(request=req, user=form.instance)
            return redirect("home")
        else:
            return render(request=req, template_name="my_app/signup.html",
                          context={"form": form})


def logout_user(req):

    if req.user.is_authenticated:
        logout(request=req)

    return HttpResponse("Logged out")


def connect(req):

    if req.method == "GET":
        return render(request=req, template_name="my_app/login.html",
                      context={"form": LoginForm(),
                               'action': 'login'})

    elif req.method == "POST":
        un = req.POST.get("username")
        pw = req.POST.get("password")

        user = authenticate(req, username=un, password=pw)

        if user is None:
            return HttpResponse(f"wrong user info")
        else:
            login(request=req, user=user)
            return HttpResponse(f"welcome {user.username}")


def home(req):
    if req.user.is_authenticated:
        return HttpResponse(f"welcome {req.user}")
    else:
        return HttpResponse(f"welcome anonymous user")


class CarsListView(ListView):
    model = Car
    template_name = "genericListView.html"
    context_object_name = "my_car_list" # instead of car_list
    queryset = Car.objects.filter(car_type__contains="a")


class PersonCreationForm(CreateView):
    model = Person
    fields = "__all__"
    success_url = "admin/"
    # template_name = "my_tmplate.html"


class PersonUpdateView(UpdateView):
    model = Person
    fields = '__all__'
    success_url = "https://ynet.co.il"
    template_name = "my_app/person_update.html"



def add_car(req, cid):
    # cid = 123
    print(cid)
    if req.method == 'GET':

        car = Car.objects.get(pk=2)
        form = CarForm(instance=car)


        return render(request=req, template_name="my_app/add_car.html",
                      context={"form": form, "cid": cid})

    elif req.method == 'POST':
        # form = CarForm(data=req.POST)
        print(req.POST)
        car = Car.objects.get(pk=2)
        form = CarForm(instance=car)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                return HttpResponse(f"Some error: {e}")

            return HttpResponse("Car Added")
        else:
            return render(request=req, template_name="my_app/add_car.html",
                          context={"form": form, "cid": cid})





def default(request):
    # return HttpResponseRedirect("http://127.0.0.1:8000/search")
    # return HttpResponseRedirect(reverse("search_car"))
    return redirect("search_car")


def serve_msg(req):

    car = Car.objects.first()
    return render(request=req, template_name="my_app/index.html",
                  context={'msg': car.car_type})


# def search_old(req):
#     if req.method == 'GET':
#         return render(request=req, template_name="my_app/search_car.html")
#
#     elif req.method == 'POST':
#         search_str = req.POST['search_str'][0]
#         cars = Car.objects.filter(car_type__contains=search_str)
#
#         return render(request=req, template_name="my_app/cars_list.html",
#                       context={"cars": cars})


# from .forms import Search
def search(req):
    if req.method == 'GET':
        return render(request=req, template_name="my_app/search_car.html",
                context={'form':
                             Search(initial={"car_type_str": "example_str"})})

    elif req.method == 'POST':

        form = Search(data=req.POST)

        file = req.FILES.get('file')

        new_file_path = str(settings.BASE_DIR) + rf"\my_app\uploaded_files\{file.name}"
        with open(new_file_path, "wb") as fh:

            for chunk in file.chunks():
                fh.write(chunk)

            return HttpResponse("file uploaded")

        #
        # if form.is_valid():
        #
        #     # send_email(cleaned_data)
        #     return JsonResponse(form.cleaned_data)
        # else:
        #     return render(request=req, template_name="my_app/search_car.html",
        #                   context={"form": form })
        #
        #
        # return HttpResponse(str(req.POST))


def edit_car(req, cid):

    if req.method == 'GET':
        try:
            car = Car.objects.get(pk=cid)  # todo: deal with exceptions
            form = CarForm(instance=car)
            form.fields['car_type'].disabled = True
            return render(request=req, template_name="my_app/edit_car.html",
                          context={"form": form, "cid": cid})

        except Exception as e:
            return HttpResponse(f"Some error: {e}", 500)

    elif req.method == 'POST':
        try:
            car = Car.objects.get(pk=cid)
            form = CarForm(instance=car, data=req.POST)

            if form.is_valid():
                form.save()
                return HttpResponse("Car edited")
            else:
                return render(request=req, template_name="my_app/edit_car.html",
                              context={"form": form, "cid": cid})

        except Exception as e:
            return HttpResponse(f"Some error: {e}", status=500)

# from django.views.decorators.http import require_http_methods
@require_http_methods(['GET'])
def serve_cars(req):
    cars = Car.objects.all()

    return render(request=req, template_name="my_app/cars_list.html",
                  context={"cars": cars})


