from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# import pyautogui
from django.contrib.auth.models import  User
from django.core.files.storage import FileSystemStorage
from django.contrib import messages #import messages
from django.conf import settings
import requests

#
def hospital(request):
    if request.method=='POST':

        # importing geopy library
        from geopy.geocoders import Nominatim

        # calling the Nominatim tool
        loc = Nominatim(user_agent="GetLoc")

        # entering the location name----
        getLoc = loc.geocode("Gosainganj Lucknow")

        # printing address
        print(getLoc.address)

        # printing latitude and longitude
        print("Latitude = ", getLoc.latitude, "\n")
        print("Longitude = ", getLoc.longitude)
    return render(request, 'app1/hospital.html')
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('/')
        else:
            messages.error(request, 'Username or Password Wrong')

            return redirect('/')
def description(request):
    if request.method == 'POST':
        name = request.POST['name']
        name = name.upper()
        if len(name) == 0:
            messages.error(request, "write something")
            return redirect('/')
        try:
            first_character = name[0].upper()
            import json
            data = open('C:/Users/in68700007/Desktop/MidnightDocs-main/static/app1/meds.json').read()
            # opens the json file and saves the raw contents
            jsonData = json.loads(data)  # converts to a json structure
            ans = jsonData[first_character]
            data = {}
            for i in ans:
                name_ = i['name']
                lst = name_.split()
                if name in lst:
                    data['name']= i['name']
                    data['link']= i['link']
                    data['img']= i['img']
                    data['generic']= i['generic']
                    data["commercialisation"]= i["commercialisation"]
                    data["country"]= i["country"]
                    data["commercial_name"]= i["commercial_name"]
                    data["ppa"]= i['ppa']
                    data["registration"]= i["registration"]
                    data["dci"]= i['dci']
                    data["dosage"]= i['dosage']
                    data["conditioning"]= i["conditioning"]
                    break
            if len(data) != 0:
                return render(request, 'app1/results.html', {'data': data})
            messages.error("drug not present in database :(")
            return redirect('/')

        except:
            messages.error(request, "Please write valid drug name")
            return redirect('/')




    return render(request, 'app1/description.html')

def main(request):
    return render(request, 'app1/index.html')

def createblog(request,names):
    if request.method=='POST':
        print(names)
        catagoy=request.POST['catagory']
        name=request.POST['name']
        gender=request.POST['gender']
        mobile_number=request.POST['mobile-number']
        mobile_number=request.POST['mobile-number']
        email=request.POST['email']
        age=request.POST['age']
        if len(mobile_number)!=10:
            messages.error(request, 'Enter the valid mobile number')

            # pyautogui.alert('enter all the fields')
            bar = get_user_model().objects.get(username=names)
            return render(request, 'app1/createblog.html', {'bar': bar})

        if catagoy=='' or name=='' or gender=='' or mobile_number=='' or email=='' or age=='' :
            messages.error(request,'Enter All The Fields')

            # pyautogui.alert('enter all the fields')
            bar = get_user_model().objects.get(username=names)
            return render(request, 'app1/createblog.html', {'bar': bar})
        from .models import appointment
        blog=appointment(catagory=catagoy, name=names, gender=gender, mobile_number=mobile_number, age=age, email=email)
        blog.save()
        email_from=settings.EMAIL_HOST_USER

        send_mail(
            'we have just get your message regarding your doctor appointment (MidnightDocs)',
            'we will get back to you soon with all the details regarding your appointment query, till explore MidnightDocs website....',
            email_from,
            [email],
            fail_silently=False,
        )
        messages.success(request, 'Congrats! you appointment has been successfully booked, you will get further notification on your mobile number and email address')

        return redirect('/')
    else:
        bar=get_user_model().objects.get(username=names)
        return render(request, 'app1/createblog.html' , {'bar':bar})
def about(request):
    return render(request, 'app1/about.html')
def contact(request):
    if request.method=='POST':
        email=request.POST['email']
        regarding=request.POST['catagory']
        text=request.POST['textarea']
        if email=='' or regarding=='' or text=='':
            messages.error(request, 'Enter All The Fields')

            # pyautogui.alert('Enter All The Fields')
            return render(request, 'app1/contact.html')
        email_from=settings.EMAIL_HOST_USER
        send_mail(
            'we have just get your query (MidnightDocs)',
            'we get your query, we will reply it as soon as possible till explore MidnightDocs website....',
            email_from,
            [email]
        )
        from .models import contact
        con=contact(email=email, regarding=regarding, text=text)
        con.save()
        messages.success(request, "We have received your message")

        # pyautogui.confirm(' send')
        return redirect('contact')
    else:
        return render(request, 'app1/contact.html')

def signup(request):
    if request.method=='POST':
        username=request.POST['username']

        password=request.POST['password']

        password1=request.POST['password1']
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        email=request.POST['email']

        if username=='' or password=='' or password1=='' or first_name=='' or last_name=='' or email=='':
            # pyautogui.alert('Enter All The Fields')
            messages.error(request,'Enter All The Fields')
            return redirect('/')
        if len(password)<7:
            messages.error(request, 'Password should be of atleast 7 letters')
            return redirect('/')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'OOPS! ,Username already taken')
            return redirect('/')
        else:

            if password1!=password:
                messages.error(request,'Password Not Matched')
                return redirect('/')
            email_from=settings.EMAIL_HOST_USER

            send_mail(
                'Wow you have just signed up in MidnightDocs',
                'congratulations your account is now setup. you can login through the main website and can take appointments.....',
                email_from,
                [email],
                fail_silently=False,
            )
            myuser = User.objects.create_user(username,email,password)
            myuser.first_name=first_name
            myuser.last_name=last_name
            myuser.save()
            messages.success(request, 'User Created')
            return redirect('/')





def logout(request):
    auth_logout(request)
    return redirect('/')
def forgot(request):
    if request.method=='POST':
        email=request.POST['email']
        username=request.POST['username']
        if email=='' or username=='':
            messages.error(request,'Enter All The Fields')
            return redirect('forgot')

        if not User.objects.filter(username=username, email=email).exists():
            messages.error(request,'Username or Email Wrong')

            return render(request, 'app1/forgot.html')
        if User.objects.filter(username=username, email=email):
            bog = User.objects.get(username=username, email=email)
            harsh = 'This is the link, click it http://midnightdocs.herokuapp.com/forgotpass/' + str(bog.id)
            print(harsh)
            print(bog.password)
            send_mail(
                'click the link to change your password',
                harsh,
                'khannaharshit064@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Mail has been sent to your email address.')
        # pyautogui.confirm('mail has been sent to your email')
            return render(request, 'app1/forgot.html')

    else:
        return render(request, 'app1/forgot.html')


def forgotpass(request, id):
    bog = get_user_model().objects.get(id=int(id))
    return render(request, 'app1/forgetpass.html', {'bog': bog})
def changepassword(request,id):
    if request.method=='POST':
        password=request.POST['password']
        password1=request.POST['password1']
        if password!=password1:
            messages.error(request,'Password Not Matched')
            bog = get_user_model().objects.get(id=int(id))
            return render(request, 'app1/forgetpass.html', {'bog': bog})
        bog = get_user_model().objects.get(id=int(id))
        bog.set_password(password)
        bog.save()
        messages.success(request,'Password Saved')
        return render(request, 'app1/forgot.html')
def myprofile(request, name):
    bog=get_user_model().objects.get(username=name)
    print(name)
    # from .models import image
    from .models import appointment
    har=appointment.objects.filter(name=name)
    print(har)

    kar=len(har)
    return render(request,'app1/myprofile.html', {'bog': bog , 'har': har, 'kar':kar})

def allblog(request):
    from .models import blogpost
    blog=blogpost.objects.all()
    return render(request, 'app1/allblog.html', {'blog': blog })
def create(request,names):
    if request.method=='POST':
        print(names)
        try:
            image = request.FILES['image']
            fs=FileSystemStorage()
            filename=fs.save(image.name,image)
            url=fs.url(filename)
        except:
            messages.error(request,'Upload Image')

            bar = get_user_model().objects.get(username=names)
            return render(request, 'app1/create.html', {'bar': bar})
        catagoy=request.POST['catagory1']
        catagory=catagoy.lower()
        title=request.POST['title']
        textarea=request.POST['textarea1']
        print(url)
        name1=request.POST['name']
        if catagoy=='' or title=='' or textarea=='' or name1=='':
            messages.error(request,'Enter All The Fields')

            # pyautogui.alert('enter all the fields')
            bar = get_user_model().objects.get(username=names)
            return render(request, 'app1/create.html', {'bar': bar})
        from .models import blogpost
        blog=blogpost(catagory=catagory, title=title, textarea=textarea, email=name1, name=names, image=url)
        blog.save()
        messages.success(request, 'Uploaded')

        return redirect('/')
    else:
        bar=get_user_model().objects.get(username=names)
        return render(request, 'app1/create.html' , {'bar':bar})
def blogpost(request, id):
    from .models import blogpost
    blog=blogpost.objects.filter(ids=id)
    return render(request,'app1/specificblogpost.html', {'blog':blog})
def deletepost(request,id):
    from .models import appointment
    blog=appointment.objects.get(ids=id)
    name=blog.name
    print(name)
    bog=get_user_model().objects.get(username=name)
    blog.delete()
    har = appointment.objects.filter(name=name)
    print(har)
    kar = len(har)


    return render(request,'app1/myprofile.html',{'bog':bog,'har':har, 'kar':kar})
def covid(request):
    data = True
    result = None
    globalSummary = None
    countries = None
    while (data):
        try:
            result = requests.get('https://api.covid19api.com/summary')
            json = result.json()
            print(json)
            globalSummary = json['Global']
            countries = json['Countries']

            data = False
        except:
            data = True
    return render(request, 'app1/corona.html',
                  {'globalSummary': globalSummary,
                   'countries': countries})
def specialization(request):
    return render(request, 'app1/specialities.html')
