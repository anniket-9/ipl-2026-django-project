from django.contrib import admin
from .models import Team, Player, Match, Comment


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'home_ground']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'city']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'role', 'runs', 'wickets', 'matches_played']
    list_filter = ['team', 'role']
    search_fields = ['name']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['title', 'team1', 'team2', 'match_date', 'venue', 'status']
    list_filter = ['status', 'team1', 'team2']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'venue']
    date_hierarchy = 'match_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'match', 'created_date', 'active']
    list_filter = ['active', 'created_date']
    search_fields = ['name', 'email', 'comment']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Approve selected comments"
