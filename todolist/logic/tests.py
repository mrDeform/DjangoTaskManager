from django.test import TestCase
from .models import Task, ToDo, User


class ModelTest(TestCase):
    def test_model_user_task_todo(self):
        # create user
        user = User(username='root_test', email='root@mail.net', password='afgsdgnaeoijk')
        user.save()
        self.assertIsInstance(user, User)
        search = User.objects.filter(email='root@mail.net')
        self.assertTrue(search[0], user)

        # create task
        task = Task(title='Test for Task1',
                    task_description='Testing Model Task',
                    manager=User.objects.get(id=1),
                    deadline='2022-08-26',
                    is_complete=False)
        task.save()
        self.assertIsInstance(task, Task)

        # create to_do
        todo = ToDo(title='Test for Todo1',
                    todo_description='Testing Model Todo',
                    deadline='2022-08-26',
                    is_complete=False,
                    task=Task.objects.get(id=1),
                    responsible=User.objects.get(id=1))
        todo.save()
        self.assertIsInstance(todo, ToDo)

        # search object
        self.assertTrue(Task.objects.filter(task_description='Testing Model Task'))
        self.assertTrue(ToDo.objects.filter(title='Test for Todo1'))

        # deleted all objects
        search.delete()
        self.assertFalse(User.objects.filter(username='root_test'))
        self.assertFalse(Task.objects.filter(title='Test for Task1'))
        self.assertFalse(ToDo.objects.filter(title='Test for Todo1'))

