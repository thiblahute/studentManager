from binascii import b2a_base64
from datetime import datetime
from django.core import serializers
from django.test import TestCase
from django.utils.functional import curry
from django_restapi.authentication import HttpDigestAuthentication
from django_restapi_tests.examples.authentication import digest_authfunc
from django_restapi_tests.polls.models import Poll
import webbrowser, re

DIGEST_AUTH = 'Digest username="%(username)s", realm="%(realm)s", nonce="%(nonce)s", uri="%(fullpath)s", algorithm=MD5, response="%(response)s", qop=%(qop)s, nc=%(nc)s, cnonce="%(cnonce)s"'

SHOW_ERRORS_IN_BROWSER = False

def show_in_browser(content):
    if SHOW_ERRORS_IN_BROWSER:
        f = open("/tmp/djangorest_error", "w")
        f.write(content)
        f.close()
        webbrowser.open_new("file:///tmp/djangorest_error")

class BasicTest(TestCase):

    fixtures = ['initial_data.json']
        
    def setUp(self):
        self.client.put = curry(self.client.post, REQUEST_METHOD='PUT')
        self.client.delete = curry(self.client.get, REQUEST_METHOD='DELETE')
    
    def test_basics(self):
        
        for format in ['xml', 'html']:
            
            # Get list of polls
            url = '/%s/polls/' % format
            
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, 200)
            self.failUnlessEqual(response.content.find('secret'), -1)
    
            # Get list of choices
            url = '/%s/choices/' % format
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, 200)
            
            # Second page of choices must exist.
            response = self.client.get(url, {'page' : 2})
            self.failUnlessEqual(response.status_code, 200)
                    
            # Third page must not exist.
            response = self.client.get(url, {'page' : 3})
            self.failUnlessEqual(response.status_code, 404)
                    
            # Try to create poll with insufficient data
            # (needs to fail)
            url = '/%s/polls/' % format
            params = {
                'question' : 'Does this not work?',
            }
            response = self.client.post(url, params)
            self.failUnlessEqual(response.status_code, 400)
            
            # Create poll
            params = {
                'question' : 'Does this work?',
                'password' : 'secret',
                'pub_date' : '2001-01-01'
            }
            response = self.client.post(url, params)
            self.failUnlessEqual(response.status_code, 201)
            location = response['Location']
            poll_id = int(re.findall("\d+", location)[0])
            
            # Try to change poll with inappropriate data
            # (needs to fail)
            url = '/%s/polls/%d/' % (format, poll_id)
            params = {
                'question' : 'Yes, it works.',
                'password' : 'newsecret',
                'pub_date' : '2007-07-07-123'
            }
            response = self.client.put(url, params)
            self.failUnlessEqual(response.status_code, 400)
                
            # Change poll
            url = '/%s/polls/%d/' % (format, poll_id)
            params = {
                'question' : 'Yes, it works.',
                'password' : 'newsecret',
                'pub_date' : '2007-07-07'
            }
            response = self.client.put(url, params)
            self.failUnlessEqual(response.status_code, 200)
            
            # Read poll
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, 200)
            self.failUnlessEqual(response.content.find('secret'), -1)
            
            # Delete poll
            response = self.client.delete(url)
            self.failUnlessEqual(response.status_code, 200)
            
            # Read choice
            url = '/%s/choices/1/' % format
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, 200)
            
            # Try to delete choice (must fail)
            response = self.client.delete(url)
            self.failUnlessEqual(response.status_code, 405)
        
    def test_urlpatterns(self):
        url = '/json/polls/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content.find('secret'), -1)
        
        # Get poll
        url = '/json/polls/1/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content.find('secret'), -1)
    
        # Get filtered list of choices
        url = '/json/polls/1/choices/'
        response = self.client.get(url)
        self.failUnlessEqual(len(eval(response.content)), 3)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content.find('secret'), -1)
    
        # Get choice
        url = '/json/polls/1/choices/1/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content.find('secret'), -1)
        
        # Get choice (failure)
        url = '/json/polls/1/choices/12/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 404)
        self.failUnlessEqual(response.content.find('secret'), -1)
        
        # Try to create poll with insufficient data
        # (needs to fail)
        url = '/json/polls/'
        params = {
            'question' : 'Does this not work?',
        }
        response = self.client.post(url, params)
        self.failUnlessEqual(response.status_code, 400)
        
        # Create choice
        url = '/json/polls/1/choices/'
        params = {
            'poll' : 1, # TODO: Should be taken from URL
            'choice' : 'New choice',
            'votes' : 0
        }
        response = self.client.post(url, params)
        self.failUnlessEqual(response.status_code, 201)
        location = response['location']
        poll_id = int(re.findall("\d+", location)[0])
        self.failUnlessEqual(poll_id, 1)
    
        # Try to update choice with insufficient data (needs to fail)
        url = location[17:]
        # strip the protocol head and base url:
        # only working with paths! (note: bad variable name choice!!!)
        params = {
            'poll' : poll_id,
            'choice' : 'New choice',
            'votes' : 'Should be an integer'
        }
        response = self.client.put(url, params)
        self.failUnlessEqual(response.status_code, 400)
        
        # Update choice
        params = {
            'poll' : poll_id,
            'choice' : 'New choice',
            'votes' : '712'
        }
        response = self.client.put(url, params)
        self.failIfEqual(response.content.find("712"), -1)
        self.failUnlessEqual(response.status_code, 200)
        
        # Delete choice
        response = self.client.delete(url)
        self.failUnlessEqual(response.status_code, 200)

    def test_submission(self):
        
        # XML
        url = '/fullxml/polls/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        
        #  Create
        new_poll = Poll(
            question = 'Does XML submission work?',
            password = 'secret',
            pub_date = datetime.now()
        )
        serialized_poll = serializers.serialize('xml', [new_poll])
        serialized_poll = serialized_poll.replace('pk="None"', 'pk="1"') # Is ignored, but needs to be an integer
        response = self.client.post(url, data=serialized_poll, content_type='application/xml')
        self.failUnlessEqual(response.status_code, 201)
        response_content = re.sub('pk="\d+"', 'pk="1"', response.content)
        self.failUnlessEqual(serialized_poll, response_content)
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.failIfEqual(response_content.find("XML submission"), -1)
        
        #  Update
        url = '/fullxml/polls/1/'
        updated_poll = Poll(
            question = 'New question',
            password = 'new_secret',
            pub_date = datetime.now()
        )
        serialized_poll = serializers.serialize('xml', [updated_poll])
        serialized_poll = serialized_poll.replace('pk="None"', 'pk="1"') # Is ignored, but needs to be an integer
        response = self.client.put(url, data=serialized_poll, content_type='application/xml')
        updated_poll = Poll.objects.get(id=1)
        self.failUnlessEqual(updated_poll.question, "New question")
        self.failUnlessEqual(updated_poll.password, "new_secret")
                
        # JSON
        url = '/fulljson/polls/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        
        #  Create
        new_poll = Poll(
            question = 'Does JSON submission work?',
            password = 'secret',
            pub_date = datetime.now()
        )
        serialized_poll = serializers.serialize('json', [new_poll])
        serialized_poll = serialized_poll.replace('"pk": null', '"pk": 1') # Is ignored, but needs to be an integer
        response = self.client.post(url, data=serialized_poll, content_type='application/json')
        self.failUnlessEqual(response.status_code, 201)
        response_content = re.sub('"pk": \d+,', '"pk": 1,', response.content)
        self.failUnlessEqual(serialized_poll, response_content)
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.failIfEqual(response_content.find("JSON submission"), -1)
        
        #  Update
        url = '/fulljson/polls/2/'
        updated_poll = Poll(
            question = 'Another question',
            password = 'another_secret',
            pub_date = datetime.now()
        )
        serialized_poll = serializers.serialize('json', [updated_poll])
        serialized_poll = serialized_poll.replace('"pk": "None"', '"pk": "1"') # Is ignored, but needs to be an integer
        response = self.client.put(url, data=serialized_poll, content_type='application/json')
        updated_poll = Poll.objects.get(id=2)
        self.failUnlessEqual(updated_poll.question, "Another question")
        self.failUnlessEqual(updated_poll.password, "another_secret")
        
class AuthenticationTest(TestCase):
    
    fixtures = ['initial_data.json']
    
    def get_digest_test_params(self, response, url, auth_helper):
        """
        Extract authentication variables from server response
        e.g. {'nonce': '477be2a405a439cdba5227be89ba0f76', 'qop': 'auth', 'realm': 'realm1', 'opaque': '67d958f952de6bd4c1a88686f1b8a896'}
        and add missing params (method, path, username, cnonce, nc).
        """
        www_auth_response = response['WWW-Authenticate']
        self.failUnlessEqual(www_auth_response[:7].lower(), 'digest ')
        auth_params = auth_helper.get_auth_dict(www_auth_response[7:])
        self.failUnlessEqual(len(auth_params), 4)
        auth_params.pop('opaque')
        auth_params.update({'http_method': 'GET', 'fullpath': url, 'username': 'john', 'cnonce': '12345678', 'nc': '00000001'})
        return auth_params
    
    def test_basic_authentication(self):
        # Basic authentication, no password
        url = '/basic/polls/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 401)
        
        # Basic authentication, wrong password
        headers = {
            'HTTP_AUTHORIZATION': 'Basic %s' % b2a_base64('rest:somepass')[:-1]
        }
        response = self.client.get(url, **headers)
        self.failUnlessEqual(response.status_code, 401)
    
        # Basic authentication, right password
        headers = {
            'HTTP_AUTHORIZATION': 'Basic %s' % b2a_base64('rest:rest')[:-1]
        }
        response = self.client.get(url, **headers)
        self.failUnlessEqual(response.status_code, 200)
    
    def test_digest_authentication(self):

        # 1) Digest authentication, no password
        url = '/digest/polls/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 401)
        self.failUnlessEqual(response.has_header('WWW-Authenticate'), True)
        
        # Set up an auth class in order to avoid duplicate
        # authentication code.
        auth_helper = HttpDigestAuthentication(authfunc=digest_authfunc, realm='realm1')
        
        # 2) Digest authentication, wrong response (=wrong password)
        auth_params = self.get_digest_test_params(response, url, auth_helper)
        auth_params['response'] = 'wrongresponse'
        headers = {
            'SCRIPT_NAME' : '',
            'HTTP_AUTHORIZATION': DIGEST_AUTH % auth_params
        }
        response = self.client.get(url, **headers)
        self.failUnlessEqual(response.status_code, 401)
        
        # 3) Digest authentication, right password
        auth_params = self.get_digest_test_params(response, url, auth_helper)
        response = auth_helper.get_auth_response(**auth_params)
        auth_params['response'] = response
        headers = {
            'SCRIPT_NAME' : '',
            'HTTP_AUTHORIZATION': DIGEST_AUTH % auth_params
        }
        response = self.client.get(url, **headers)
        self.failUnlessEqual(response.status_code, 200)
