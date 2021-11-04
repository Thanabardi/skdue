from django.test import TestCase
from skdue_calendar.utils import generate_slug, generate_tag


class GenerateSlugTests(TestCase):
    def test_generate_slug(self):
        """Test that generate_slug returns correct slug"""
        names = ["event 1", "EvnTR 2", "evBMr 3 AND 5", 
                "caLendar 1", "CaleENDAR TWO", "calendar 3 and 4"]
        expects = ["event-1", "EvnTR-2", "evBMr-3-AND-5", 
                "caLendar-1", "CaleENDAR-TWO", "calendar-3-and-4"]
        for name, expect in zip(names, expects):
            with self.subTest():
                self.assertEqual(expect, generate_slug(name))

    def test_generate_slug_with_special_char(self):
        names = ["@123's test", "test's-file@%  "]
        expects = ["123s-test", "tests-file"]
        for name, expect in zip(names, expects):
            with self.subTest():
                self.assertEqual(expect, generate_slug(name))

class GenerateTagTests(TestCase):
    def test_generate_tag(self):
        """Test that generate_tag returns correct tag"""
        tags = ["event 1", "EvnTR 2", "evBMr 3 AND 5", 
                "caLendar 1", "CaleENDAR TWO", "calendar 3 and 4"]
        expects = ["event1", "evntr2", "evbmr3and5", 
                "calendar1", "caleendartwo", "calendar3and4"]
        for tag, expect in zip(tags, expects):
            with self.subTest():
                self.assertEqual(expect, generate_tag(tag))

    def test_generate_tag_with_special_char(self):
        tags = ["@123's test", "test's-file@%  "]
        expects = ["123stest", "testsfile"]
        for tag, expect in zip(tags, expects):
            with self.subTest():
                self.assertEqual(expect, generate_tag(tag))