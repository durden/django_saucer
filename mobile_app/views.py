import os
import re
import datetime

from django.shortcuts import render_to_response

from models import Beer
from saucer_api.saucer import Saucer

def __getCurrentWeek():
    # Run from Monday - Sunday (Inclusive)
    start = datetime.date.today()
    day = datetime.timedelta(days=1)

    while start.weekday() != 0:
        start -= day

    end = start + datetime.timedelta(days=6)
    return (start, end)

def TypeHandler(request, type):
    if request.method == 'GET':
        beers = Beer.objects.filter(type=type, avail=True).order_by("name")
        template_values = {'beers' : beers, 'type' : type}
        return render_to_response('type.html', template_values)

def Can(request):
    return TypeHandler(request, "Can")

def Cask(request):
    return TypeHandler(request, "Cask")

def Draft(request):
    return TypeHandler(request, "Draft")

def Bottle(request):
    return TypeHandler(request, "Bottle")

def New(request):
    if request.method == 'GET':
        start, end = __getCurrentWeek()
        beers = Beer.objects.filter(date__range=(start, end),
                                    avail=True).order_by("name")

        template_values = {'beers' : beers, 'type' : 'New'}
        return render_to_response('type.html', template_values)

def Retired(request):
    x = 1
    if request.method == 'GET':
        start, end = __getCurrentWeek()
        beers = Beer.objects.filter(date__range=(start, end),
                                    avail=False).order_by("name")

        template_values = {'beers' : beers, 'type' : 'Retired'}
        return render_to_response('type.html', template_values)

def Index(request):
    if request.method == 'GET':
        drafts = Beer.objects.filter(type="Draft", avail=True).order_by("name")
        bottles = Beer.objects.filter(type="Bottle", avail=True).order_by("name")
        cans = Beer.objects.filter(type="Can", avail=True).order_by("name")
        casks = Beer.objects.filter(type="Cask", avail=True).order_by("name")

        beers = {}
        beers['drafts'] = drafts
        beers['bottles'] = bottles
        beers['cans'] = cans
        beers['casks'] = casks

        template_values = {'beers' : beers}

        # FIXME: This template sucks b/c it has 4 loops that are duplicates
        return render_to_response('index.html', template_values)

def Retire(request):
    # Get all beers from saucer site and compare them with currently available
    # beers from our db
    saucer = Saucer()
    saucer_beers = saucer.get_all_beers()
    db_beers = Beer.objects.filter(avail=True)
    retired = []

    for db_beer in db_beers:
        found = False
        # Look for db beer in list of dictionaries
        for saucer_beer in saucer_beers:
            if saucer_beer['name'] == db_beer.name and\
                saucer_beer['type'] == db_beer.type:
                found = True
                break

        if not found:
            db_beer.avail = False
            db_beer.save()
            retired.append(db_beer)

    template_values = {'retired': retired}
    return render_to_response('retire.html', template_values)

def Update(request, start=None, fetch=None):
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
                else:
                    b = Beer(name=_name, type=_type, avail=True,
                                style=det['Style:'], descr=det['Description:'])
                    b.save()
                jj += 1

            # FIXME: Incorrect counting now b/c we don't always add
            added += num_details
            ii += skip
            ids = []

        template_values = {'fetch' : saucer.fetch, 'san' : saucer.san,
                            'details' : saucer.create_details, 'added' : added,
                            'start' : start, 'requested' : fetch}
        return render_to_response('update.html', template_values)

def BrewDetail(request, b):
    if request.method == 'GET':
        try:
            beer = Beer.objects.get(id=b)
        except Beer.DoesNotExist:
            beer = None

        template_values = {'beer' : beer}
        return render_to_response('beer_details.html', template_values)

def Search(request, style=None):
    if request.method == 'GET':
        if style is not None and len(style) > 0:

            # FIXME: Un-urlize the string
            style = re.sub(r'%20', ' ', style)
            style = re.sub(r'%28', '(', style)
            style = re.sub(r'%29', ')', style)

            # Find all the styles by creating a set from all beers b/c
            # app engine won't let us grab just this column from a table
            beers = Beer.objects.filter(style=style, avail=True).order_by("name")

            template_values = {'beers' : beers, 'search' : style}
            return render_to_response('beers.html', template_values)

        # Use a list to preserve ordering
        styles = []
        tmp = Beer.objects.all()

        for beer in tmp:
            styles.append(beer.style)

        styles = list(set(styles))
        styles.sort()
        template_values = {'styles' : styles}
        return render_to_response('search.html', template_values)

    else:
        name = request.POST.get('name', None)

        #if name is None or not len(name):
        #    self.redirect("/search")
        #    return

        beers = Beer.objects.filter(name=name)

        template_values = {'beers' : beers, 'requested' : name}
        return render_to_response('beers.html', template_values)
