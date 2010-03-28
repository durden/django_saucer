"""Feeds"""

from django.contrib.syndication.feeds import Feed

from views import _weekly_beers


class BeerFeed(Feed):
    """Generic class for beer beeds"""

    # Standard templates
    title_template = "feeds/beer_title.html"
    description_template = "feeds/beer_description.html"

    # Standard RSS feed requirements
    link = "/"
    title = "Saucer Beers"
    description = "Saucer Beers"

class NewBeersFeed(BeerFeed):
    """Feed for new beers"""

    title = "New Beers"
    description = "New beers at Houston Flying Saucer"

    def items(self):
        """Return new beers"""
        return  _weekly_beers(avail=True).order_by('-type')

class RetiredBeersFeed(BeerFeed):
    """Feed for retired beers"""

    title = "Retired beers"
    description = "Retired beers at Houston Flying Saucer"

    def items(self):
        """Return retired beers"""
        return  _weekly_beers(avail=False).order_by('-type')
