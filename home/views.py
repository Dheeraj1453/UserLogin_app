from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from home.models import Contact, Profile


@login_required
def home(request):

    contacts = Contact.objects.filter(user=request.user)

    return render(request, 'home.html', {
        'contacts': contacts
    })


# Login view
def loginUser(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')

#add_contact view
def addContact(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        contact_number = request.POST.get('contact_number')
        relation = request.POST.get('relation')
        image = request.FILES.get('image')

        Contact.objects.create(
            user=request.user,
            name=name,
            contact_number=contact_number,
            relation=relation,
            image=image
        )

        return redirect('home')
    return render(request, 'add_contact.html')

#edit_contact view
@login_required
def editContact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)

    if request.method == 'POST':
        contact.name = request.POST.get('name')
        contact.contact_number = request.POST.get('contact_number')
        contact.relation = request.POST.get('relation')

        if 'image' in request.FILES:
            contact.image = request.FILES['image']

        contact.save()
        return redirect('home')

    return render(request, 'edit_contact.html', {'contact': contact})


#delete_contact view
def deleteContact(request):

    if request.method == 'POST':

        contact_id = request.POST.get('contact_id')

        contact = Contact.objects.get(id=contact_id)
        contact.delete()

        return redirect('home')

    return redirect('home')


# Register view
def registerUser(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        if len(password) < 8:
            return render(request, 'register.html', {
                'error': 'Password must be at least 8 characters'
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=name,
            email=email
        )

        Profile.objects.create(
            user=user,
            gender=gender
        )

        return redirect('login')

    return render(request, 'register.html')

#llogout view
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return redirect('login')

#forget password view
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def forgot_password(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {
                'error': 'Invalid username'
            })

        if not user.email:
            return render(request, 'forgot_password.html', {
                'error': 'No email address is associated with this account'
            })

        # Encode user ID
        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        # Generate Django password reset token
        token = default_token_generator.make_token(user)

        print("USER ID:", user.pk)
        print("UID:", uid)
        print("TOKEN:", token)

        print("TOKEN CHECK:", default_token_generator.check_token(user, token))

        # Create reset URL
        reset_url = request.build_absolute_uri(
            reverse(
                'password_reset_confirm',
                kwargs={
                    'uidb64': uid,
                    'token': token
                }
            )
        )

        print("RESET URL:", reset_url)

        send_mail(
            subject='Password Reset',
            message=f'Click this link to reset your password:\n\n{reset_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return render(request, 'forgot_password.html', {
            'success': 'Password reset link has been sent to your email.'
        })

    return render(request, 'forgot_password.html')

#reset password view
def reset_password(request, uidb64, token):

    print("RESET PASSWORD VIEW CALLED")
    print("REQUEST METHOD:", request.method)
    print("TOKEN RECEIVED:", token)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        print("USER:", user.username)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):

        print("INVALID USER")

        return render(request, 'reset_password.html', {
            'error': 'Invalid reset link'
        })


    if not default_token_generator.check_token(user, token):


        return render(request, 'reset_password.html', {
            'error': 'This reset link is invalid or expired'
        })

    print("TOKEN VALID")

    if request.method == 'POST':

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'reset_password.html', {
                'error': 'Passwords do not match'
            })

        if len(password) < 8:
            return render(request, 'reset_password.html', {
                'error': 'Password must be at least 8 characters'
            })

        user.set_password(password)
        user.save()

        return redirect('login')

    return render(request, 'reset_password.html')