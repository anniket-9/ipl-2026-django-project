from django.db import models
from django.utils.text import slugify


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    home_ground = models.CharField(max_length=150, blank=True)
    color = models.CharField(max_length=7, default='#1a1a2e', help_text='Hex color code for team')

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('team_detail', kwargs={'slug': self.slug})


class Player(models.Model):
    ROLE_CHOICES = [
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All-rounder', 'All-rounder'),
        ('Wicketkeeper', 'Wicketkeeper'),
    ]

    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    nationality = models.CharField(max_length=50, blank=True, default='Indian')
    photo = models.ImageField(upload_to='players/', blank=True, null=True)

    class Meta:
        ordering = ['-runs']

    def __str__(self):
        return f"{self.name} ({self.team.name})"


class Match(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Completed', 'Completed'),
        ('Live', 'Live'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    match_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    result = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Upcoming')
    match_number = models.IntegerField(default=1)

    class Meta:
        ordering = ['-match_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while Match.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('match_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"Comment by {self.name} on {self.match.title}"
