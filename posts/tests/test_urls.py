from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.tests.post_test_base_case import PostBaseTestCase


class PostsURLTests(PostBaseTestCase):

    def test_homepage(self):
        response = self.guest_client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_flat_pages(self):
        for url in self.static_pages:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 301, f'url: {url}')

    def test_page_not_found(self):
        response = self.guest_client.get(reverse("Error_404"))
        self.assertEqual(response.status_code, 404)

    def test_page_server_error(self):
        response = self.guest_client.get(reverse("Error_500"))
        self.assertEqual(response.status_code, 500)

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
        urls = (reverse("profile", kwargs={"username": self.user.username}),
                reverse("post",
                        kwargs={"username": self.user.username,
                                "post_id": self.post.id}))
        for url in urls:
            with self.subTest():
                response_status = guest_client.get(url).status_code
                self.assertEqual(response_status, 200)

    def test_url_another_author_user(self):
        another_auth_user = self.another_auth_user
        response_status = another_auth_user.get(
            reverse("post_edit",
                    kwargs={
                        "username": self.user.username,
                        "post_id": self.post.pk
                    })).status_code
        self.assertEqual(response_status, 302)
