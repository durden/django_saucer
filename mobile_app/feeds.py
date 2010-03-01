"""Feeds"""

from views import _get_current_week, _new_weekly_beers

from django.contrib.syndication.feeds import Feed


class NewBeersFeed(Feed):
    """Feed for new beers"""

    start, end = _get_current_week()

    title = "New Saucer beers for %s - %s" % (start, end)
    link = "/"
    description = "Newest beers for week"

    def items(self):
        """Return new beers"""
        return  _new_weekly_beers().order_by('-type')
