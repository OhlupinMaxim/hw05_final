import io

from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, modify_settings
from django.urls import reverse

from PIL import Image

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
        buf = io.BytesIO()
        imageBytes = Image.new("RGB", (100, 100),
                               (205, 205, 205)).save(buf, format="jpeg")
        cls.img1 = SimpleUploadedFile(name='test1.jpg',
                                      content=buf.getvalue(),
                                      content_type='image/jpeg')
        buf = io.BytesIO()
        imageBytes = Image.new("RGB", (10, 10),
                               (255, 255, 255)).save(buf, format="jpeg")
        cls.img2 = SimpleUploadedFile(name='test2.jpg',
                                      content=buf.getvalue(),
                                      content_type='image/jpeg')

        cls.flat_about = FlatPage.objects.create(
            url='about-author/',
            title='about',
            content='<b>content</b>'
        )
        cls.flat_tech = FlatPage.objects.create(
            url='about-technology/',
            title='terms',
            content='<b>content</b>'
        )
        site = Site.objects.get(pk=1)
        cls.flat_about.sites.add(site)
        cls.flat_tech.sites.add(site)
        cls.static_pages = ('/about-author', '/about-technology')
