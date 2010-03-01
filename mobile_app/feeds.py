"""Feeds"""

from django.contrib.syndication.feeds import Feed

from views import _get_current_week, _weekly_beers


# Start/end of current week (for date-based feeds)
START_WEEK, END_WEEK = _get_current_week()


class BeerFeed(Feed):
    """Generic class for beer beeds"""

    # Standard templates
    title_template = "feeds/beer_title.html"
    description_template = "feeds/beer_description.html"

    # Standard RSS feed requirements
    link = "/"
    title = "Saucer Beers"
    description = "Saucer Beers"

    def items(self):
        """Return list of beers to show in feed"""
        pass

class NewBeersFeed(BeerFeed):
    """Feed for new beers"""

    title = "New Saucer beers for %s - %s" % (START_WEEK, END_WEEK)
    description = "New beers for week"

    def items(self):
        """Return new beers"""
        return  _weekly_beers(avail=True).order_by('-type')

class RetiredBeersFeed(BeerFeed):
    """Feed for retired beers"""

    title = "Retired Saucer beers for %s - %s" % (START_WEEK, END_WEEK)
    description = "Retired beers for week"

    def items(self):
        """Return retired beers"""
        return  _weekly_beers(avail=False).order_by('-type')
