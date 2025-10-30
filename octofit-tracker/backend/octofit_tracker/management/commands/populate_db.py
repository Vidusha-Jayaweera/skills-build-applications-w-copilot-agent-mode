from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from django.db import connection
from pymongo import MongoClient

from bson.objectid import ObjectId

# Define models if not already defined (for demonstration)
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users (super heroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': marvel},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password')
            user_objs.append(user)

        # Create Activities
        Activity.objects.create(name='Running', user='ironman', team='Marvel', duration=30)
        Activity.objects.create(name='Cycling', user='batman', team='DC', duration=45)
        Activity.objects.create(name='Swimming', user='spiderman', team='Marvel', duration=25)
        Activity.objects.create(name='Yoga', user='wonderwoman', team='DC', duration=40)

        # Create Leaderboard
        Leaderboard.objects.create(team='Marvel', points=100)
        Leaderboard.objects.create(team='DC', points=90)

        # Create Workouts
        Workout.objects.create(name='HIIT', description='High intensity interval training', difficulty='Hard')
        Workout.objects.create(name='Stretching', description='Full body stretching', difficulty='Easy')

        # Ensure unique index on email for users using PyMongo
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db['users'].create_index('email', unique=True)
        client.close()

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
