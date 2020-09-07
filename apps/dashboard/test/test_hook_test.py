import os

from django.contrib.auth.models import User
from django.test import TestCase

from playexo.models import PLSession, Answer, PL

TEST_DATA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")


class ViewsTestCase(TestCase):

    def setUp(self) -> None:
        self.pl = PL.objects.create(name="random_add", data={})

        self.user = User.objects.create(username="user", password="password")
        self.plsession = PLSession.objects.create(pl=self.pl,seed=42)

    def tearDown(self) -> None:
        super().tearDown()

    def test_sandbox(self):
        a = Answer.objects.create(session=self.plsession, answer={"intro":"beurk"},seed=12, grade=77)
        self.assertIsNotNone(4)

