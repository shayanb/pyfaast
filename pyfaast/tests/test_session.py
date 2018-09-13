import os
import vcr
import unittest
import pyfaast

from pyfaast.tests.utils import read_test_ini, FILE_DIR


my_vcr = vcr.VCR(
    cassette_library_dir=os.path.join(FILE_DIR, "vcr/session"),
    record_mode="new_episodes",
)


class TestSession(unittest.TestCase):

    def setUp(self):
        pass

    @my_vcr.use_cassette(filter_post_data_parameters=["pair",
                                                      "facebook_id",
                                                      "facebook_token"])
    def test_login(self):
        auth = read_test_ini()
        session = pyfaast.Session(pair = auth["pair"], facebook_id=auth["facebook_id"], facebook_token=auth["facebook_token"])
        self.assertEqual(session.profile.gender, "wemale") #fix this

    @my_vcr.use_cassette(filter_post_data_parameters=["facebook_id",
                                                      "facebook_token"])
    def test_nearby_users_empty(self):
        auth = read_test_ini()
        session = pyfaast.Session(facebook_token=auth["facebook_token"], facebook_id=auth["facebook_id"])
        self.assertEqual(len(list(session.nearby_users(limit=10))), 0)
