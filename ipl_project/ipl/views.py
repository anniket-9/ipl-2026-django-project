from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import Match, Team, Player, Comment
from .forms import CommentForm, ShareMatchForm


def match_list(request):
    """View all IPL matches with pagination - 5 per page."""
    all_matches = Match.objects.select_related('team1', 'team2').all()

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        all_matches = all_matches.filter(status=status_filter)

    paginator = Paginator(all_matches, getattr(settings, 'MATCHES_PER_PAGE', 5))
    page = request.GET.get('page')

    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)

    context = {
        'matches': matches,
        'status_filter': status_filter,
        'total_matches': all_matches.count(),
    }
    return render(request, 'ipl/match_list.html', context)


def match_detail(request, slug):
    """Single match detail with comments."""
    match = get_object_or_404(Match, slug=slug)
    active_comments = match.comments.filter(active=True)
    comment_form = CommentForm()

    context = {
        'match': match,
        'comments': active_comments,
        'comment_form': comment_form,
        'comment_count': active_comments.count(),
    }
    return render(request, 'ipl/match_detail.html', context)


def add_comment(request, slug):
    """Add a comment to a match."""
    match = get_object_or_404(Match, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.match = match
            comment.save()
            messages.success(request, 'Your comment has been posted successfully!')
            return redirect('match_detail', slug=match.slug)
        else:
            active_comments = match.comments.filter(active=True)
            context = {
                'match': match,
                'comments': active_comments,
                'comment_form': form,
                'comment_count': active_comments.count(),
            }
            return render(request, 'ipl/match_detail.html', context)

    return redirect('match_detail', slug=slug)


def share_match(request, slug):
    """Share match details via email."""
    match = get_object_or_404(Match, slug=slug)

    if request.method == 'POST':
        form = ShareMatchForm(request.POST)
        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            your_email = form.cleaned_data['your_email']
            friend_email = form.cleaned_data['friend_email']
            user_message = form.cleaned_data.get('message', '')

            subject = f"{your_name} wants to share a match with you: {match.title}"

            match_url = request.build_absolute_uri(match.get_absolute_url())

            email_body = f"""
Hi there!

{your_name} ({your_email}) thought you'd be interested in this IPL 2026 match:

🏏 {match.title}
📅 Date: {match.match_date.strftime('%d %B %Y, %I:%M %p IST')}
📍 Venue: {match.venue}
⚡ Status: {match.status}
"""
            if match.status == 'Completed' and match.result:
                email_body += f"🏆 Result: {match.result}\n"

            if user_message:
                email_body += f"\nPersonal Message from {your_name}:\n{user_message}\n"

            email_body += f"\nCheck out the full match details here:\n{match_url}\n\n"
            email_body += "Enjoy IPL 2026! 🎉\n"

            try:
                send_mail(
                    subject=subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[friend_email],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    f'Match details successfully shared with {friend_email}!'
                )
            except Exception as e:
                messages.error(request, f'Failed to send email. Please try again.')

            return redirect('match_detail', slug=match.slug)
    else:
        form = ShareMatchForm()

    context = {
        'match': match,
        'form': form,
    }
    return render(request, 'ipl/share_match.html', context)


def team_list(request):
    """List all IPL teams."""
    teams = Team.objects.prefetch_related('players').all()
    context = {
        'teams': teams,
        'total_teams': teams.count(),
    }
    return render(request, 'ipl/team_list.html', context)


def team_detail(request, slug):
    """Team detail with players."""
    team = get_object_or_404(Team, slug=slug)
    players = team.players.all()
    context = {
        'team': team,
        'players': players,
    }
    return render(request, 'ipl/team_detail.html', context)


def player_list(request):
    """List players, optionally filtered by team."""
    teams = Team.objects.all()
    team_slug = request.GET.get('team', '')
    role_filter = request.GET.get('role', '')

    players = Player.objects.select_related('team').all()

    if team_slug:
        players = players.filter(team__slug=team_slug)
    if role_filter:
        players = players.filter(role=role_filter)

    paginator = Paginator(players, 10)
    page = request.GET.get('page')
    try:
        players_page = paginator.page(page)
    except PageNotAnInteger:
        players_page = paginator.page(1)
    except EmptyPage:
        players_page = paginator.page(paginator.num_pages)

    context = {
        'players': players_page,
        'teams': teams,
        'team_slug': team_slug,
        'role_filter': role_filter,
        'roles': ['Batsman', 'Bowler', 'All-rounder', 'Wicketkeeper'],
        'total_players': players.count(),
    }
    return render(request, 'ipl/player_list.html', context)
