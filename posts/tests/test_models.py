from posts.tests.post_test_base_case import PostBaseTestCase


class PostModelTest(PostBaseTestCase):

    def test_Post_get_str(self):
        """Тестируем модель Пост"""
        post = PostModelTest.post
        expected = post.text[:15]
        self.assertEqual(expected, str(post))

    def test_Group_get_str(self):
        """Тестируем модель Групп"""
        group = PostModelTest.group
        self.assertEqual(group.__str__(), str(group))
