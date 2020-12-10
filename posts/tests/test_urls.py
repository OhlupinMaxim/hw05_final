from django.core.cache import cache
from django.test import TestCase, Client

from posts.tests.post_test_base_case import PostBaseTestCase


class StaticURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_author(self):
        response = self.guest_client.get("/about-author")
        self.assertEqual(response.status_code, 301)

    def test_about_technology(self):
        response = self.guest_client.get("/about-technology")
        self.assertEqual(response.status_code, 301)

    def test_page_not_found(self):
        response = self.guest_client.get("/404")
        self.assertEqual(response.status_code, 301)

    def test_page_server_error(self):
        response = self.guest_client.get("/500")
        self.assertEqual(response.status_code, 301)


class PostsURLTests(PostBaseTestCase):

    def test_urls_anonymous_user(self):
        cache.clear()
        guest_client = PostsURLTests.guest_client
        urls = PostsURLTests.urls
        for template, reverse_name in urls.items():
            with self.subTest():
                response = guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_urls_user(self):
        cache.clear()
        auth_client = PostsURLTests.authorized_client
        urls = PostsURLTests.urls_auth
        for template, reverse_name in urls.items():
            with self.subTest():
                response = auth_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_url_guest_redirect(self):
        guest_client = self.guest_client
        urls = (f"/{self.user.username}/",
                f"/{self.user.username}/{str(self.post.pk)}/")
        for url in urls:
            with self.subTest():
                response_status = guest_client.get(url).status_code
                self.assertEqual(response_status, 200)

    def test_url_another_author_user(self):
        another_auth_user = self.another_auth_user
        url = f"/{self.user.username}/{str(self.post.pk)}/edit"
        response_status = another_auth_user.get(url).status_code
        self.assertEqual(response_status, 301)
