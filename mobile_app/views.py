import os
import re
import datetime

from django.shortcuts import render_to_response

from models import Beer
from saucer_api.saucer import Saucer

today = datetime.date.today()
today = datetime.date.today()
week = datetime.timedelta(weeks=1)
last = today - week
next = today + week

# Helper function for sorting weekly brews
def __weekly_brews__(query):
    return query.filter(date__gte=last).filter(date__lt=next).order_by("date")

#class BrewHandler(request):
    # FIXME: Better way to do this?
#    def type(self):
#        return None

#    if request.method == 'GET':
#        beers = __weekly_brews__(Beer.objects.filter(type=self.type())).order_by("name")
#        template_values = {'beers' : beers, 'type' : self.type()}

        # FIXME: This template sucks b/c it has 4 loops that are duplicates
#        return render_to_response('type.html', template_values)

#def CanHandler(BrewHandler):
#    def type(self):
#        return "Can"

#def CaskHandler(BrewHandler):
#    def type(self):
#        return "Cask"

#def DraftHandler(BrewHandler):
#    def type(self):
#        return "Draft"

#def BottleHandler(BrewHandler):
#    def type(self):
#        return "Bottle"

def Index(request):
    if request.method == 'GET':
        # Have to filter name afterwards b/c datastore requires the inequality
        # operators to have a order FIRST if there is going to be any order
        # clauses at all (see datastore docs)
        drafts = __weekly_brews__(Beer.objects.filter(type="Draft")).order_by("name")
        bottles = __weekly_brews__(Beer.objects.filter(type="Bottle")).order_by("name")
        cans = __weekly_brews__(Beer.objects.filter(type="Can")).order_by("name")
        casks = __weekly_brews__(Beer.objects.filter(type="Cask")).order_by("name")

        beers = {}
        beers['drafts'] = drafts
        beers['bottles'] = bottles
        beers['cans'] = cans
        beers['casks'] = casks

        template_values = {'beers' : beers}

        # FIXME: This template sucks b/c it has 4 loops that are duplicates
        return render_to_response('index.html', template_values)

def Update(request, start=None, fetch=None):
    if request.method == 'GET':
        ids = []
        ii = 0
        added = 0
        skip = 10
        saucer = Saucer()
        saucer.reset_stats()
        all_beers = saucer.getAllBeers()
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

            details = saucer.getBeerDetails(ids)
            num_details = len(details)
            if not num_details:
                break

            jj = 0
            for det in details:
                b = Beer(name=beers[jj]['name'], type=beers[jj]['type'],
                            style=det['Style:'], descr=det['Description:'])
                b.save()
                jj += 1

            added += num_details
            ii += skip
            ids = []

        template_values = {'fetch' : Saucer.fetch, 'san' : Saucer.san,
                            'details' : Saucer.create_details, 'added' : added,
                            'start' : start, 'requested' : fetch}
        return render_to_response('update.html', template_values)

def BrewDetail(request, br):
    if request.method == 'GET':
        try:
            beer = Beer.objects.get(beer)
        except models.DoesNotExist:
            beer = None

        template_values = {'beer' : beer}
        return render_to_response('beer_details.html', template_values)

def Search(request):
    if request.method == 'GET':
        if style is not None and len(style) > 0:

            # FIXME: Un-urlize the string
            style = re.sub(r'%20', ' ', style)
            style = re.sub(r'%28', '(', style)
            style = re.sub(r'%29', ')', style)

            # Find all the styles by creating a set from all beers b/c
            # app engine won't let us grab just this column from a table
            beers = __weekly_brews__(Beer.objects.filter(style=style)).order_by("name")

            template_values = {'beers' : beers, 'search' : style}
            return render_to_response('beers.html', template_values)

        # Use a list to preserve ordering
        styles = []
        tmp = __weekly_brews__(Beer.all())

        for beer in tmp:
            styles.append(beer.style)

        styles = list(set(styles))
        styles.sort()
        template_values = {'styles' : styles}
        return render_to_response('search.html', template_values)

    else:
        name = request.get('name')

        if name is None or not len(name):
            self.redirect("/search")
            return
        beers = __weekly_brews__(Beer.all().filter("name = ", name))

        template_values = {'beers' : beers}
        return render_to_response('beers.html', template_values)
