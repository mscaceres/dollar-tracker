import collections
import datetime
import itertools
import logging
import dollar_tracker.persitence


log = logging.getLogger(__name__)


class PriceHistory:
    def __init__(self, name):
        self.name = name
        self._points = collections.defaultdict(lambda: collections.defaultdict(list))
        self._max_points = collections.OrderedDict()
        self._min_points = collections.OrderedDict()
        self._avg_points = collections.OrderedDict()

    def add_point(self, source, date, price):
        self._points[date][source].append(price)
        self._max_points[date] = max(price, self._max_points.get(date, price))
        self._min_points[date] = min(price, self._min_points.get(date, price))
        self.update_avg_value(date, price)

    def points_per_day(self, date):
        return sum(len(self._points[date][source])
                   for source in self._points[date])

    @property
    def max_points(self):
        return self._max_points.items()

    @property
    def min_points(self):
        return self._min_points.items()

    @property
    def avg_points(self):
        return self._avg_points.items()

    def update_avg_value(self, date, price):
        current_avg = self._avg_points.get(date, 0)
        self._avg_points[date] = current_avg + (price - current_avg) / self.points_per_day(date)

    def variation_btw(self, date_from, date_to):
        if self.are_btw_dates_valid(date_from, date_to):
            return ((self._avg_points[date_to] - self._avg_points[date_from]) / self._avg_points[date_from]) * 100

    def are_btw_dates_valid(self, date_from, date_to):
        return (len(self._avg_points) >= 2
                and date_from <= date_to
                and date_from in self._avg_points
                and date_to in self._avg_points
               )

class DollarHistory:

    def __init__(self):
        self.buy_prices = PriceHistory("Compra")
        self.sell_prices = PriceHistory("Venta")

    @classmethod
    def from_pickle(cls, path):
        return dollar_tracker.persitence.pickled_context(cls, path)

    def add_point(self, source, dollar_point):
        log.info("Adding point from {}: {}".format(source, dollar_point))
        self.buy_prices.add_point(source, dollar_point.date, dollar_point.buy_price)
        self.sell_prices.add_point(source, dollar_point.date, dollar_point.sell_price)
