from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password
from datetime import datetime

# Create your views here.

def gender_list(request):
    try:
        genders = Genders.objects.all()

        data = {
            'genders':genders
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')

            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html')     
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')

def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)

            gender = request.POST.get('gender')

            genderObj.gender = gender
            genderObj.save()

            messages.success(request, 'Gender updated succesfully!')

            data = {
                'gender': genderObj
            }
            
            return render(request, 'gender/EditGender.html', data )
        else:
            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender': genderObj
            }

            return render(request, 'gender/EditGender.html', data)
    
    except Exception as e:
        return HttpResponse(f'Error occured during edit gender: {e}')
    
def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            genderObj.delete()

            messages.success(request, 'Gender deleted successfully!')
            return redirect('/gender/list')
        else:
            
            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender': genderObj
            }
    
        return render(request, 'gender/DeleteGender.html', data)    
    except Exception as e:
        return HttpResponse(f'Error occured during delete gender: {e}')
    
def user_list(request):    
    try:
        userObj = Users.objects.select_related('gender') # SELECT * FROM INNER JOIN tbl_genders ON tbl_users.gender_id = tbl.genders.gender_id;
        
        data = {
            'users': userObj
        }
        
        return render(request, 'user/UsersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error Occured during load users: {e}')

def add_user(request):
    try:
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')

            if not birthDate:
                messages.error(request, 'Birth date is required.')
                return redirect('/user/add')

            try:
                # Validate date format
                birthDate = datetime.strptime(birthDate, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD format.')
                return redirect('/user/add')

            if password != confirmPassword:
                messages.error(request, 'Passwords do not match.')
                return redirect('/user/add')

            Users.objects.create(
                full_name=fullName,
                gender=Genders.objects.get(pk=gender),
                birth_date=birthDate,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                password=make_password(password)
            ).save()

            messages.success(request, 'User added successfully!')
            return redirect('/user/add')
        else:
            genderObj = Genders.objects.all()

            data = {
                'genders': genderObj
            }
        
        return render(request, 'user/AddUser.html', data)
    except Exception as e:
        messages.error(request, f'Error occurred during add user: {str(e)}')
        return redirect('/user/add')