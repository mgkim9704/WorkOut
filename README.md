# CS473-workout
team RED 

# Caution 
Our project root is work-out(django framework root)

# Settings
install git, python3, virtualenv-python3

you can easily run  

> (venv) $ pip install -r reqirements.txt   
> (venv) $ cd workout
> (venv) $ python manage.py makemigrations  
> (venv) $ python manage.py migrate  
> (venv) $ python manage.py collectstatic  
> (venv) $ python manage.py runserver  

then site will open on 127.0.0.1:8000  

# Urls Infomation
Url routing of our site can be check below.  
work-out/workout/wokrout/urls.py  
work-out/workout/main/urls.py  
work-out/workout/wouser/urls.py  
work-out/workout/sport/urls.py  
work-out/workout/match/urls.py  

# Our Main Logic
you can check almost code in   
> work-out/workout/match/views.py  

# ELO Rating
## Calculations
If Player A has a rating of R<sub>A</sub> and Player B a rating of R<sub>B</sub>, the exact formula for Player A's score is:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/51346e1c65f857c0025647173ae48ddac904adcb)

And Player B's score is:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/4b340e7d15e61ee7d90f428dcf7f4b3c049d89ff)

Supposing Player A was expected to score E<sub>A</sub> points but actually scored S<sub>A</sub> points. The formula for updating his/her rating is:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/09a11111b433582eccbb22c740486264549d1129)

Right now the K factor is found by the number of player multiplied by 42 as a constant. Working on custom K factors.

[reference here](https://github.com/HankMD/EloPy/blob/master/README.md)

## Implementation
we use open source.
[https://github.com/sublee/elo](https://github.com/sublee/elo)

[our source](https://github.com/choiking10/cs473-workout/blob/f179291e8f96f141b3462a7e42638b5480daef39/work-out/workout/match/views.py#L115-L135)
```
def win(self, sport, winner, loser, drawn=False):
    w_ability, l_ability = Ability.objects.get(user=winner, sport=sport), Ability.objects.get(user=loser, sport=sport)
    w_rating, l_rating = rate_1vs1(Rating(w_ability.rating), Rating(l_ability.rating), drawn)
    w_ability.rating = int(w_rating)
    l_ability.rating = int(l_rating)
    w_ability.save()
    l_ability.save()
```

# Database Schema

Database schema of our site can be check below.  

> work-out/workout/wouser/models.py  
> work-out/workout/sport/models.py  
> work-out/workout/match/models.py  


# Main Features

## Implement
- Request match and match conduct
- Manual match
- ELO rating system
- Evaluation and comment systems

## Future Work
- Auto matching


# Our github repository
## For TA please visit our another git repository!
 - [https://github.com/choiking10/cs473-workout](https://github.com/choiking10/cs473-workout)
 - [https://github.com/mgkim9704/WorkOut](https://github.com/mgkim9704/WorkOut)
