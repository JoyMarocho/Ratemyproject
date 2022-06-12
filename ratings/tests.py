from django.test import TestCase
from .models import Project, Rating

# Create your tests here.
class TestProjectClass(TestCase):
    def setUp(self):
        self.new_project = Project(title = 'rate_my_project', profile_photo = 'image.jpg', description = 'An application that allows users to rate their peers project', link='www.github.com/Ratemyproject')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_project,Project))


class TestRatingClass(TestCase):
    def setUp(self):
        self.new_rating = Rating(design = 8, usability = 9, content = 8)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_rating,Rating))

