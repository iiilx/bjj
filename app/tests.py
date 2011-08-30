from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from bjj.app.models import * 

class AnonTest(TestCase):
    fixtures = ['blah.json'] 

    def setUp(self):
        pass
    
    def test_cats_exist(self):
        c= Category.objects.get(name='Funny')
   
    def test_anon_urls(self):
        uris=['/','/latest', '/top-contributers', '/login', '/accounts/login/', '/admin/', '/sentry/login']    
        client = Client()
        for uri in uris:
            response = client.get(uri)
            self.failUnlessEqual(response.status_code, 200)

    def test_anon_add_post(self):
        """a get request to /add-post w/o authentication redirects to default login page"""
        client = Client()
        response = client.get('/add-post')
        self.failUnlessEqual(response.status_code, 302) 

    def test_anon_categories(self):
        cats = ['Funny','Gi-Matches','Highlights','Instructionals',
                'No-Gi-Matches','Pro-Fights','Questions','Wrestling']      
        client = Client()
        for cat in cats:
            response = client.get('/category/%s' % cat)
            self.failUnlessEqual(response.status_code, 200)

class AuthenticatedTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john2', 'lennon@thebeatles.com', 'abc')
        #p = UserProfile.objects.create(user=user,handle='johnny')
        self.client = Client()
        self.client.login(username='john2', password='abc')

    def test_handle_form(self):
        response = self.client.post('/set-handle', {'handle':'john2'}) 
        self.failUnlessEqual(response.status_code, 302) #redirects to home

    def test_profile(self):
        uris=['/add-post', '/edit-profile']
        p = UserProfile.objects.create(user=self.user, handle='john2')
        for uri in uris:
            response = self.client.get(uri)
            self.failUnlessEqual(response.status_code, 200)

    def tearDown(self):
        self.user.delete()
