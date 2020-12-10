from django.urls import reverse

from posts.models import Post, Comment

from posts.tests.post_test_base_case import PostBaseTestCase


class PostsFormTests(PostBaseTestCase):

    def test_new_post(self):
        form_data = {
            "text": "new_post_text",
            "group": self.group.id,
            "image": self.img1,
        }
        count = Post.objects.count()
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(count + 1, Post.objects.count())
        post = Post.objects.first()
        self.assertEqual(post.text, form_data["text"])
        self.assertEqual(post.group, self.group)
        self.assertEqual(post.image.size, self.img1.size)

    def test_post_edit(self):
        count = Post.objects.count()
        form_data = {
            "text": "edit text",
            "group": self.another_group.id,
            "image": self.img2,
        }
        response = self.authorized_client.post(
            reverse('post_edit', kwargs={"username": self.user.username,
                                         "post_id": self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(count, Post.objects.count())
        self.assertRedirects(response,
                             f"/{self.user.username}/{str(self.post.id)}/")
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.text, form_data["text"])
        self.assertEqual(post.group, self.another_group)
        self.assertEqual(post.image.size, self.img2.size)

    def test_add_comment(self):
        response_guest = self.guest_client.get(reverse('add_comment', kwargs={
            "username": self.user.username,
            "post_id": self.post.id
        }))
        self.assertEqual(response_guest.status_code, 302)
        form_data = {"text": "new comment"}
        response_auth = self.authorized_client.post(reverse(
            'add_comment', kwargs={
                "username": self.user.username,
                "post_id": self.post.id
            }),
            data=form_data,
            follow=True
        )
        self.assertEqual(Comment.objects.first().text, form_data['text'])
