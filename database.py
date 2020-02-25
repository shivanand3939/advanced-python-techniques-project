from models import OrbitPath, NearEarthObject
import pandas as pd

class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.
        self.orbitdate_neo_mapping = {}
        self.neoname_neo_mapping = {}
        self.filename = filename


    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?
        df  = pd.read_csv(filename)
        df_sub = df[['id', 'name', 'nasa_jpl_url',\
                               'absolute_magnitude_h', 'estimated_diameter_min_kilometers',\
                               'close_approach_date', 'miss_distance_kilometers']]
        df_sub['neo_object'] = df_sub.apply( self.generate_neo_object , axis = 1)
        df_sub['orbit_part_object'] = df[['id', 'name', 'nasa_jpl_url',\
                               'absolute_magnitude_h', 'estimated_diameter_min_kilometers',\
                               'close_approach_date', 'miss_distance_kilometers']].apply( self.generate_orbit_path , axis = 1)

        df_orbit_path = pd.DataFrame([])
        df_orbit_path['orbit_part_v1'] = df_sub.groupby('name')['orbit_part_object'].apply(list)
        df_orbit_path.reset_index(inplace=True)

        df_neo_object = pd.DataFrame([])
        df_neo_object['neo_object_v1'] = df_sub.groupby('name')['neo_object'].first()
        df_neo_object = df_neo_object.reset_index()

        df_res = pd.merge(df_orbit_path, df_neo_object, on='name')
        df_res['neo_object_v2'] = df_res[['neo_object_v1', 'orbit_part_v1']].apply(self.final_neo_object, axis = 1)
        df_final = pd.merge(df, df_res, on='name')

        self.orbitdate_neo_mapping = df_final.groupby(['close_approach_date'])['neo_object_v2'].apply(list).to_dict()
        self.neoname_neo_mapping = df_res.groupby(['name'])['neo_object_v2'].first().to_dict()

        return None

    def final_neo_object(self, val):
        neo_object_v1, orbit_part_v1 = val
        for each in orbit_part_v1:
            neo_object_v1.update_orbits(each)

        return neo_object_v1

    def generate_neo_object(self, val):
        """
        Generates Neo object from every record of the csv file
        """
        id_, name, nasa_jpl_url, absolute_magnitude_h, estimated_diameter_min_kilometers, close_approach_date, miss_distance_kilometers = val
        neo = NearEarthObject(id_ = id_, \
                          name = name, \
                          nasa_jpl_url = nasa_jpl_url, \
                          absolute_magnitude_h = absolute_magnitude_h, \
                          estimated_diameter_min_kilometers = estimated_diameter_min_kilometers
                         )
        return neo


    def generate_orbit_path(self, val):
        """
        Generates Neo object from every record of the csv file
        """
        id, name, nasa_jpl_url, absolute_magnitude_h, estimated_diameter_min_kilometers, close_approach_date, miss_distance_kilometers = val
        return OrbitPath(name = name, \
                     miss_distance_kilometers = miss_distance_kilometers, \
                     close_approach_date = close_approach_date)


    def get_neo_object(self, name):
        return self.neoname_neo_mapping[name]
