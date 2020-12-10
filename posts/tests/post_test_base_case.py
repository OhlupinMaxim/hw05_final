from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

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
            author=User.objects.get(username='author'),
            group=Group.objects.get(slug="slug"),
        )

        Post.objects.create(
            text="text_another_author",
            pub_date='23.11.2020',
            author=User.objects.get(username='another_author'),
            group=Group.objects.get(slug="slug"),
        )
        cls.post = Post.objects.get(id=1)
        cls.group = Group.objects.get(slug='slug')
        cls.another_group = Group.objects.get(slug='another_slug')

        cls.urls = {
            "index.html": "/",
            "group_list.html": "/group/",
            "group.html": "/group/slug/",
        }
        cls.urls_auth = {
            "index.html": "/",
            "group_list.html": "/group/",
            "group.html": "/group/slug/",
            "new_post.html": "/new/",
            "profile.html": f"/{cls.user.username}/",
            "post.html": f"/{cls.user.username}/{str(cls.post.pk)}/",
            "post_edit.html": f"/{cls.user.username}/{str(cls.post.pk)}/edit/",
        }
        cls.img1 = SimpleUploadedFile(name='test1.jpg',
                                      content=open('posts/tests/test1.jpg',
                                                   'rb').read(),
                                      content_type='image/jpeg')
        cls.img2 = SimpleUploadedFile(name='test2.jpg',
                                      content=open('posts/tests/test2.jpg',
                                                   'rb').read(),
                                      content_type='image/jpeg')
