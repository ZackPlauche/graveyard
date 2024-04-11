from django.test import TestCase
from .models import Testimonial


class TestimonialTestCase(TestCase):
    def setUp(self):
        Testimonial.objects.create(
            author_first_name = 'Jeff',
            author_last_name='Bezos',
            star_rating=5,
            heading='ZackHub is truly an amazing agency.',
            body='I\'ve loved working with ZackHub from day 1.',
        )

    def test_get_author_name(self):
        testimonial = Testimonial.objects.get(author_first_name='Jeff')
        self.assertEqual(testimonial.get_author_name(), 'Jeff Bezos')
    
    