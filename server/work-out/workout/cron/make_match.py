#!/usr/bin/env python
import os
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workout.settings')

import django
from django.utils import timezone

django.setup()

from match.models import Match, RequestMatch


def main():
    req_matches = RequestMatch.objects.filter(status=RequestMatch.FINDING).order_by('location', 'sport')

    # group by location and sport
    req_list = [req for req in req_matches]
    groups = []
    tmp_groups = []
    for req in req_list:
        if len(tmp_groups) == 0 or (req.location == tmp_groups[0].location and req.sport == tmp_groups[0].sport):
            tmp_groups.append(req)
        else:
            groups.append(tmp_groups)
    groups.append(tmp_groups)
    candidate = []
    for group in groups:
        if len(group) < 1:
            continue
        sz = len(group)
        for i in range(sz):
            for j in range(i+1, sz):
                if group[i].user == group[j].user:
                    continue
                s1, e1 = group[i].from_to()
                s2, e2 = group[j].from_to()
                if s1 > s2:
                    s1, e1, s2, e2 = s2, e2, s1, e1

                if s1 > timezone.now() + timedelta(days=2):
                    continue
                if s2 < e1:
                    candidate.append((group[i], group[j], s1))

main()

