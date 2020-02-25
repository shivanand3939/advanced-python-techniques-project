from collections import namedtuple
from enum import Enum

from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        # TODO: What instance variables will be useful for storing on the Query object?
        self.number = None
        self.start_date = None
        self.end_date = None
        self.return_object = None
        for key, value in kwargs.items():
            if key == 'number':
                self.number = value
            elif key == 'date':
                self.date = value
            elif key == 'start_date':
                self.start_date = value
            elif key == 'end_date':
                self.end_date = value
            elif key == 'return_object':
                self.return_object = value


    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """
        if self.end_date:
            date_search = self.DateSearch('between', [self.start_date, self.end_date])
        else:
            date_search = self.DateSearch('equals', [self.date])

        # TODO: Translate the query parameters into a QueryBuild.Selectors object
        return self.Selectors(date_search, self.number, None, self.return_object)

class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?
        self.date_search_between = DateSearch.between.value
        self.date_search_equals = DateSearch.equals.value

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors
        date_search = query[0]
        number = query[1]
        filter = query[2]
        return_object = query[3]
        if date_search[0] == self.date_search_equals:
            res = self.date_equals(self.db, date_search[1][0])
        else:
            res = self.date_between(self.db, date_search[1][0], date_search[1][1])
        return res[:number]


    def date_equals(self, db, date):
        return db.orbitdate_neo_mapping[date]


    def date_between(self, db, start_date, end_date):
        res = []
        for each in db.orbitdate_neo_mapping:
            if each >=start_date and each <= end_date:
                res.extend(db.orbitdate_neo_mapping[each])
        return res
