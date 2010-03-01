"""Feeds"""

from django.contrib.syndication.feeds import Feed

from views import _get_current_week, _weekly_beers


class NewBeersFeed(Feed):
    """Feed for new beers"""

    title_template = "feeds/beer_title.html"
    description_template = "feeds/beer_description.html"

    start, end = _get_current_week()

    title = "New Saucer beers for %s - %s" % (start, end)
    link = "/"
    description = "Newest beers for week"

    def items(self):
        """Return new beers"""
        return  _weekly_beers(avail=True).order_by('-type')

class RetiredBeersFeed(Feed):
    """Feed for retired beers"""

    start, end = _get_current_week()

    title = "Retired Saucer beers for %s - %s" % (start, end)
    link = "/"
    description = "Retired beers for week"

    def items(self):
        """Return retired beers"""
        return  _weekly_beers(avail=False).order_by('-type')
