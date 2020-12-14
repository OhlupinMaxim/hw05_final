import django
from django import forms
from django.core.cache import cache
from django.urls import reverse

from posts.models import Follow, Post, User, Group
from posts.tests.post_test_base_case import PostBaseTestCase


class PostsViewTests(PostBaseTestCase):

    def test_index_page_correct_context(self):
        cache.clear()
        response = self.guest_client.get(reverse('index'))
        paginator = response.context.get("paginator")
        self.assertEqual(type(paginator), django.core.paginator.Paginator)
        response = self.guest_client.get(reverse('group'))
        self.assertEqual(type(response.context.get("paginator")),
                         django.core.paginator.Paginator)

    def test_index_cache(self):
        response = self.guest_client.get(reverse('index'))
        context = response.context
        Post.objects.create(
            text="text NEW",
            pub_date='23.11.2020',
            author=User.objects.filter(username='another_author').first(),
            group=Group.objects.filter(slug="slug").first(),
        )
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(context, response.context)
        cache.clear()
        self.assertFalse(context == self.guest_client.get(
            reverse('index')).context)

    def test_group_page_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('group'))
        task_title_0 = response.context.get('groups')[1].title
        task_text_0 = response.context.get('groups')[1].description
        task_slug_0 = response.context.get('groups')[1].slug
        self.assertEqual(task_title_0, 'group')
        self.assertEqual(task_text_0, 'description')
        self.assertEqual(task_slug_0, 'slug')

    def test_group_slug_page_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('group_slug', kwargs={'slug': 'slug'})
        )
        self.assertEqual(response.context.get('group').title, 'group')
        self.assertEqual(response.context.get('group').
                         description, 'description')
        self.assertEqual(response.context.get('group').slug, 'slug')

    def test_new_post(self):
        response_guest = self.guest_client.get(reverse("new_post"))
        response_auth = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.CharField,
            'group': forms.ChoiceField,
            'image': forms.ImageField,
        }
        self.assertEqual(response_guest.status_code, 302)
        for val, expected in form_fields.items():
            with self.subTest(value=val):
                form_field = response_auth.context.get('form').fields.get(val)
                self.assertIsInstance(form_field, expected)

    def test_edit_post(self):
        response_guest = self.guest_client.get(
            reverse('post_edit', kwargs={
                "username": self.user.username,
                "post_id": self.post.id
            }))
        response_auth = self.authorized_client.get(
            reverse('post_edit', kwargs={
                "username": self.user.username,
                "post_id": self.post.id
            }))
        form_fields = {
            'text': forms.CharField,
            'group': forms.ChoiceField,
            'image': forms.ImageField,
        }
        self.assertEqual(response_guest.status_code, 302)
        for val, expected in form_fields.items():
            with self.subTest(value=val):
                form_field = response_auth.context.get('form').fields.get(val)
                self.assertIsInstance(form_field, expected)

    def test_follow(self):
        response_auth = self.authorized_client.get(
            reverse('profile_follow',
                    kwargs={
                        "username": self.another_user}))
        self.assertEqual(response_auth.status_code, 302)
        self.assertTrue(Follow.objects.filter(
            user=self.user, author=self.another_user).exists())
        response_auth = self.authorized_client.get(reverse('follow_index'))
        post = Post.objects.get(author=self.another_user)
        self.assertEqual(response_auth.context.get("post").first(),
                         post)
        response_auth = self.another_auth_user.get(reverse('follow_index'))
        self.assertEqual(response_auth.get("post"), None)
        response_guest = self.guest_client.get(
            reverse('profile_follow',
                    kwargs={
                        "username": self.another_user}))
        self.assertEqual(response_guest.status_code, 302)

    def test_unfollow(self):
        response_auth = self.authorized_client.get(
            reverse("profile_unfollow",
                    kwargs={
                        "username": self.another_user}))
        self.assertEqual(response_auth.status_code, 302)
        self.assertFalse(Follow.objects.filter(
            user=self.user, author=self.another_user).exists())
