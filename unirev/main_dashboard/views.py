from django.shortcuts import render
from main_dashboard.models import *
from main_dashboard.serializers import *
from rest_framework import viewsets, permissions
from django.http import HttpResponse
from django.contrib.sessions.models import Session
import bcrypt
import hashlib
import datetime
from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404

# render web-page here


def main_dashboard(request):

    # Searching the user input in our db for name of University
    # if no result then we display the list of uni we have in our db
    if request.method == "POST":
        query = request.POST.get('query')

        if '<script>' in query:
            return render(request, "main_dashboard/404_error.html")
        try:
            search_results = Universities.objects.filter(uni_name__icontains=query)
            if search_results:
                if 'email_input' in request.session:
                    session = Session.objects.get(session_key=request.session.session_key)
                    session_data = session.get_decoded()
                    user = Users.objects.get(email=session_data['email_input'])
                    data = {
                        'user_info': user,
                        'uni': search_results,
                        'query': query,
                    }
                    print("reached here2" + query)
                    return render(request, "main_dashboard/search_results.html", {'data': data})
                else:
                    data = {
                        'uni': search_results,
                        'query': query,
                    }
                    return render(request, "main_dashboard/search_results.html", {'data': data})
            else:
                all_uni_info = Universities.objects.all()
                if 'email_input' in request.session:
                    session = Session.objects.get(session_key=request.session.session_key)
                    session_data = session.get_decoded()
                    user = Users.objects.get(email=session_data['email_input'])
                    all_uni_info = Universities.objects.all()
                    list_data = {
                        'user_info': user,
                        'uni_list': all_uni_info,
                        'query': query,
                    }
                    return render(request, "main_dashboard/search_results.html", {'list_data': list_data})
                else:
                    list_data = {
                        'uni_list': all_uni_info,
                        'query': query,
                    }
                    return render(request, "main_dashboard/search_results.html", {'list_data': list_data})
        except:
            # if found nothing useful , I suggest return a http code instead of a page
            return render(request, "main_dashboard/404_error.html")

    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])
        data = {
            'user_info': user,
        }

        return render(request, "main_dashboard/index.html", {'data': data})
    else:
        return render(request, "main_dashboard/index.html")


def about(request):
    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])
        data = {
            'user_info': user,
        }
        return render(request, "main_dashboard/about.html", {'data': data})
    else:
        return render(request, "main_dashboard/about.html")


def contact(request):
    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])
        data = {
            'user_info': user,
        }
        return render(request, "main_dashboard/contact.html", {'data': data})
    else:
        return render(request, "main_dashboard/contact.html")


def privacy(request):
    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])
        data = {
            'user_info': user,
        }
        return render(request, "main_dashboard/privacy.html", {'data': data})
    else:
        return render(request, "main_dashboard/privacy.html")


def feedback(request):
    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])
        data = {
            'user_info': user,
        }
        return render(request, "main_dashboard/feedback.html", {'data': data})
    else:
        return render(request, "main_dashboard/feedback.html")


def sign_in_unsuccessful(request):
    return render(request, "main_dashboard/sign_in_not_succeed.html")


def feedback_send(request):
    # Feedback send by user is received here.
    if request.method == 'POST':
        name = request.POST["full_name"]
        email = request.POST["email"]
        get_text = request.POST["feedback"]

        if '<script>' not in (get_text,name,email):
            f = open("feedback.txt", "a+")
            f.write('Name: '+ name + " " + 'Email: ' + email + " " + "Feedback: " + get_text)
            f.write('  Time received at: ' + str(datetime.datetime.now()))
            f.write('\n')
            f.close()
            if 'email_input' in request.session:
                session = Session.objects.get(session_key=request.session.session_key)
                session_data = session.get_decoded()
                user = Users.objects.get(email=session_data['email_input'])
                data = {
                    'user_info': user,
                }
                return render(request, "main_dashboard/feedback_send.html", {'data': data})
            else:
                return render(request, "main_dashboard/feedback_send.html")
        else:
            return render(request, "main_dashboard/404_error.html")


def signin(request):
    return render(request, "main_dashboard/signin.html")


def signup(request):
    # Create new user here. If everything is successful new user will be created and added to db.
    if request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        # Security check to prevent XSS attack
        if '<script>' in (name,password,re_password):
            return render(request, "main_dashboard/404_error.html")

        # render the signup page again if password re-enter doesn't matches
        if password != re_password:
            reason = "Password doesn't match"
            data = {
                'reason': reason,
            }
            return render(request, "main_dashboard/signup.html", {'data': data})
        uni = request.POST.get('university')
        bday = request.POST.get('bday')
        status = request.POST.get('dropdown')

        # Security check to prevent XSS attack
        if '<script>' in uni:
            return render(request, "main_dashboard/404_error.html")

        # Check if email already exist in db
        try:
            a = Users.objects.get(email=email)
            reason = "Email already taken"
            data = {
                'reason': reason,
            }
            return render(request, "main_dashboard/signup.html", {'data': data})

        except Users.DoesNotExist:

            # salt and hashing the password and storing in db
            salt = bcrypt.gensalt()
            salt.decode('utf-8')
            hash = hashlib.sha512()
            hash.update(('%s%s' % (salt, password)).encode('utf-8'))
            password_hash = hash.hexdigest()

            # Saving user to database
            user_to_store = Users(email=email, full_name=name, university_studies=uni, dob=bday,
                                  passwords=password_hash,
                                  salt=salt, status=status)
            user_to_store.save()
            return render(request, "main_dashboard/sign_up_success.html")

    return render(request, "main_dashboard/signup.html")


def profile(request, pk=None):
    # Displays User information here once they logged in
    if pk and request.method == "GET" and 'email_input' in request.session:
        a = Users.objects.get(user_id=pk)
        img_obj = a.userimage_set.all()
        data = {
            'user_info': a,
            'user_img': img_obj,
        }
        return render(request, "main_dashboard/profile.html", {'data': data})

    # Signing user out
    if request.method == "GET":
        if 'action' in request.GET:
            action = request.GET.get('action')
            # if user sign outs we delete the session.
            if action == 'sign_out':
                if request.session.has_key('email_input'):
                    request.session.flush()
                    return render(request, "main_dashboard/sign_out.html")

    if request.method == "GET" and 'email_input' not in request.session:
            return render(request, "main_dashboard/signin.html")

    if request.method == "POST":
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')

        # Security check to prevent XSS attack
        if '<script>' in (email_input,password_input):
            return render(request, "main_dashboard/404_error.html")

        try:
            a = Users.objects.get(email=request.POST.get('email'))
            salt = a.salt
            hash = hashlib.sha512()
            hash.update(('%s%s' % (salt, password_input)).encode('utf-8'))
            password_input_hash = hash.hexdigest()

            if a.passwords == password_input_hash:
                # img_obj = Userimage.objects.get(user=a.user_id)
                # print(a.user_id)
                img_obj = a.userimage_set.all()

                data = {
                    'user_info': a,
                    'user_img': img_obj,
                }
                # Setting up the session here
                request.session['email_input'] = email_input
                #request.session.set_expiry(300)
                return render(request, "main_dashboard/profile.html", {'data': data})
            else:
                return render(request, "main_dashboard/sign_in_not_succeed.html")
        except:
            return render(request, "main_dashboard/sign_in_not_succeed.html")


def profile_images(request, pk):
    # Get all the images that user have in db and upload image here
    try:
        if request.method == "POST" and request.FILES['file']:
            if 'email_input' in request.session:
                    img_to_upload = request.FILES['file']
                    if int(img_to_upload.size) > 5242880:
                        return render(request, "main_dashboard/404_error.html")
                    if (str(img_to_upload).lower().endswith(('.png', '.jpg', '.jpeg', 'gif'))):
                        img_to_store = Userimage(user=Users.objects.get(user_id=pk), image=img_to_upload)
                        img_to_store.save()
                        user = Users.objects.get(user_id=pk)
                        img_obj = user.userimage_set.all()
                        data = {
                            'user_info': user,
                        }
                        print('reached here2')
                        return render(request, "main_dashboard/image_added.html", {'data': data})
                    else:
                        print("the format is: " + str(img_to_upload).lower())
                        return render(request, "main_dashboard/404_error.html")
            else:
                return render(request, "main_dashboard/signin.html")
        else:

            a = Users.objects.get(user_id=pk)
            img_obj = a.userimage_set.all()
            data = {
                'user_info': a,
                'user_img': img_obj,
            }
            return render(request, "main_dashboard/profile_images.html", {'data': data})
    except:
        return render(request, "main_dashboard/404_error.html")


def settings(request, pk):
    # Get setting page for user
    # User can upload their profile image and will be updated in db
    try:
        if request.method == "POST" and request.FILES['file']:
            if 'email_input' in request.session:
                img_to_upload = request.FILES['file']
                if(str(img_to_upload).lower().endswith(('.png', '.jpg', '.jpeg','gif'))):
                    img_to_store = Userimage(user=Users.objects.get(user_id=pk), image=img_to_upload)
                    img_to_store.save()
                else:
                    print("the format is: " + str(img_to_upload).lower())
                    raise Exception('Bad input foramt')
            else:
                return render(request, "main_dashboard/signin.html")

        # print("PK of the user name: " + str(pk))
        a = Users.objects.get(user_id=pk)
        data = {
            'user_info': a,
        }
        return render(request, "main_dashboard/settings.html", {'data': data})
        # No file chosen, return HTTP 400
    except:
        return render(request, "main_dashboard/404_error.html")


def profile_edit_name(request, pk):
    # Change user's email here and update in db
    if 'email_input' in request.session and request.method == "GET":
        a = Users.objects.get(user_id=pk)

        data = {
            'user_info': a,
        }
        return render(request, "main_dashboard/profile_edit_name.html", {'data': data})
    return render(request, "main_dashboard/signin.html")


def profile_edit_name_ajax(request):
    # Get user full name here and give them options to change.
    if request.is_ajax() and request.method == "POST" and 'email_input' in request.session:
        name = request.POST.get('name')
        pk = request.POST.get('pk')

        # Security check to prevent XSS attack
        if '<script>' in name:
            return HttpResponse(status=400)

        user_to_update = Users.objects.get(user_id=pk)
        user_to_update.full_name = name
        user_to_update.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def profile_edit_password(request, pk):
    # Get options to change their password here.
    if 'email_input' in request.session and request.method == "GET":
        a = Users.objects.get(user_id=pk)
        data = {
            'user_info': a,
        }
        return render(request, "main_dashboard/profile_edit_password.html", {'data': data})
    return render(request, "main_dashboard/signin.html")


def profile_edit_password_ajax(request):
    # Change user's password here and will be updated in db
    if request.is_ajax() and request.method == "POST" and 'email_input' in request.session:
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        pk = request.POST.get('pk')

        if password != re_password:
            return HttpResponse(status=404)
        # Security check to prevent XSS attack
        if '<script>' in password:
            return HttpResponse(status=400)

        user_to_update = Users.objects.get(user_id=pk)
        # getting new salt and hashing the password and storing in db
        salt = bcrypt.gensalt()
        salt.decode('utf-8')
        hash = hashlib.sha512()
        hash.update(('%s%s' % (salt, password)).encode('utf-8'))
        password_hash = hash.hexdigest()
        user_to_update.salt = salt
        user_to_update.passwords = password_hash
        user_to_update.save()
        return HttpResponse(status=204)


def profile_edit_email(request, pk):
    # Get user email and give them options to change their email here.
    if 'email_input' in request.session and request.method == "GET":
        a = Users.objects.get(user_id=pk)
        data = {
            'user_info': a,
        }
        return render(request, "main_dashboard/profile_edit_email.html", {'data': data})
    return render(request, "main_dashboard/signin.html")


def profile_edit_email_ajax(request):
    # Change user's email ID here and will be updated in db
    if request.is_ajax() and request.method == "POST" and 'email_input' in request.session:
        email = request.POST.get('email')
        pk = request.POST.get('pk')

        # Check if email already exist in db
        try:
            a = Users.objects.get(email=email)
            return HttpResponse(status=404)
        except Users.DoesNotExist:
            if '<script>' in email:
                return HttpResponse(status=400)
            user_to_update = Users.objects.get(user_id=pk)
            user_to_update.email = email
            user_to_update.save()
            return HttpResponse(status=204)


def profile_edit_status(request, pk):
    # Get user status and give them options to change their status if they want.
    if 'email_input' in request.session and request.method == "GET":
        a = Users.objects.get(user_id=pk)
        data = {
            'user_info': a,
        }
        return render(request, "main_dashboard/profile_edit_status.html", {'data': data})
    return render(request, "main_dashboard/signin.html")


def profile_edit_status_ajax(request):
    # Change the user status e.g from students to staff and will be updated in db
    if request.is_ajax() and request.method == "POST" and 'email_input' in request.session:
        status = request.POST.get('status')
        pk = request.POST.get('pk')
        user_to_update = Users.objects.get(user_id=pk)
        user_to_update.status = status
        user_to_update.save()
        return HttpResponse(status=204)


def deactivate_account(request, pk):
    # Delete the Users account here and will be deleted from db
    if request.method == "POST":
        # following code will delete the account that's why its commented for now.
        account = Users.objects.get(user_id=pk)
        account.delete()
        return render(request, "main_dashboard/account_delete_success.html")


def uni_homepage(request, pk):
    # Get university information with all the reviews that User has posted for them
    uni = Universities.objects.get(uni_id=pk)
    uni_reviews = uni.reviews_set.all()

    # getting user information from sessions
    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])

        data = {
            'user_info': user,
            'uni': uni,
            'reviews': uni_reviews,
        }
        return render(request, "main_dashboard/uni_homepage.html", {'data': data})

    # Render the page without user info
    data = {
        'uni': uni,
        'reviews': uni_reviews,
    }
    return render(request, "main_dashboard/uni_homepage.html", {'data': data})


def uni_images(request, pk):
    # Get all the images of university that we have in Database
    uni = Universities.objects.get(uni_id=pk)
    uni_images = uni.uniimage_set.all()

    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])

        data = {
            'user_info': user,
            'uni': uni,
            'uni_images': uni_images,
        }
        return render(request, "main_dashboard/uni_images.html", {'data': data})

    else:
        data = {
            'uni': uni,
            'uni_images': uni_images,
        }
        return render(request, "main_dashboard/uni_images.html", {'data': data})


def uni_reviews_post_ajax(request):
    # Post reviews on University here. Only logged in user can post comments and will be updated in db
    if request.is_ajax() and request.method == "POST" and 'email_input' in request.session:
        review = request.POST.get('reviews')
        pk_uni = request.POST.get('pk_uni')

        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])
        pk_user = user.user_id
        print("User posting review PK: " + str(pk_user))
        print(Users.objects.get(user_id=pk_user).user_id)
        # Security check to prevent XSS attack
        if '<script>' in review:
            return HttpResponse(status=400)

        review_to_store = Reviews(uni=Universities.objects.get(uni_id=pk_uni), user=Users.objects.get(user_id=pk_user),
                                  reviews=review)
        review_to_store.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def uni_unit_of_study(request, pk):
    # Get all the university UOS that we have in DB
    uni = Universities.objects.get(uni_id=pk)
    unit_of_study = uni.unitofstudy_set.all()

    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])
        data = {
            'user_info': user,
            'uni': uni,
            'unit_of_study': unit_of_study,
        }
        return render(request, "main_dashboard/uni_unit_of_study.html", {'data': data})

    data = {
        'uni': uni,
        'unit_of_study': unit_of_study,
    }
    return render(request, "main_dashboard/uni_unit_of_study.html", {'data': data})


def uos_experience(request, pk):
    # Get all the experience shared by users for particular UOS
    uos = Unitofstudy.objects.get(uos_id=pk)
    uos_exp = uos.experience_set.all()

    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])
        data = {
            'user_info': user,
            'uos': uos,
            'uos_exp': uos_exp,
        }
        return render(request, "main_dashboard/uos_experience.html", {'data': data})

    data = {
        'uos': uos,
        'uos_exp': uos_exp,
    }
    return render(request, "main_dashboard/uos_experience.html", {'data': data})


def uos_experience_post_ajax(request):
    # Post experience on UOS here. Only logged in user can post comments and will be updated in db
    if request.is_ajax() and request.method == "POST" and 'email_input' in request.session:
        experience = request.POST.get('experience')
        pk_user = request.POST.get('pk_user')
        pk_uos = request.POST.get('pk_uos')

        # Security check to prevent XSS attack
        if '<script>' in experience:
            return HttpResponse(status=400)
        exp_to_store = Experience(user=Users.objects.get(user_id=pk_user), uos=Unitofstudy.objects.get(uos_id=pk_uos),
                                  experience=experience)
        exp_to_store.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def post_comments_on_reviews(request, pk):
    # Get all the comments given on Universities' each reviews
    reviews = Reviews.objects.get(reviews_id=pk)
    comments = reviews.comments_set.all()
    if 'email_input' in request.session:
        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()
        user = Users.objects.get(email=session_data['email_input'])
        data = {
            'user_info': user,
            'reviews': reviews,
            'comments': comments,
        }
        return render(request, "main_dashboard/post_comments_on_reviews.html", {'data': data})

    data = {
        'reviews': reviews,
        'comments': comments,
    }
    return render(request, "main_dashboard/post_comments_on_reviews.html", {'data': data})


def post_comments_on_reviews_ajax(request):
    # Post comments on reviews here. Only logged in user can post comments and will be updated in db
    if request.is_ajax() and request.method == "POST" and 'email_input' in request.session:
        comments = request.POST.get('comments')
        pk_user = request.POST.get('pk_user')
        pk_reviews = request.POST.get('pk_reviews')

        # Security check to prevent XSS attack
        if '<script>' in comments:
            return HttpResponse(status=400)

        comments_to_save = Comments(user=Users.objects.get(user_id=pk_user),
                                    reviews=Reviews.objects.get(reviews_id=pk_reviews),
                                    comments=comments)
        comments_to_save.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def post_ratings_on_uni_ajax(request):
    # Update rating for Universities here
    if request.is_ajax() and request.method == "POST" and 'email_input' in request.session:
        pk_uni = request.POST.get('pk_uni')
        ratings = request.POST.get('ratings')
        uni_ratings_to_update = Universities.objects.get(uni_id=pk_uni)
        uni_ratings_to_update.ratings = (uni_ratings_to_update.ratings+int(ratings)) / 2
        uni_ratings_to_update.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def post_ratings_on_uos_ajax(request):
    # Update the ratings for UOS here and will be updated in db
    if request.is_ajax() and request.method == "POST" and 'email_input' in request.session:
        pk_uos = request.POST.get('pk_uos')
        ratings = request.POST.get('ratings')
        uos_ratings_to_update = Unitofstudy.objects.get(uos_id=pk_uos)
        uos_ratings_to_update.ratings = (uos_ratings_to_update.ratings + int(ratings)) / 2
        uos_ratings_to_update.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def delete_review(request):
    # Deleting user's reviews here
    if request.method == "POST" and 'email_input' in request.session:
        try:
            pk_reviews = request.POST.get('pk_reviews')
            pk_uni = request.POST.get('pk_uni')
            session = Session.objects.get(session_key=request.session.session_key)
            session_data = session.get_decoded()
            user = Users.objects.get(email=session_data['email_input'])

            review_to_delete = Reviews.objects.get(reviews_id=pk_reviews)
            user_object = review_to_delete.user  # Getting user object to check if they reviews were posted by that user.
            if int(user_object.user_id) == int(user.user_id):
                review_to_delete.delete()
                uni = Universities.objects.get(uni_id=pk_uni)
                uni_reviews = uni.reviews_set.all()
                data = {
                    'user_info': user,
                    'uni': uni,
                    'reviews': uni_reviews,
                }
                return render(request, "main_dashboard/uni_homepage.html", {'data': data})
            else:
                error = "This was not your reviews. You can't delete this."
                data = {
                    'user_info': user,
                    'error': error,
                }
                return render(request, "main_dashboard/post_delete_error.html", {'data': data})
        except:
            pk_uni = request.POST.get('pk_uni')
            uni = Universities.objects.get(uni_id=pk_uni)
            print('reached here3')
            uni_reviews = uni.reviews_set.all()
            if 'email_input' in request.session:
                session = Session.objects.get(session_key=request.session.session_key)
                session_data = session.get_decoded()
                user = Users.objects.get(email=session_data['email_input'])
                data = {
                    'user_info': user,
                    'uni': uni,
                    'reviews': uni_reviews,
                }
                return render(request, "main_dashboard/uni_homepage.html", {'data': data})
            else:
                data = {
                    'uni': uni,
                    'reviews': uni_reviews,
                }
                return render(request, "main_dashboard/uni_homepage.html", {'data': data})

    if request.method == "POST" and 'email_input' not in request.session:
        error = "User need to log in to do this"
        data = {
            'error': error,
        }
        return render(request, "main_dashboard/post_delete_error.html", {'data': data})


def delete_comment(request):
    # Deleting comments here

    if request.method == "POST" and'email_input' in request.session:
        try:
            pk_comments = request.POST.get('pk_comments')
            pk_reviews = request.POST.get('pk_reviews')
            comment_to_delete = Comments.objects.get(comments_id=pk_comments)

            # Getting users PK
            session = Session.objects.get(session_key=request.session.session_key)
            session_data = session.get_decoded()
            user = Users.objects.get(email=session_data['email_input'])
            commented_user = comment_to_delete.user

            if int(user.user_id) == int(commented_user.user_id):
                comment_to_delete.delete()
                reviews = Reviews.objects.get(reviews_id=pk_reviews)
                comments = reviews.comments_set.all()
                data = {
                    'user_info': user,
                    'reviews': reviews,
                    'comments': comments,
                }
                return render(request, "main_dashboard/post_comments_on_reviews.html", {'data': data})
            else:
                error = "This was not your comments. You can't delete this."
                data = {
                    'user_info': user,
                    'error': error,
                }
                return render(request, "main_dashboard/post_delete_error.html", {'data': data})
        except:
            pk_reviews = request.POST.get('pk_reviews')
            reviews = Reviews.objects.get(reviews_id=pk_reviews)
            comments = reviews.comments_set.all()
            if 'email_input' in request.session:
                session = Session.objects.get(session_key=request.session.session_key)
                session_data = session.get_decoded()
                user = Users.objects.get(email=session_data['email_input'])
                data = {
                    'user_info': user,
                    'reviews': reviews,
                    'comments': comments,
                }
                return render(request, "main_dashboard/post_comments_on_reviews.html", {'data': data})
            else:
                data = {
                    'reviews': reviews,
                    'comments': comments,
                }
                return render(request, "main_dashboard/post_comments_on_reviews.html", {'data': data})

    if request.method == "POST" and 'email_input' not in request.session:
        error = "User need to log in to do this"
        data = {
            'error': error,
        }
        return render(request, "main_dashboard/post_delete_error.html", {'data': data})


class UserViewSet(viewsets.ModelViewSet):

    queryset = Users.objects.all()
    serializer_class = UsersSerializer
