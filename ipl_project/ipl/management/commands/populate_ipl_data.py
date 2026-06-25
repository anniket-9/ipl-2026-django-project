"""
Management command to populate the database with sample IPL 2026 data.
Run: python manage.py populate_ipl_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from ipl.models import Team, Player, Match


TEAMS_DATA = [
    {
        'name': 'Mumbai Indians',
        'city': 'Mumbai',
        'home_ground': 'Wankhede Stadium',
        'color': '#004C97',
        'description': 'The most successful franchise in IPL history with five championships. Known for their aggressive batting lineup and world-class fast bowlers.',
    },
    {
        'name': 'Chennai Super Kings',
        'city': 'Chennai',
        'home_ground': 'MA Chidambaram Stadium',
        'color': '#FDB913',
        'description': 'The most consistent team in IPL history led by MS Dhoni. Famous for their calm, calculated approach and never-say-die attitude.',
    },
    {
        'name': 'Royal Challengers Bangalore',
        'city': 'Bangalore',
        'home_ground': 'M. Chinnaswamy Stadium',
        'color': '#EC1C24',
        'description': 'Home to some of cricket\'s biggest stars and a passionate fan base. Known for explosive batting and a high-scoring ground.',
    },
    {
        'name': 'Kolkata Knight Riders',
        'city': 'Kolkata',
        'home_ground': 'Eden Gardens',
        'color': '#3A225D',
        'description': 'Two-time IPL champions known for their electric atmosphere and smart team management. Eden Gardens is one of cricket\'s great venues.',
    },
    {
        'name': 'Delhi Capitals',
        'city': 'Delhi',
        'home_ground': 'Arun Jaitley Stadium',
        'color': '#00008B',
        'description': 'A dynamic franchise with talented young Indian players and experienced internationals making a strong push for their first IPL title.',
    },
    {
        'name': 'Rajasthan Royals',
        'city': 'Jaipur',
        'home_ground': 'Sawai Mansingh Stadium',
        'color': '#FF69B4',
        'description': 'The inaugural IPL champions known for unearthing talent and playing smart cricket. Steeped in royal tradition and Pink City pride.',
    },
    {
        'name': 'Sunrisers Hyderabad',
        'city': 'Hyderabad',
        'home_ground': 'Rajiv Gandhi International Stadium',
        'color': '#FF822A',
        'description': 'Known for their powerful bowling attack and disciplined game plan. Former IPL champions with a fiercely loyal fan base.',
    },
    {
        'name': 'Punjab Kings',
        'city': 'Mohali',
        'home_ground': 'Punjab Cricket Association IS Bindra Stadium',
        'color': '#DD1F2D',
        'description': 'A franchise famous for big-hitting batsmen and dramatic finishes. Always competitive with world-class overseas stars.',
    },
    {
        'name': 'Gujarat Titans',
        'city': 'Ahmedabad',
        'home_ground': 'Narendra Modi Stadium',
        'color': '#1C1C1C',
        'description': 'The newest powerhouse in IPL, back-to-back finalists since inception. Home to the world\'s largest cricket stadium.',
    },
    {
        'name': 'Lucknow Super Giants',
        'city': 'Lucknow',
        'home_ground': 'BRSABV Ekana Cricket Stadium',
        'color': '#A0C4FF',
        'description': 'A franchise built around balanced team composition. Representing the passionate cricket culture of Uttar Pradesh.',
    },
]

PLAYER_ROLES = ['Batsman', 'Bowler', 'All-rounder', 'Wicketkeeper']

FAMOUS_PLAYERS = [
    ('Rohit Sharma', 'Mumbai Indians', 'Batsman', 650, 0, 14),
    ('Jasprit Bumrah', 'Mumbai Indians', 'Bowler', 45, 22, 14),
    ('Suryakumar Yadav', 'Mumbai Indians', 'Batsman', 580, 2, 14),
    ('Hardik Pandya', 'Mumbai Indians', 'All-rounder', 320, 15, 14),
    ('Ishan Kishan', 'Mumbai Indians', 'Wicketkeeper', 410, 0, 13),

    ('MS Dhoni', 'Chennai Super Kings', 'Wicketkeeper', 280, 0, 14),
    ('Ruturaj Gaikwad', 'Chennai Super Kings', 'Batsman', 720, 0, 14),
    ('Ravindra Jadeja', 'Chennai Super Kings', 'All-rounder', 340, 18, 14),
    ('Devon Conway', 'Chennai Super Kings', 'Batsman', 490, 0, 12),
    ('Deepak Chahar', 'Chennai Super Kings', 'Bowler', 60, 14, 13),

    ('Virat Kohli', 'Royal Challengers Bangalore', 'Batsman', 741, 0, 14),
    ('Faf du Plessis', 'Royal Challengers Bangalore', 'Batsman', 625, 0, 14),
    ('Glenn Maxwell', 'Royal Challengers Bangalore', 'All-rounder', 400, 8, 14),
    ('Mohammed Siraj', 'Royal Challengers Bangalore', 'Bowler', 30, 20, 14),

    ('Shreyas Iyer', 'Kolkata Knight Riders', 'Batsman', 540, 0, 14),
    ('Sunil Narine', 'Kolkata Knight Riders', 'All-rounder', 390, 16, 14),
    ('Andre Russell', 'Kolkata Knight Riders', 'All-rounder', 440, 12, 13),
    ('Varun Chakravarthy', 'Kolkata Knight Riders', 'Bowler', 20, 21, 14),

    ('David Warner', 'Delhi Capitals', 'Batsman', 560, 0, 14),
    ('Rishabh Pant', 'Delhi Capitals', 'Wicketkeeper', 480, 0, 14),
    ('Axar Patel', 'Delhi Capitals', 'All-rounder', 280, 14, 14),
    ('Anrich Nortje', 'Delhi Capitals', 'Bowler', 15, 19, 12),

    ('Sanju Samson', 'Rajasthan Royals', 'Wicketkeeper', 620, 0, 14),
    ('Jos Buttler', 'Rajasthan Royals', 'Batsman', 680, 0, 14),
    ('Yuzvendra Chahal', 'Rajasthan Royals', 'Bowler', 25, 24, 14),
    ('Trent Boult', 'Rajasthan Royals', 'Bowler', 18, 17, 13),

    ('Heinrich Klaasen', 'Sunrisers Hyderabad', 'Wicketkeeper', 510, 0, 14),
    ('Pat Cummins', 'Sunrisers Hyderabad', 'All-rounder', 240, 16, 14),
    ('Travis Head', 'Sunrisers Hyderabad', 'Batsman', 567, 0, 14),
    ('Bhuvneshwar Kumar', 'Sunrisers Hyderabad', 'Bowler', 40, 18, 14),

    ('Shikhar Dhawan', 'Punjab Kings', 'Batsman', 480, 0, 14),
    ('Sam Curran', 'Punjab Kings', 'All-rounder', 290, 12, 14),
    ('Kagiso Rabada', 'Punjab Kings', 'Bowler', 30, 22, 14),
    ('Liam Livingstone', 'Punjab Kings', 'All-rounder', 380, 7, 13),

    ('Shubman Gill', 'Gujarat Titans', 'Batsman', 695, 0, 14),
    ('Rashid Khan', 'Gujarat Titans', 'All-rounder', 180, 25, 14),
    ('Mohammed Shami', 'Gujarat Titans', 'Bowler', 20, 20, 14),
    ('Hardik Pandya', 'Gujarat Titans', 'All-rounder', 310, 14, 13),

    ('KL Rahul', 'Lucknow Super Giants', 'Wicketkeeper', 580, 0, 14),
    ('Quinton de Kock', 'Lucknow Super Giants', 'Batsman', 520, 0, 14),
    ('Krunal Pandya', 'Lucknow Super Giants', 'All-rounder', 250, 13, 14),
    ('Ravi Bishnoi', 'Lucknow Super Giants', 'Bowler', 22, 19, 14),
]


class Command(BaseCommand):
    help = 'Populate database with sample IPL 2026 data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        Match.objects.all().delete()
        Player.objects.all().delete()
        Team.objects.all().delete()

        self.stdout.write(self.style.WARNING('Creating teams...'))
        teams = {}
        for td in TEAMS_DATA:
            team = Team.objects.create(**td)
            teams[td['name']] = team
            self.stdout.write(f"  ✓ {team.name}")

        self.stdout.write(self.style.WARNING('Creating players...'))
        for name, team_name, role, runs, wickets, matches in FAMOUS_PLAYERS:
            if team_name in teams:
                Player.objects.create(
                    name=name,
                    team=teams[team_name],
                    role=role,
                    runs=runs,
                    wickets=wickets,
                    matches_played=matches,
                )
        
        # Add some additional generic players per team
        for team_name, team in teams.items():
            existing = team.players.count()
            for i in range(11 - existing):
                roles = PLAYER_ROLES
                role = roles[i % 4]
                Player.objects.create(
                    name=f"Player {i+1} ({team_name[:3]})",
                    team=team,
                    role=role,
                    runs=random.randint(50, 400),
                    wickets=random.randint(0, 15),
                    matches_played=random.randint(8, 14),
                )

        self.stdout.write(self.style.WARNING('Creating matches...'))
        team_list = list(teams.values())
        now = timezone.now()

        match_number = 1
        created_pairs = []

        statuses = ['Completed'] * 20 + ['Upcoming'] * 30 + ['Live'] * 2

        for i in range(len(team_list)):
            for j in range(i + 1, len(team_list)):
                t1 = team_list[i]
                t2 = team_list[j]
                
                days_offset = (match_number - 25) * 2
                match_date = now + timedelta(days=days_offset)
                
                if days_offset < -2:
                    status = 'Completed'
                elif days_offset <= 0:
                    status = 'Live'
                else:
                    status = 'Upcoming'

                result = ''
                if status == 'Completed':
                    winner = random.choice([t1, t2])
                    margin = random.choice(['6 wickets', '4 wickets', '23 runs', '11 runs', '7 wickets', '2 runs'])
                    result = f"{winner.name} won by {margin}"

                title = f"{t1.name} vs {t2.name} — Match {match_number}"
                
                venues = [
                    'Wankhede Stadium, Mumbai',
                    'MA Chidambaram Stadium, Chennai',
                    'M. Chinnaswamy Stadium, Bangalore',
                    'Eden Gardens, Kolkata',
                    'Narendra Modi Stadium, Ahmedabad',
                    'Sawai Mansingh Stadium, Jaipur',
                ]

                Match.objects.create(
                    title=title,
                    team1=t1,
                    team2=t2,
                    match_date=match_date,
                    venue=random.choice(venues),
                    result=result,
                    status=status,
                    match_number=match_number,
                )
                match_number += 1
                if match_number > 70:
                    break
            if match_number > 70:
                break

        self.stdout.write(self.style.SUCCESS(f'\n✅ Done! Created:'))
        self.stdout.write(f'   🏟 {Team.objects.count()} Teams')
        self.stdout.write(f'   👤 {Player.objects.count()} Players')
        self.stdout.write(f'   🏏 {Match.objects.count()} Matches')
        self.stdout.write(self.style.SUCCESS('\nRun: python manage.py runserver'))
