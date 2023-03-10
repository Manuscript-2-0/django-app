import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.contrib.auth.models import User
import random
import string
import os


def upload_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return '{}/{}{}'.format(
        ''.join(random.choice(string.ascii_lowercase +
                              string.ascii_uppercase + string.digits) for i in range(7)),
        filename_base,
        filename_ext.lower()
    )


class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(self, username, email, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Каждому пользователю нужен понятный человеку уникальный идентификатор,
    # который мы можем использовать для предоставления User в пользовательском
    # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
    # повышения скорости поиска в дальнейшем.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # Так же мы нуждаемся в поле, с помощью которого будем иметь возможность
    # связаться с пользователем и идентифицировать его при входе в систему.
    # Поскольку адрес почты нам нужен в любом случае, мы также будем
    # использовать его для входы в систему, так как это наиболее
    # распространенная форма учетных данных на данный момент (ну еще телефон).
    email = models.EmailField(db_index=True, unique=True)

    # Когда пользователь более не желает пользоваться нашей системой, он может
    # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
    # нами данные очень ценны, и мы не хотим их удалять. Мы просто предложим
    # пользователям способ деактивировать учетку вместо ее полного удаления.
    # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
    # далее анализировать информацию.
    is_active = models.BooleanField(default=True)

    # Этот флаг определяет, кто может войти в административную часть нашего
    # сайта. Для большинства пользователей это флаг будет ложным.
    is_staff = models.BooleanField(default=False)

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.

    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s')),
            "username": self.username,
            "email": self.email,
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class EventType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    location = models.CharField(max_length=100, default='Almaty, Kazakhstan')
    location_url = models.URLField(blank=True, default='')
    description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    type = models.ForeignKey('EventType', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('EventTag', blank=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.type.name}): {self.start_date} - {self.end_date}'


class AgendaItem(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()

    def __str__(self):
        return f'{self.name} ({self.event.name})'


class EventTag(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to=upload_to, null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    TICKET_STATUSES = ['activated', 'pending', 'canceled']
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[(
        status, status) for status in TICKET_STATUSES], default='pending')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.event}'


class RequiredSkill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    leader = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='teams')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    required_skills = models.ManyToManyField(RequiredSkill, blank=True)

    def __str__(self) -> str:
        return self.name


class TeamMaterial(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=upload_to, null=True, blank=True)
    url = models.URLField(blank=True, default='')

    def __str__(self) -> str:
        return self.name


class ActionNotification(models.Model):
    JOIN_REQUEST = 'join_request'
    INVITE_REQUEST = 'invite_request'
    KICK = 'kick'
    MEMBER_LEFT = 'member_left'
    NOTIFICATION_TYPES = [
        (JOIN_REQUEST, JOIN_REQUEST), (INVITE_REQUEST, INVITE_REQUEST), (KICK, KICK), (MEMBER_LEFT, MEMBER_LEFT)]
    message = models.CharField(max_length=100)
    action_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES, default='join')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.message}'
