from django.conf import settings
import django.core.validators

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('slug', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message='Слаг содержит недопустимые символы.', regex='^[-a-zA-Z0-9_]+$')], verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('slug', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message='Слаг содержит недопустимые символы.', regex='^[-a-zA-Z0-9_]+$')], verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('year', models.IntegerField(validators=[django.core.validators.MaxValueValidator(limit_value=2023, message='Год выпуска не может быть больше текущего года.')], verbose_name='Год выпуска')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='titles.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(related_name='genres', to='titles.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Тайтл',
                'verbose_name_plural': 'Тайтлы',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('score', models.IntegerField(choices=[(1, 'Один балл'), (2, 'Два балла'), (3, 'Три балла'), (4, 'Четыре балла'), (5, 'Пять баллов'), (6, 'Шесть баллов'), (7, 'Семь баллов'), (8, 'Восемь баллов'), (9, 'Девять баллов'), (10, 'Десять баллов')], verbose_name='Оценка пользователя')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titles_review', to='titles.title', verbose_name='Произведение(тайтл)')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='titles.review', verbose_name='Комментируемый отзыв')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
            options={
                'verbose_name': 'Тайтл',
                'verbose_name_plural': 'Тайтлы',
            },
        ),
    ]
