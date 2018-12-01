from django.test import TestCase
from django.test import Client
from main_dashboard.models import *
from django.urls import reverse

class TestUsers(TestCase):
    def setUp(self):
        Users.objects.create(email="user1@gmail.com", full_name="First User", university_studies="First Uni",
                             dob='2000-10-11', passwords='first password', status='Student')
        Users.objects.create(email="user2@gmail.com", full_name="Second User", university_studies=" First Uni",
                             passwords='second password', status='Staff')
        Users.objects.create(full_name="H")
        Users.objects.create(email="user4@gmail.com", full_name="Fourth User", university_studies=None,
                             dob=None, passwords='')
        Users.objects.create(email="user5@gmail.com", full_name="Fifth User", university_studies='',
                             dob='2000-10-11', passwords='', status='Employee')

    def test_user01(self):
        first_user = Users.objects.get(full_name='First User')
        self.assertEqual(first_user.email, 'user1@gmail.com')
        self.assertEqual(first_user.status, 'Student')
        self.assertEqual(first_user.passwords, 'first password')
        self.assertEqual(first_user.university_studies, "First Uni")
        self.assertEqual(str(first_user.dob), '2000-10-11')
        self.assertEqual(first_user.salt, '')

    def test_user02(self):
        user = Users.objects.get(full_name='Second User')
        self.assertEqual(user.email, 'user2@gmail.com')
        self.assertEqual(user.status, 'Staff')
        self.assertEqual(user.passwords, 'second password')
        self.assertEqual(user.dob, None)
        self.assertEqual(user.salt, '')

    def test_user03(self):
        user = Users.objects.get(full_name='H')
        self.assertEqual(user.email, '')
        self.assertEqual(user.status, '')
        self.assertEqual(user.passwords, '')
        self.assertEqual(user.dob, None)
        self.assertEqual(user.salt, '')

    def test_user04(self):
        user = Users.objects.get(email='user4@gmail.com')
        self.assertEqual(user.full_name, 'Fourth User')
        self.assertEqual(user.status, '')
        self.assertEqual(user.university_studies, None)
        self.assertNotEqual(user.passwords, None)
        self.assertEqual(user.dob, None)

    def test_user05(self):
        user = Users.objects.get(email='user5@gmail.com')
        self.assertEqual(user.full_name, 'Fifth User')
        self.assertEqual(user.status, 'Employee')
        self.assertEqual(user.university_studies, '')
        self.assertEqual(user.passwords, '')
        self.assertEqual(str(user.dob), '2000-10-11')

    def test_user06(self):
        all_user = Users.objects.all()
        self.assertEqual(all_user.count(), 5)
        instance = Users.objects.get(full_name='H')
        instance.delete()
        all_user = Users.objects.all()
        self.assertEqual(all_user.count(), 4)
        instance = Users.objects.get(email='user4@gmail.com')
        instance.delete()
        all_user = Users.objects.all()
        self.assertEqual(all_user.count(), 3)

    def test_user07(self):
        try:
            Users.objects.get(full_name='Hey')
        except:
            self.assertRaises(Users.DoesNotExist)

    def test_user08(self):
        try:
            Users.objects.get(email='Second')
        except:
            self.assertRaises(Users.DoesNotExist)


class TestUniversities(TestCase):
    def setUp(self):
        Universities.objects.create(uni_name="The University Of Sydney", location='Sydney Australia', ratings=5)
        Universities.objects.create(uni_name="The University Western Sydney", location=None, ratings=None)
        Universities.objects.create(uni_name="The University Of California", location='')
        Universities.objects.create(location='Melbourne', ratings=5)

    def test_university01(self):
        uni = Universities.objects.get(uni_name='The University Of Sydney')
        self.assertEqual(uni.location, 'Sydney Australia')
        self.assertNotEqual(uni.location, 'Melbourne')
        self.assertEqual(uni.ratings, 5)

    def test_university02(self):
        uni = Universities.objects.get(uni_name='The University Western Sydney')
        self.assertNotEqual(uni.location, 'Sydney Australia')
        self.assertEqual(uni.location, None)
        self.assertEqual(uni.ratings, None)

    def test_university03(self):
        uni = Universities.objects.get(uni_name='The University Of California')
        self.assertEqual(uni.location, '')
        self.assertEqual(uni.ratings, None)

    def test_university04(self):
        uni = Universities.objects.get(location='Melbourne')
        self.assertEqual(uni.uni_name, None)
        self.assertEqual(uni.ratings, 5)

    def test_university05(self):
        all_uni = Universities.objects.all()
        self.assertEqual(all_uni.count(), 4)
        instance = Universities.objects.get(location='Melbourne')
        instance.delete()
        all_uni = Universities.objects.all()
        self.assertEqual(all_uni.count(), 3)

    def test_university06(self):
        try:
            Universities.objects.get(location='Melbourne1')
        except:
            self.assertRaises(Universities.DoesNotExist)

    def test_university07(self):
        try:
            Universities.objects.get(location='Sydney')
        except:
            self.assertRaises(Universities.DoesNotExist)


class TestUnitOfStudy(TestCase):
    def setUp(self):
        Universities(uni_name='University of Technology Sydney', location='City', ratings=5).save()
        Universities(uni_name='Macquarie University', location='North Ryde', ratings=5).save()
        Universities(uni_name='Golden University', location='Golden tower', ratings=5).save()

        uni_obj = Universities.objects.get(uni_name='University of Technology Sydney')
        Unitofstudy(uni=uni_obj, unit_name='33130   Mathematical Modelling 1', ratings=5).save()
        Unitofstudy(uni=uni_obj, unit_name='48230   Engineering Communication', ratings=5).save()
        Unitofstudy(uni=uni_obj, unit_name='48023   Programming Fundamentals', ratings=1).save()

        uni_obj = Universities.objects.get(uni_name='Macquarie University')
        Unitofstudy(uni=uni_obj, unit_name='COMP115     Introduction to Computer Programming', ratings=3).save()
        Unitofstudy(uni=uni_obj, unit_name='COMP125	    Fundamentals of Computer Science', ratings=5).save()
        Unitofstudy(uni=uni_obj).save()

        uni_obj = Universities.objects.get(uni_name='Golden University')
        Unitofstudy(uni=uni_obj).save()


    def test_unit_of_study01(self):
        uos = Unitofstudy.objects.get(unit_name='33130   Mathematical Modelling 1')
        self.assertEqual(uos.ratings, 5)
        self.assertEqual(uos.uni.uni_name, 'University of Technology Sydney')

    def test_unit_of_study02(self):
        uos = Unitofstudy.objects.get(unit_name='48023   Programming Fundamentals')
        self.assertEqual(uos.ratings, 1)
        self.assertEqual(uos.uni.uni_name, 'University of Technology Sydney')

    def test_unit_of_study03(self):
        uos = Unitofstudy.objects.all()
        self.assertEqual(uos.count(), 7)
        instance = Unitofstudy.objects.get(unit_name='48230   Engineering Communication')
        instance.delete()
        uos = Unitofstudy.objects.all()
        self.assertEqual(uos.count(), 6)

    def test_unit_of_study04(self):
        uos = Unitofstudy.objects.get(unit_name='COMP115     Introduction to Computer Programming')
        self.assertEqual(uos.ratings, 3)
        self.assertEqual(uos.uni.uni_name, 'Macquarie University')

    def test_unit_of_study05(self):
        uos = Unitofstudy.objects.get(uni=Universities.objects.get(uni_name='Golden University'))
        self.assertEqual(uos.ratings, None)
        self.assertEqual(uos.unit_name, None)

    def test_unit_of_study06(self):
        try:
            Unitofstudy.objects.get(unit_name='COMP115')
        except:
            self.assertRaises(Unitofstudy.DoesNotExist)

    def test_unit_of_study07(self):
        try:
            Unitofstudy.objects.get(unit_name='COMP1159')
        except:
            self.assertRaises(Unitofstudy.DoesNotExist)


class TestReviewsAndComments(TestCase):

    def setUp(self):
        Universities(uni_name='University of Technology Sydney', location='City', ratings=5).save()
        Universities(uni_name='Macquarie University', location='North Ryde', ratings=5).save()

        Users.objects.create(email="user1@gmail.com", full_name="User1", university_studies="First Uni",
                             dob='2000-10-11', passwords='first password', status='Student')

        user = Users.objects.get(email='user1@gmail.com')
        uni_1 = Universities.objects.get(uni_name='University of Technology Sydney')
        uni_2 = Universities.objects.get(uni_name='Macquarie University')

        Reviews.objects.create(user=user, uni=uni_1, reviews="Hi there")
        Reviews.objects.create(user=user, uni=uni_1, reviews='Great time')
        Reviews.objects.create(user=user, uni=uni_1, reviews=None)
        Reviews.objects.create(user=user, uni=uni_2, reviews="Great University")
        Reviews.objects.create(user=user, uni=uni_2, reviews="")

        review_1 = Reviews.objects.get(reviews='Hi there')
        review_2 = Reviews.objects.get(reviews='Great University')

        Comments.objects.create(user=user, reviews=review_1, comments='Very helpful review')
        Comments.objects.create(user=user, reviews=review_1, comments='Good going')
        Comments.objects.create(user=user, reviews=review_1, comments=None)
        Comments.objects.create(user=user, reviews=review_2, comments='')
        Comments.objects.create(user=user, reviews=review_2, comments='Not agreeing')

    def test_reviews01(self):
        try:
            Reviews.objects.get(reviews='Hey')
        except:
            self.assertRaises(Reviews.DoesNotExist)

    def test_reviews02(self):
        review = Reviews.objects.get(reviews='Hi there')
        self.assertEqual(review.reviews, 'Hi there')
        self.assertNotEqual(review.reviews, 'Hi')

    def test_reviews03(self):
        review = Reviews.objects.get(reviews='Great time')
        self.assertNotEqual(review.reviews, None)
        self.assertEqual(review.reviews, 'Great time')
        self.assertEqual(review.uni.uni_name, 'University of Technology Sydney')
        self.assertEqual(review.user.full_name, 'User1')

    def test_reviews04(self):
        review = Reviews.objects.get(reviews='Great University')
        self.assertEqual(review.reviews, 'Great University')
        self.assertNotEqual(review.reviews, 'Great Universities')
        self.assertNotEqual(review.uni.uni_name, 'University of Technology Sydney')

    def test_reviews05(self):
        review = Reviews.objects.get(reviews='')
        self.assertEqual(review.reviews, '')
        self.assertNotEqual(review.uni.uni_name, 'University of Technology Sydney')
        self.assertNotEqual(review.reviews, 'Great Universities')

    def test_reviews06(self):
        try:
            Reviews.objects.get(reviews='H')
        except:
            self.assertRaises(Reviews.DoesNotExist)

    # Testing the comments now
    def test_comments01(self):
        try:
            Comments.objects.get(comments='Hey')
        except:
            self.assertRaises(Comments.DoesNotExist)

    def test_comments02(self):
        comments = Comments.objects.get(comments='Very helpful review')
        self.assertEqual(comments.comments, 'Very helpful review')
        self.assertNotEqual(comments.comments, 'Very')

    def test_comments03(self):
        comments = Comments.objects.get(comments=None)
        self.assertEqual(comments.comments, None)
        self.assertNotEqual(comments.comments, 'Very')

    def test_comments04(self):
        comments = Comments.objects.get(comments='')
        self.assertEqual(comments.comments, '')
        self.assertNotEqual(comments.comments, None)

    def test_comments05(self):
        comments = Comments.objects.get(comments='')
        self.assertEqual(comments.user.email, 'user1@gmail.com')
        self.assertEqual(comments.user.full_name, 'User1')
        self.assertNotEqual(comments.user.full_name, 'Users')

    def test_comments07(self):
        comments = Comments.objects.get(comments='')
        self.assertEqual(comments.reviews.reviews, 'Great University')
        self.assertNotEqual(comments.reviews.reviews, 'User1')

    def test_comments08(self):
        comments = Comments.objects.get(comments='')
        self.assertEqual(comments.reviews.reviews, 'Great University')
        self.assertNotEqual(comments.reviews.reviews, 'User1')

    def test_comments09(self):
        comments = Comments.objects.all()
        self.assertEqual(comments.count(), 5)
        instance = Comments.objects.get(comments='')
        instance.delete()
        self.assertEqual(comments.count(), 4)

    def test_reviews07(self):
        review = Reviews.objects.all()
        self.assertEqual(review.count(), 5)
        instance = Universities.objects.get(uni_name='Macquarie University')
        instance.delete()
        review = Reviews.objects.all()
        self.assertEqual(review.count(), 3)
        instance = Reviews.objects.get(reviews='Hi there')
        instance.delete()
        review = Reviews.objects.all()
        self.assertEqual(review.count(), 2)


class TestExperience(TestCase):

    def setUp(self):
        Universities(uni_name='University of Technology Sydney', location='City', ratings=5).save()
        Users.objects.create(email="user1@gmail.com", full_name="User1", university_studies="First Uni",
                             dob='2000-10-11', passwords='first password', status='Student')

        uni_obj = Universities.objects.get(uni_name='University of Technology Sydney')
        Unitofstudy(uni=uni_obj, unit_name='33130   Mathematical Modelling 1', ratings=5).save()
        Unitofstudy(uni=uni_obj, unit_name='48230   Engineering Communication', ratings=5).save()

        user = Users.objects.get(email='user1@gmail.com')
        uos_1 = Unitofstudy.objects.get(unit_name='33130   Mathematical Modelling 1')
        uos_2 = Unitofstudy.objects.get(unit_name='48230   Engineering Communication')

        Experience.objects.create(user=user, uos=uos_1, experience="Enjoyed")
        Experience.objects.create(user=user, uos=uos_1, experience="")
        Experience.objects.create(user=user, uos=uos_1)
        Experience.objects.create(user=user, uos=uos_2, experience="Was great unit")
        Experience.objects.create(user=user, uos=uos_2, experience="Thanks for reviews")

    def test_experience01(self):
        exp = Experience.objects.get(experience="Enjoyed")
        self.assertEqual(exp.experience, 'Enjoyed')

    def test_experience02(self):
        try:
            Experience.objects.get(experience='Hey')
        except:
            self.assertRaises(Experience.DoesNotExist)

    def test_experience03(self):
        exp = Experience.objects.get(experience="")
        self.assertEqual(exp.user.email, 'user1@gmail.com')
        self.assertEqual(exp.user.full_name, 'User1')
        self.assertEqual(exp.uos.unit_name, '33130   Mathematical Modelling 1')
        self.assertEqual(exp.uos.ratings, 5)

    def test_experience04(self):
        exp = Experience.objects.get(experience="Thanks for reviews")
        self.assertEqual(exp.user.email, 'user1@gmail.com')
        self.assertNotEqual(exp.user.full_name, 'User')
        self.assertNotEqual(exp.uos.unit_name, '33130   Mathematical Modelling 1')
        self.assertEqual(exp.uos.ratings, 5)

    def test_experience05(self):
        exp = Experience.objects.all()
        self.assertEqual(exp.count(), 5)

    def test_experience06(self):
        instance = Experience.objects.get(experience="Thanks for reviews")
        instance.delete()
        exp = Experience.objects.all()
        self.assertEqual(exp.count(), 4)

    def test_experience07(self):
        user = Users.objects.get(email='user1@gmail.com')
        user.delete()
        all_exp = Experience.objects.all()
        self.assertEqual(all_exp.count(), 0)

    def test_experience08(self):
        try:
            Experience.objects.get(experience='Thanks for reviews')
        except:
            self.assertRaises(Experience.DoesNotExist)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home01(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/index.html')

    def test_home02(self):
        response = self.client.get('/', follow=True)
        content = response.content.decode('utf-8')
        self.assertTrue('script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js' in content)
        self.assertTrue('link href="/static/js/bootstrap.min.js' in content)
        self.assertTrue('<link href="/static/css/bootstrap.min.css" rel="stylesheet">' in content)

    def test_home03(self):
        response = self.client.get('/', follow=True)
        content = response.content.decode('utf-8')
        self.assertTrue('placeholder="Search for University"' in content)
        self.assertTrue('About Us' in content)
        self.assertTrue('Privacy' in content)
        self.assertTrue('Feedback' in content)

    def test_home03(self):
        response = self.client.post('/', {'query': 'sydney'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/index.html')

    def test_about01(self):
        response = self.client.get('/about', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/about.html')

    def test_about02(self):
        response = self.client.get('/about', follow=True)
        content = response.content.decode('utf-8')
        self.assertTrue('script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js' in content)
        self.assertTrue('link href="/static/js/bootstrap.min.js' in content)
        self.assertTrue('About us' in content)
        self.assertTrue('Students helping out students our motto.' in content)

    def test_about03(self):
        response = self.client.post('/about', follow=True)
        self.assertNotEqual(response.status_code, 301)

    def test_contact01(self):
        response = self.client.get('/contact/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/contact.html')

    def test_contact02(self):
        response = self.client.get('/contact/', follow=True)
        content = response.content.decode('utf-8')
        self.assertTrue('script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js' in content)
        self.assertTrue('link href="/static/js/bootstrap.min.js' in content)
        self.assertTrue('Contact us' in content)
        self.assertTrue('If you find any problems or want to know more about our work.' in content)

    def test_contact03(self):
        response = self.client.post('/contact/', follow=True)
        self.assertNotEqual(response.status_code, 301)

    def test_feedback01(self):
        response = self.client.get('/feedback', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/feedback.html')

    def test_feedback02(self):
        response = self.client.get('/feedback', follow=True)
        content = response.content.decode('utf-8')
        self.assertTrue('link href="/static/js/bootstrap.min.js' in content)
        self.assertTrue('Contact us' in content)
        self.assertTrue('Please provide us a feedback here.' in content)

    def test_feedback03(self):
        response = self.client.post('/feedback/', {'full_name': 'Jason Bond', 'email': 'Bond0007@gmail.com', 'feedback':
                                                    'Bond James Bond'}, follow=True)
        self.assertNotEqual(response.status_code, 301)

    def test_feedback_send01(self):
        response = self.client.post('/feedback_send/', {'full_name': 'Jason Bond', 'email': 'Bond0007@gmail.com',
                                                        'feedback': 'Bond James Bond'})
        self.assertEqual(response.status_code, 200)

    def test_feedback_send02(self):
        response = self.client.post('/feedback_send/', {'full_name': 'Jason Bond', 'email': 'Bond0007@gmail.com',
                                                       'feedback': 'Bond James Bond'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_feedback_send03(self):
        response = self.client.post('/feedback_send/', {'full_name': 'Jason Bond', 'email': '<script>', 'feedback': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/404_error.html')

    def test_privacy_policy01(self):
        response = self.client.get('/privacy/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/privacy.html')

    def test_privacy_policy02(self):
        response = self.client.get('/privacy/', follow=True)
        content = response.content.decode('utf-8')
        self.assertTrue('script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js' in content)
        self.assertTrue('Our privacy policy' in content)
        self.assertTrue('We genuinely are here to help.' in content)

    def test_privacy_policy03(self):
        response = self.client.post('/privacy', follow=True)
        self.assertNotEqual(response.status_code, 301)

    def test_sign_in01(self):
        response = self.client.get('/signin/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/signin.html')

    def test_sign_in02(self):
        response = self.client.get('/signin/', follow=True)
        content = response.content.decode('utf-8')
        self.assertTrue('link href="/static/js/bootstrap.min.js' in content)
        self.assertTrue('Please sign in' in content)

    def test_sign_in03(self):
        response = self.client.post('/signin/', {'email': 'lshr9992@uni.sydney.edu.au', 'password': 'bb'})
        content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Please sign in' in content)

    def test_sign_up01(self):
        response = self.client.get('/signup/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/signup.html')

    def test_sign_up02(self):
        response = self.client.get('/signup', follow=True)
        content = response.content.decode('utf-8')
        self.assertTrue('link href="/static/js/bootstrap.min.js' in content)
        self.assertTrue('Please sign up here' in content)
        self.assertTrue('Select your status' in content)

    def test_sign_up03(self):
        response = self.client.post('/signup/', {'full_name': 'Jason Bond', 'email': 'Bond0007@gmail.com', 'password':
                                                 'bb', 're_password': 'bb', 'university': 'USYD', 'bday': '2000-2-2',
                                                 'dropdown': 'Student'}, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/profile/', {'email': 'Bond0007@gmail.com', 'password': 'bb'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/profile.html')

    def test_sign_up04(self):
        response = self.client.post('/signup/',
                                    {'full_name': 'Jason Bond', 'email': 'Bond0007@gmail.com', 'password': 'bb',
                                     're_password': 'not_bb', 'university': '<script>',  'bday': '2000-2-2', 'dropdown':
                                         'Student'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/signup.html')

    def test_profile01(self):
        response = self.client.get('/profile/1/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/signin.html')

    def test_profile02(self):
        response = self.client.get('/profile/3/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/signin.html')

    def test_profile03(self):
        response = self.client.get('/profile/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/signin.html')

    def test_profile04(self):
        response = self.client.post('/profile/', {'email': 'lshr9992@uni.sydney.edu.au', 'password': 'bb'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile05(self):
        response = self.client.post('/profile/', {'email': 'lshr9992@uni.sydney.edu.au', 'password': 'incorrect_pass'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/base.html')

    def test_profile06(self):
        response = self.client.post('/profile/', {}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/sign_in_not_succeed.html')
        content = response.content.decode('utf-8')
        self.assertTrue('link href="/static/js/bootstrap.min.js' in content)
        self.assertTrue('Sign in unsuccessful' in content)
        self.assertTrue('Incorrect Username or Password.' in content)

    def test_profile07(self):
        response = self.client.post('/signup/', {'full_name': 'Jason', 'email': '12345679@gmail.com', 'password':
                                                 'bb1', 're_password': 'bb1', 'university': 'USYD', 'bday': '2000-2-2',
                                                 'dropdown': 'Student'}, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/profile/', {'email': '12345679@gmail.com', 'password': 'bb1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_dashboard/profile.html')
        content = response.content.decode('utf-8')
        self.assertTrue('link href="/static/js/bootstrap.min.js' in content)
        self.assertTrue('Profile Information' in content)
        self.assertTrue('Welcome Jason' in content)

    def test_profile_image01(self):
        response = self.client.get('/profile_image/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_image02(self):
        response = self.client.post('/profile_image/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_image03(self):
        response = self.client.get('/profile_image/1/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_image04(self):
        response = self.client.post('/profile_image/1/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_image05(self):
        response = self.client.get('/profile_image/55/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_settings01(self):
        response = self.client.get('/settings/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_settings02(self):
        response = self.client.post('/settings/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_settings03(self):
        response = self.client.get('/settings/1/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_settings04(self):
        response = self.client.get('/settings/1/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_name01(self):
        response = self.client.get('/profile_edit_name/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_edit_name02(self):
        response = self.client.post('/profile_edit_name/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_edit_name03(self):
        response = self.client.get('/profile_edit_name/3/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_name04(self):
        response = self.client.get('/profile_edit_name/32/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_password01(self):
        response = self.client.get('/profile_edit_password/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_edit_password02(self):
        response = self.client.post('/profile_edit_password/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_edit_password03(self):
        response = self.client.get('/profile_edit_password/3/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_password04(self):
        response = self.client.get('/profile_edit_password/32/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_email01(self):
        response = self.client.get('/profile_edit_email/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_edit_email02(self):
        response = self.client.post('/profile_edit_email/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_edit_email03(self):
        response = self.client.get('/profile_edit_email/3/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_email04(self):
        response = self.client.get('/profile_edit_email/32/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_status01(self):
        response = self.client.get('/profile_edit_status/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_edit_status02(self):
        response = self.client.post('/profile_edit_status/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_profile_edit_status03(self):
        response = self.client.get('/profile_edit_status/3/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_status04(self):
        response = self.client.get('/profile_edit_status/32/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_deactivate_account01(self):
        response = self.client.get('/deactivate_account/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_deactivate_account02(self):
        response = self.client.post('/deactivate_account/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_deactivate_account03(self):
        self.client.post('/signup/', {'full_name': 'Jason', 'email': '12345679@gmail.com', 'password':
                                       'bb1', 're_password': 'bb1', 'university': 'USYD', 'bday': '2000-2-2',
                                        'dropdown': 'Student'}, follow=True)
        user = Users.objects.get(full_name='Jason')
        id = user.user_id
        resp = self.client.post(reverse('deactivate_account', kwargs={'pk': id}))
        self.assertEqual(resp.status_code, 200)

    def test_deactivate_account04(self):
        try:
            response = self.client.post('/deactivate_account/32/', follow=True)
        except:
            self.assertRaises(Users.DoesNotExist)

    def test_deactivate_account05(self):
        response = self.client.post('/deactivate_account/dsafas/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_uni_homepage01(self):
        response = self.client.get('/uni_homepage/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_uni_homepage02(self):
        response = self.client.post('/uni_homepage/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_uni_homepage03(self):
        try:
            response = self.client.get('/uni_homepage/3/', follow=True)
        except:
            self.assertRaises(Universities.DoesNotExist)

    def test_uni_homepage04(self):
        try:
            response = self.client.get('/uni_homepage/32/', follow=True)
        except:
            self.assertRaises(Universities.DoesNotExist)

    def test_uni_homepage05(self):
        Universities.objects.create(uni_name="The University Of Sydney", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of Sydney")
        id = uni.uni_id
        response = self.client.post(reverse('uni_homepage', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)

    def test_uni_homepage06(self):
        Universities.objects.create(uni_name="The University Of NSW", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of NSW")
        id = uni.uni_id
        response = self.client.post(reverse('uni_homepage', kwargs={'pk': id}))
        content = response.content.decode('utf-8')
        self.assertTrue('This is The University Of NSW reviews page' in content)

    def test_uni_images01(self):
        response = self.client.get('/uni_images/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_uni_images02(self):
        response = self.client.post('/uni_images/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_uni_images03(self):
        try:
            response = self.client.get('/uni_images/222', follow=True)
        except:
            self.assertRaises(Uniimage.DoesNotExist)

    def test_uni_images04(self):
        Universities.objects.create(uni_name="The University Of NSW", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of NSW")
        id = uni.uni_id
        response = self.client.post(reverse('uni_images', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)

    def test_uni_images05(self):
        Universities.objects.create(uni_name="The University Of NSW", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of NSW")
        id = uni.uni_id
        response = self.client.post(reverse('uni_images', kwargs={'pk': id}))
        content = response.content.decode('utf-8')
        self.assertTrue('The University Of NSW Photo Gallery' in content)

    def test_uni_unit_of_study01(self):
        response = self.client.get('/uni_unit_of_study/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_uni_unit_of_study02(self):
        response = self.client.post('/uni_unit_of_study/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_uni_unit_of_study03(self):
        try:
            response = self.client.get('/uni_unit_of_study/222', follow=True)
        except:
            self.assertRaises(Unitofstudy.DoesNotExist)

    def test_uni_unit_of_study04(self):
        Universities.objects.create(uni_name="The University Of NSW", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of NSW")
        id = uni.uni_id
        response = self.client.post(reverse('uni_unit_of_study', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)

    def test_uni_unit_of_study05(self):
        Universities.objects.create(uni_name="The University Of Sydney", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of Sydney")
        Unitofstudy.objects.create(uni=uni, unit_name="ELEC3609", ratings=5)
        id = uni.uni_id
        response = self.client.post(reverse('uni_unit_of_study', kwargs={'pk': id}))
        content = response.content.decode('utf-8')
        self.assertTrue('This is The University Of Sydney Unit of Study page' in content)
        self.assertTrue('ELEC3609' in content)

    def test_uos_experience01(self):
        response = self.client.get('/uos_experience/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_uos_experience02(self):
        response = self.client.post('/uos_experience/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_uos_experience03(self):
        try:
            response = self.client.get('/uos_experience/222', follow=True)
        except:
            self.assertRaises(Unitofstudy.DoesNotExist)

    def test_uos_experience04(self):
        Universities.objects.create(uni_name="The University Of Sydney", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of Sydney")
        Unitofstudy.objects.create(uni=uni, unit_name="ELEC3609", ratings=5)
        Users.objects.create(email="user1@gmail.com", full_name="First User", university_studies="First Uni",
                             dob='2000-10-11', passwords='first password', status='Student')
        user= Users.objects.get(email= "user1@gmail.com" )
        uos= Unitofstudy.objects.get(unit_name='ELEC3609')
        Experience.objects.create(user=user, uos=uos, experience="Great Exprience")
        pk= uos.uos_id
        response = self.client.post(reverse('uos_experience', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        self.assertTrue('This is ELEC3609' in content)
        self.assertTrue('Rate This UOS' in content)

    def test_uos_experience05(self):
        Universities.objects.create(uni_name="The University Of Sydney", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of Sydney")
        Unitofstudy.objects.create(uni=uni, unit_name="ELEC3609", ratings=5)
        Users.objects.create(email="user1@gmail.com", full_name="First User", university_studies="First Uni",
                             dob='2000-10-11', passwords='first password', status='Student')
        user= Users.objects.get(email= "user1@gmail.com" )
        uos= Unitofstudy.objects.get(unit_name='ELEC3609')
        Experience.objects.create(user=user, uos=uos, experience="Great Experience")
        pk= uos.uos_id
        response = self.client.post(reverse('uos_experience', kwargs={'pk': pk}))
        content = response.content.decode('utf-8')
        self.assertTrue('This is ELEC3609' in content)
        self.assertTrue('Rate This UOS' in content)

    def test_post_comments_on_reviews01(self):
        response = self.client.get('/post_comments_on_reviews/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_post_comments_on_reviews02(self):
        response = self.client.post('/post_comments_on_reviews/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_post_comments_on_reviews03(self):
        try:
            response = self.client.get('/post_comments_on_reviews/222', follow=True)
        except:
            self.assertRaises(Comments.DoesNotExist)

    def test_post_comments_on_reviews04(self):
        Universities.objects.create(uni_name="The University Of Sydney", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of Sydney")
        Users.objects.create(email="user1@gmail.com", full_name="First User", university_studies="First Uni",
                             dob='2000-10-11', passwords='first password', status='Student')
        user = Users.objects.get(email="user1@gmail.com")
        Reviews.objects.create(uni=uni, user=user, reviews='Great University')
        review = Reviews.objects.get(reviews='Great University')
        pk = review.reviews_id
        response = self.client.post(reverse('post_comments_on_reviews', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_comments_on_reviews05(self):
        Universities.objects.create(uni_name="The University Of Sydney", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of Sydney")
        Users.objects.create(email="user1@gmail.com", full_name="First User", university_studies="First Uni",
                             dob='2000-10-11', passwords='first password', status='Student')
        user = Users.objects.get(email="user1@gmail.com")
        Reviews.objects.create(uni=uni, user=user, reviews='Great University')
        review = Reviews.objects.get(reviews='Great University')
        Comments.objects.create(user=user, reviews=review, comments="Thanks for your review.")
        pk = review.reviews_id
        response = self.client.post(reverse('post_comments_on_reviews', kwargs={'pk': pk}))
        content = response.content.decode('utf-8')
        self.assertTrue('Great University' in content)
        self.assertTrue('Thanks for your review.' in content)

    def test_delete_review01(self):
        response = self.client.post('/delete_review/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_review02(self):
        try:
            response = self.client.get('/delete_review/', {'pk_uni': '3434', 'pk_reviews': '333'}, follow=True)
        except:
            self.assertRaises(Universities.DoesNotExist)

    def test_delete_review03(self):
        self.client.post('/signup/', {'full_name': 'Jason', 'email': '12345679@gmail.com', 'password':
                                                 'bb1', 're_password': 'bb1', 'university': 'USYD', 'bday': '2000-2-2',
                                                 'dropdown': 'Student'}, follow=True)
        self.client.post('/profile/', {'email': '12345679@gmail.com', 'password': 'bb1'})
        user = Users.objects.get(full_name='Jason')
        Universities.objects.create(uni_name="The University Of Sydney", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of Sydney")
        pk_uni = uni.uni_id
        Reviews.objects.create(uni=uni, user=user, reviews='Great University')
        review = Reviews.objects.get(reviews='Great University')
        pk_reviews = review.reviews_id

        response = self.client.post('/delete_review/', {'pk_uni': pk_uni, 'pk_reviews': pk_reviews})
        self.assertEqual(response.status_code, 200)
        try:
            review = Reviews.objects.get(reviews='Great University')
        except:
            self.assertRaises(Reviews.DoesNotExist)

    def test_delete_comment01(self):
        response = self.client.post('/delete_comment/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_comment02(self):
        try:
            response = self.client.get('/delete_review/', {'pk_comments': '3434', 'pk_reviews': '333'}, follow=True)
        except:
            self.assertRaises(Comments.DoesNotExist)

    def test_delete_comment03(self):
        self.client.post('/signup/', {'full_name': 'Jason', 'email': '12345679@gmail.com', 'password':
                                                 'bb1', 're_password': 'bb1', 'university': 'USYD', 'bday': '2000-2-2',
                                                 'dropdown': 'Student'}, follow=True)
        self.client.post('/profile/', {'email': '12345679@gmail.com', 'password': 'bb1'})
        user = Users.objects.get(full_name='Jason')
        Universities.objects.create(uni_name="The University Of Sydney", location='Sydney Australia', ratings=5)
        uni = Universities.objects.get(uni_name="The University Of Sydney")

        Reviews.objects.create(uni=uni, user=user, reviews='Great University')
        review = Reviews.objects.get(reviews='Great University')
        pk_reviews = review.reviews_id

        Comments.objects.create(reviews=review, user=user, comments="Just commenting")
        comment = Comments.objects.get(comments="Just commenting")
        pk_comments = comment.comments_id

        response = self.client.post('/delete_comment/', {'pk_comments': pk_comments, 'pk_reviews': pk_reviews})
        self.assertEqual(response.status_code, 200)

        try:
            review = Comments.objects.get(reviews="Just commenting")
        except:
            self.assertRaises(Comments.DoesNotExist)
















































