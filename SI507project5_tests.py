import unittest
from SI507project5_code import *

class Proj5_test_suite(unittest.TestCase):
    def setUp(self):
        sample_dict = {"Tumblr":"likes"}
        test_cache = {"TUMBLR/LIKES":"bogus"}
    def test_method_create_request_identifier(self):
        assertEqual(create_request_identifier(sample_dict),"TUMBLR/LIKES")
    def test_method_get_from_cache(self):
        assertEqual(get_from_cache("TUMBLR/LIKES",test_cache),"bogus")        
    def test_pytumblr_output(self):
        CLIENT_KEY = secret_data_tumblr.client_key 
        CLIENT_SECRET = secret_data_tumblr.client_secret 
        OAUTH_TOKEN = secret_data_tumblr.oauth_token
        OAUTH_SECRET = secret_data_tumblr.oauth_secret
        client = pytumblr.TumblrRestClient(CLIENT_KEY, CLIENT_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
        
        assertIs(type(client),dict)
    def test_method_set_in_data_cache(self):
        set_in_data_cache("TUMBLR/LIKES","some data",7)
        
    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
