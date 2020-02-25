from enum import Enum
from exceptions import UnsupportedFeature
import pandas as pd
from models import NearEarthObject

class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object use to write the results from supported output formatting options.
    """

    def __init__(self):
        # TODO: How can we use the OutputFormat in the NEOWriter?
        self.output_formats = OutputFormat.list()

    def write(self, format, data, **kwargs):
        """
        Generic write interface that, depending on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting output e.g. filename
        :return: bool representing if write successful or not
        """
        # TODO: Using the OutputFormat, how can we organize our 'write' logic for output to stdout vs to csvfile
        # TODO: into instance methods for NEOWriter? Write instance methods that write() can call to do the necessary
        # TODO: output format.
        print(kwargs.items())
        self.filename = None
        for key, value in kwargs.items():
            if key == 'output_filename':
                self.filename = value
        if not self.filename:
            self.filename = 'output.csv'


        if format in self.output_formats:
            if format == 'display':
                for each in data:
                    print(each)
                result = True
            else:
                self.save_csv(data, self.filename, isinstance(data[0], NearEarthObject))
                result = True
        else:
            print('invalid format')
            result = False
        return result


    def save_csv(self, data, filename, is_neo_object):
        if is_neo_object:
            data_list = []
            for each in data:
                data_list.append([each.name, each.nasa_jpl_url, each.absolute_magnitude_h,\
                each.diameter_min_km, each.is_potentially_hazardous_asteroid])
            df = pd.DataFrame(data_list, columns = ['name', 'nasa_jpl_url', 'absolute_magnitude_h',\
                            'diameter_min_km', 'is_potentially_hazardous_asteroid'])
            df.to_csv(filename, index=None)
        else:
            for each in data:
                data_list.append([each.neo_name, each.miss_distance_kilometers, each.close_approach_date])
            df = pd.DataFrame(data_list, columns = ['name', 'miss_distance_kilometers', 'close_approach_date'])
            df.to_csv(filename, index=None)
