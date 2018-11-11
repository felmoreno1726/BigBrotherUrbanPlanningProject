import numpy as np

def Geo2Cartesian(_geopoint):
    """
    Convert geocoordiinates into Cartesian coordinates
    Input:
        point: a tuple of (lattitude, longitude)
    Output:
        coords: a numpy array the point in Cartesian system (x, y, z)
    """
    _lat, _lon = np.deg2rad(_geopoint[0]), np.deg2rad(_geopoint[1])
    _r = np.cos(_lat)
    return np.array([_r*np.cos(_lon),
                     _r*np.sin(_lon),
                     np.sin(_lat)])

def Cartesian2Geo(_Carpoint):
    """
    Convert Cartesian coordinates into geocoordiinates
    Input:
        coords: a numpy array of the point in Cartesian system (x, y, z)
    Output:
        point: a tuple array of (lattitude, longitude)
    """
    return (np.rad2deg(np.arcsin(_Carpoint[2])),
            np.rad2deg(np.arctan2(_Carpoint[1], _Carpoint[0])))

def circle_linspace_3d(_x, _y, _n):
    """
    Interpolate two points on the unit sphere
    Input:
        x, y: starting and ending points - tuple (lattitude, longitude)
        n: number of points to generate
    Output:
        result_points: a list of the generate points in numpy array (lattitude, longitude)
    """
    # Angle from scalar product
    _alpha = np.arccos(np.dot(_x, _y))
    # Angle relative to mid point
    _beta = _alpha*np.linspace(-0.5, 0.5, _n)
    # Distance of interpolated point to the center of sphere
    _r = np.cos(0.5*_alpha)/np.cos(_beta)
    # Distance to mid line
    _m = _r*np.sin(_beta)
    # Interpolation on the chord
    _chord = 2.0*np.sin(0.5*_alpha)
    _d = (_m + np.sin(0.5*_alpha))/_chord
    # Obtain the points
    _points = _x[None, :] + (_y - _x)[None, :] * _d[:, None]
    return _points/np.sqrt(np.sum(_points**2, axis=1, keepdims=True))

def latt_long_linspace(_start, _end, _N):
    """
    Return a linspace between two points of provided lattitude and longitude

    Input:
        start: a numpy array of starting point (lattitude, longitude)
        end: a numpy array of ending point (lattitude, longitude)
        N: number of points in between to be generated
    Output:
        points: a numpy array of the points in between
    """
    _x = Geo2Cartesian(_start)
    _y = Geo2Cartesian(_end)
    # Interpolate points
    _inter_points = circle_linspace_3d(_x, _y, _N)
    # Get the results
    _result = []
    for _p in _inter_points:
        _result.append(Cartesian2Geo(_p))
    return _result
