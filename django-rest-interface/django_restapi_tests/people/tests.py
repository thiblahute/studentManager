from django.test import TestCase
from django.utils.functional import curry

class GenericTest(TestCase):

    fixtures = ['initial_data.json']
        
    def setUp(self):
        self.client.put = curry(self.client.post, REQUEST_METHOD='PUT')
        self.client.delete = curry(self.client.get, REQUEST_METHOD='DELETE')
    
    def test_resource(self):
        url = '/friends/'
        response = self.client.post(url)
        self.failUnlessEqual(response.status_code, 405)
        response = self.client.put(url)
        self.failUnlessEqual(response.status_code, 405)
        response = self.client.delete(url)
        self.failUnlessEqual(response.status_code, 405)
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        
        url = '/friends/1-2/'
        response = self.client.post(url)
        self.failUnlessEqual(response.status_code, 405)
        response = self.client.put(url)
        self.failUnlessEqual(response.status_code, 405)
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.delete(url)
        self.failUnlessEqual(response.status_code, 302)

        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 404)