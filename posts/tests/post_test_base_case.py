from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group, User


class PostBaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        user = User
        cls.user = user.objects.create_user(
            username='author',
            email='author@gmail.com',
        )
        cls.another_user = user.objects.create_user(
            username='another_author',
            email='another_author@gmail.com',
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.another_auth_user = Client()
        cls.another_auth_user.force_login(cls.another_user)

        Group.objects.create(
            title='group',
            slug='slug',
            description='description'
        )

        Group.objects.create(
            title='another_group',
            slug='another_slug',
            description='another_description',
        )

        Post.objects.create(
            text="text",
            pub_date='23.11.2020',
            author=User.objects.filter(username='author').first(),
            group=Group.objects.filter(slug="slug").first(),
        )

        Post.objects.create(
            text="text_another_author",
            pub_date='23.11.2020',
            author=User.objects.filter(username='another_author').first(),
            group=Group.objects.filter(slug="slug").first(),
        )
        cls.post = Post.objects.filter(text="text").first()
        cls.group = Group.objects.filter(slug='slug').first()
        cls.another_group = Group.objects.filter(slug='another_slug').first()

        cls.urls = {
            "index.html": reverse("index"),
            "group_list.html": reverse("group"),
            "group.html": reverse("group_slug", kwargs={"slug": "slug"}),
        }
        cls.urls_auth = {
            "index.html": reverse("index"),
            "group_list.html": reverse("group"),
            "group.html": reverse("group_slug",
                                  kwargs={"slug": cls.group.slug}),
            "new_post.html": reverse("new_post"),
            "profile.html": reverse("profile",
                                    kwargs={"username": cls.user.username}),
            "post.html": reverse("post", kwargs={"username": cls.user.username,
                                                 "post_id": cls.post.pk}),
            "post_edit.html": reverse("post_edit",
                                      kwargs={"username": cls.user.username,
                                              "post_id": cls.post.pk}),
        }
        cls.img1 = SimpleUploadedFile(name='test1.jpg',
                                      content=open('posts/tests/test1.jpg',
                                                   'rb').read(),
                                      content_type='image/jpeg')
        cls.img2 = SimpleUploadedFile(name='test2.jpg',
                                      content=open('posts/tests/test2.jpg',
                                                   'rb').read(),
                                      content_type='image/jpeg')
