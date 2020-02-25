class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        # id, name, nasa_jpl_url, absolute_magnitude_h, estimated_diameter_min_kilometers
        for key, value in kwargs.items():
            if key == 'id':
                self.id = value
            elif key == 'name':
                self.name = value
            elif key == 'nasa_jpl_url':
                self.nasa_jpl_url = value
            elif key == 'absolute_magnitude_h':
                self.absolute_magnitude_h = value
            elif key == 'diameter_min_km':
                self.diameter_min_km = value
            elif key == 'is_potentially_hazardous_asteroid':
                self.is_potentially_hazardous_asteroid = value
        self.list_of_orbits = []

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """
        # TODO: How do we connect orbits back to the Near Earth Object?
        self.list_of_orbits.append(orbit)

    def __str__(self):
        message = 'Name: ' + self.name \
                 + ', NASA_Jpl_Url: ' + self.nasa_jpl_url \
                 + ', Absolute_Magnitude_H: ' + self.absolute_magnitude_h \
                 + ', diameter_min_km: ' + self.diameter_min_km \
                 + ', is_potentially_hazardous_asteroid: ' + self.is_potentially_hazardous_asteroid
        return message





class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        #name, miss distance in km, and orbit date
        for key, value in kwargs.items():
            if key == 'name':
                self.name = value
            elif key == 'miss_distance_kilometers':
                self.miss_distance_kilometers = value
            elif key == 'close_approach_date':
                self.close_approach_date = value

    def __str__(self):
        message = 'Name: ' + self.name \
                 + ', Miss_Distance_Kilometers: ' + self.miss_distance_kilometers \
                 + ', Close_Approach_Date: ' + self.close_approach_date
        return message
