"""Views methods for saucer app"""

import re
import datetime

from django.shortcuts import render_to_response

from models import Beer
from saucer_api.saucer import Saucer

def __get_current_week():
    """Find start/end dates of current week, Monday - Sunday (inclusive) and
    return as tuple"""

    start = datetime.date.today()
    day = datetime.timedelta(days=1)

    while start.weekday() != 0:
        start -= day

    end = start + datetime.timedelta(days=6)
    return (start, end)

def type_handler(request, req_type):
    """Find all beers with serving type equal to 'req_type' and display"""

    if request.method == 'GET':
        beers = Beer.objects.filter(type=req_type, avail=True).order_by("name")
        template_values = {'beers' : beers, 'type' : req_type}
        return render_to_response('type.html', template_values)

def can(request):
    """Show all can beers"""
    return type_handler(request, "Can")

def cask(request):
    """Show all cask beers"""
    return type_handler(request, "Cask")

def draft(request):
    """Show all draft beers"""
    return type_handler(request, "Draft")

def bottle(request):
    """Show all bottle beers"""
    return type_handler(request, "Bottle")

def new(request):
    """Show all beers that were first available during current week"""

    if request.method == 'GET':
        start, end = __get_current_week()
        beers = Beer.objects.filter(date__range=(start, end),
                                    avail=True).order_by("name")

        template_values = {'beers' : beers, 'type' : 'New'}
        return render_to_response('type.html', template_values)

def retired(request):
    """Show all beers that were discontinued/retired during current week"""

    if request.method == 'GET':
        start, end = __get_current_week()
        beers = Beer.objects.filter(date__range=(start, end),
                                    avail=False).order_by("name")

        template_values = {'beers' : beers, 'type' : 'Retired'}
        return render_to_response('type.html', template_values)

def index(request):
    """Show all currently available beers sorted by serving type"""

    if request.method == 'GET':
        drafts = Beer.objects.filter(type="Draft", avail=True).order_by("name")
        btls = Beer.objects.filter(type="Bottle", avail=True).order_by("name")
        cans = Beer.objects.filter(type="Can", avail=True).order_by("name")
        casks = Beer.objects.filter(type="Cask", avail=True).order_by("name")

        beers = {}
        beers['drafts'] = drafts
        beers['bottles'] = btls
        beers['cans'] = cans
        beers['casks'] = casks

        template_values = {'beers' : beers}
        return render_to_response('index.html', template_values)

def retire(request):
    """Retire all beers currently available in our db and not saucer site"""

    if request.method == 'GET':
        saucer = Saucer()
        saucer_beers = saucer.get_all_beers()
        db_beers = Beer.objects.filter(avail=True)
        retired_beers = []

        for db_beer in db_beers:
            found = False
            for saucer_beer in saucer_beers:
                if saucer_beer['name'] == db_beer.name and\
                    saucer_beer['type'] == db_beer.type:
                    found = True
                    break

            if not found:
                db_beer.avail = False
                db_beer.save()
                retired_beers.append(db_beer)

        template_values = {'retired': retired_beers}
        return render_to_response('retire.html', template_values)

def update(request, start=None, fetch=None):
    """Update DB with beers from saucer site starting with index (start) and
    update no more than (fetch) number of beers"""

    if request.method == 'GET':
        ids = []
        ii = 0
        added = 0
        skip = 10
        saucer = Saucer()
        all_beers = saucer.get_all_beers()
        num_beers = len(all_beers)

        if fetch is not None:
            num_beers = int(fetch)

        if start is not None:
            ii = int(start)

        # Don't skip by more than requested
        if num_beers < skip:
            skip = num_beers

        while added < num_beers:
            beers = all_beers[ii:ii + skip]
            for beer in beers:
                ids.append(beer['id'])

            details = saucer.get_beer_details(ids)
            num_details = len(details)
            if not num_details:
                break

            jj = 0
            for det in details:
                _type = beers[jj]['type']
                _name = beers[jj]['name']

                # Maybe we don't find it
                try:
                    curr_beer = Beer.objects.filter(type=_type, name=_name)[0]
                except IndexError:
                    curr_beer = None

                # Beer already in db, but maybe it's newly available
                if curr_beer:
                    if not curr_beer.avail:
                        curr_beer.avail = True
                        curr_beer.date = datetime.date.today()
                        curr_beer.save()
                        added += 1
                else:
                    b = Beer(name=_name, type=_type, avail=True,
                                style=det['Style:'], descr=det['Description:'])
                    b.save()
                    added += 1
                jj += 1

            ii += skip
            ids = []

        template_values = {'fetch' : saucer.fetch, 'san' : saucer.san,
                            'details' : saucer.create_details, 'added' : added,
                            'start' : start, 'requested' : fetch}
        return render_to_response('update.html', template_values)

def brew_detail(request, req_beer):
    """Show detailed information about requested beer"""

    if request.method == 'GET':
        try:
            beer = Beer.objects.get(id=req_beer)
        except Beer.DoesNotExist:
            beer = None

        template_values = {'beer' : beer}
        return render_to_response('beer_details.html', template_values)

def search(request, style=None):
    """Search all available beers given style and/or beer name"""

    # Request is for a given style or list of all styles
    if request.method == 'GET':
        if style is not None and len(style) > 0:

            # Un-urlize the string
            style = re.sub(r'%20', ' ', style)
            style = re.sub(r'%28', '(', style)
            style = re.sub(r'%29', ')', style)

            # Find all styles by creating a set from all beers b/c can't find
            # way to bring back single column
            beers = Beer.objects.filter(style=style, avail=True).order_by("name")

            template_values = {'beers' : beers, 'search' : style}
            return render_to_response('beers.html', template_values)

        # Use list to preserve ordering
        styles = []
        tmp = Beer.objects.all()

        for beer in tmp:
            styles.append(beer.style)

        styles = list(set(styles))
        styles.sort()
        template_values = {'styles' : styles}
        return render_to_response('search.html', template_values)

    # Request is for given beer by name
    else:
        name = request.POST.get('name', None)
        beers = Beer.objects.filter(name=name)

        template_values = {'beers' : beers, 'requested' : name}
        return render_to_response('beers.html', template_values)
