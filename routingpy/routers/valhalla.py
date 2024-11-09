# -*- coding: utf-8 -*-
# Copyright (C) 2021 GIS OPS UG
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

from operator import itemgetter
from typing import List, Optional, Sequence, Union  # noqa: F401

from .. import utils
from ..client_base import DEFAULT
from ..client_default import Client
from ..direction import Direction
from ..expansion import Edge, Expansions
from ..isochrone import Isochrone, Isochrones
from ..matrix import Matrix
from ..valhalla_attributes import MatchedResults


class Valhalla:
    """Performs requests to a Valhalla instance."""

    _DEFAULT_BASE_URL = "https://valhalla1.openstreetmap.de"

    def __init__(
        self,
        base_url: str = _DEFAULT_BASE_URL,
        user_agent: Optional[str] = None,
        timeout: Optional[Union[int, None]] = DEFAULT,
        retry_timeout: Optional[int] = None,
        retry_over_query_limit: Optional[bool] = False,
        skip_api_error: Optional[bool] = None,
        client=Client,
        **client_kwargs: dict
    ):
        """
        Initializes a Valhalla client.

        :param base_url: The base URL for the request. Defaults to the public OSM
            server. Should not have a trailing slash.

        :param user_agent: User Agent to be used when requesting.
            Default :attr:`routingpy.routers.options.default_user_agent`.

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify ``None`` for no timeout. Default :attr:`routingpy.routers.options.default_timeout`.

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.  Default :attr:`routingpy.routers.options.default_retry_timeout`.

        :param retry_over_query_limit: If True, client will not raise an exception
            on HTTP 429, but instead jitter a sleeping timer to pause between
            requests until HTTP 200 or retry_timeout is reached.
            Default :attr:`routingpy.routers.options.default_retry_over_query_limit`.

        :param skip_api_error: Continue with batch processing if a :class:`routingpy.exceptions.RouterApiError` is
            encountered (e.g. no route found). If False, processing will discontinue and raise an error.
            Default :attr:`routingpy.routers.options.default_skip_api_error`.

        :param client: A client class for request handling. Needs to be derived from :class:`routingpy.base.BaseClient`
        :type client: abc.ABCMeta

        :param client_kwargs: Additional arguments passed to the client, such as headers or proxies.
        """

        self.client = client(
            base_url,
            user_agent,
            timeout,
            retry_timeout,
            retry_over_query_limit,
            skip_api_error,
            **client_kwargs
        )

    class Waypoint(object):
        """
        Constructs a waypoint with additional information or constraints.

        Refer to Valhalla's documentation for details: https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#locations

        Use ``kwargs`` to specify options, make sure the value is proper for each option.

        Example:

        >>> waypoint = Valhalla.WayPoint(position=[8.15315, 52.53151], type='through', heading=120, heading_tolerance=10, minimum_reachability=10, radius=400)
        >>> route = Valhalla('http://localhost').directions(locations=[[[8.58232, 51.57234]], waypoint, [7.15315, 53.632415]])
        """

        def __init__(self, position, **kwargs):
            self._position = position
            self._kwargs = kwargs

        def _make_waypoint(self):
            waypoint = {"lon": self._position[0], "lat": self._position[1]}
            for k, v in self._kwargs.items():
                waypoint[k] = v

            return waypoint

    def directions(
        self,
        locations: List[List[float]],
        profile: str,
        preference: Optional[str] = None,
        options: Optional[dict] = None,
        units: Optional[str] = None,
        instructions: Optional[bool] = False,
        language: Optional[str] = None,
        directions_type: Optional[str] = None,
        avoid_locations: Optional[List[List[float]]] = None,
        avoid_polygons: Optional[List[List[List[float]]]] = None,
        date_time: Optional[dict] = None,
        id: Optional[Union[str, int, float]] = None,
        dry_run: Optional[bool] = None,
        **kwargs
    ):
        """Get directions between an origin point and a destination point.

        For more information, visit https://github.com/valhalla/valhalla/blob/master/docs/docs/api/turn-by-turn/api-reference.md.

        Use ``kwargs`` for any missing ``directions`` request options.

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit. Can be a list/tuple of [lon, lat] or :class:`Valhalla.WayPoint` instance or
            a combination of both.

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "auto_shorter" (deprecated), "bicycle", "bus", "hov", "motor_scooter",
            "motorcycle", "multimodal", "pedestrian"].

        :param preference: Convenience argument to set the cost metric, one of ['shortest', 'fastest']. Note,
            that shortest is not guaranteed to be absolute shortest for motor vehicle profiles. It's called ``preference``
            to be inline with the already existing parameter in the ORS adapter.

        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options

        :param units: Distance units for output. One of ['mi', 'km']. Default km.

        :param instructions: Whether to return turn-by-turn instructions. Named for compatibility with other
            providers. Valhalla's parameter here is 'narrative'.

        :param language: The language of the narration instructions based on the IETF BCP 47 language tag string.
            One of ['ca', 'cs', 'de', 'en', 'pirate', 'es', 'fr', 'hi', 'it', 'pt', 'ru', 'sl', 'sv']. Default 'en'.

        :param directions_type: 'none': no instructions are returned. 'maneuvers': only maneuvers are returned.
            'instructions': maneuvers with instructions are returned. Default 'instructions'.

        :param avoid_locations: A set of locations to exclude or avoid within a route.
            Specified as a list of coordinates, similar to coordinates object.

        :param avoid_polygons: One or multiple exterior rings of polygons in the form of nested
            JSON arrays, e.g. [[[lon1, lat1], [lon2,lat2]],[[lon1,lat1],[lon2,lat2]]]. Roads intersecting these rings
            will be avoided during path finding. If you only need to avoid a few specific roads, it's much more
            efficient to use avoid_locations. Valhalla will close open rings (i.e. copy the first coordingate to the
            last position).

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in ISO 8601 format (YYYY-MM-DDThh:mm), local time.
            E.g. date_time = {type: 0, value: 2021-03-03T08:06:23}

        :param id: Name your route request. If id is specified, the naming will be sent thru to the response.

        :param dry_run: Print URL and parameters without sending the request.

        :param kwargs: any additional keyword arguments which will override parameters.

        :returns: A route from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction`
        """

        params = self.get_direction_params(
            locations,
            profile,
            preference,
            options,
            units,
            instructions,
            language,
            directions_type,
            avoid_locations,
            avoid_polygons,
            date_time,
            id,
            **kwargs
        )

        return self.parse_direction_json(
            self.client._request("/route", post_params=params, dry_run=dry_run),
            units,
        )

    @staticmethod
    def get_direction_params(
        locations,
        profile,
        preference=None,
        options=None,
        units=None,
        instructions=False,
        language=None,
        directions_type=None,
        avoid_locations=None,
        avoid_polygons=None,
        date_time=None,
        id=None,
        **kwargs
    ):
        """
        Builds and returns the router's route parameters. It's a separate function so that
        bindings can use routingpy's functionality. See documentation of .matrix().
        """
        params = dict(costing=profile, narrative=instructions)

        params["locations"] = Valhalla._build_locations(locations)

        if options or preference:
            params["costing_options"] = dict()
            profile = profile if profile not in ("multimodal", "transit") else "transit"
            params["costing_options"][profile] = dict()
            if options:
                params["costing_options"][profile] = options
            if preference == "shortest":
                params["costing_options"][profile]["shortest"] = True

        if any((units, language, directions_type)):
            params["directions_options"] = dict()
            if units:
                params["directions_options"]["units"] = units
            if language:
                params["directions_options"]["language"] = language
            if directions_type:
                params["directions_options"]["directions_type"] = directions_type

        if avoid_locations:
            params["avoid_locations"] = Valhalla._build_locations(avoid_locations)

        if avoid_polygons:
            params["avoid_polygons"] = avoid_polygons

        if date_time:
            params["date_time"] = date_time

        if id:
            params["id"] = id

        # update with kw args
        params.update(kwargs)

        return params

    @staticmethod
    def parse_direction_json(response, units):
        if response is None:  # pragma: no cover
            return Direction()

        geometry, duration, distance = [], 0, 0
        for leg in response["trip"]["legs"]:
            geometry.extend(utils.decode_polyline6(leg["shape"]))
            duration += leg["summary"]["time"]

            factor = 0.621371 if units == "mi" else 1
            distance += int(leg["summary"]["length"] * 1000 * factor)

        return Direction(geometry=geometry, duration=int(duration), distance=int(distance), raw=response)

    def isochrones(  # noqa: C901
        self,
        locations: List[float],
        profile: str,
        intervals: List[int],
        interval_type: Optional[str] = "time",
        colors: Optional[List[str]] = None,
        polygons: Optional[bool] = None,
        denoise: Optional[float] = None,
        generalize: Optional[float] = None,
        preference: Optional[str] = None,
        options: Optional[dict] = None,
        units: Optional[str] = None,
        language: Optional[str] = None,
        directions_type: Optional[str] = None,
        avoid_locations: Optional[List[List[float]]] = None,
        avoid_polygons: Optional[List[List[List[float]]]] = None,
        date_time: Optional[dict] = None,
        show_locations: Optional[List[List[float]]] = None,
        id: Optional[str] = None,
        dry_run: Optional[bool] = None,
        **kwargs
    ):
        """Gets isochrones or equidistants for a range of time values around a given set of coordinates.

        For more information, visit https://github.com/valhalla/valhalla/blob/master/docs/api/isochrone/api-reference.md.

        Use ``kwargs`` for any missing ``isochrones`` request options.

        :param locations: One pair of lng/lat values. Takes the form [Longitude, Latitude].

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "bicycle", "multimodal", "pedestrian".

        :param intervals: Time ranges to calculate isochrones for. In seconds or meters, depending on `interval_type`.

        :param interval_type: Set 'time' for isochrones or 'distance' for equidistants.
            Default 'time'.

        :param colors: The color for the output of the contour. Specify it as a Hex value, but without the #, such as
            "color":"ff0000" for red. If no color is specified, the isochrone service will assign a default color to the output.

        :param polygons: Controls whether polygons or linestrings are returned in GeoJSON geometry. Default False.

        :param denoise: Can be used to remove smaller contours. In range [0, 1]. A value of 1 will only return the largest contour
            for a given time value. A value of 0.5 drops any contours that are less than half the area of the largest
            contour in the set of contours for that same time value. Default 1.

        :param generalize: A floating point value in meters used as the tolerance for Douglas-Peucker generalization.
            Note: Generalization of contours can lead to self-intersections, as well as intersections of adjacent contours.

        :param preference: Convenience argument to set the cost metric, one of ['shortest', 'fastest']. Note,
            that shortest is not guaranteed to be absolute shortest for motor vehicle profiles. It's called ``preference``
            to be inline with the already existing parameter in the ORS adapter.

        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options

        :param units: Distance units for output. One of ['mi', 'km']. Default km.

        :param language: The language of the narration instructions based on the IETF BCP 47 language tag string.
            One of ['ca', 'cs', 'de', 'en', 'pirate', 'es', 'fr', 'hi', 'it', 'pt', 'ru', 'sl', 'sv']. Default 'en'.

        :param avoid_locations: A set of locations to exclude or avoid within a route.
            Specified as a list of coordinates, similar to coordinates object.

        :param List[List[List[float]]] avoid_polygons: One or multiple exterior rings of polygons in the form of nested
            JSON arrays, e.g. [[[lon1, lat1], [lon2,lat2]],[[lon1,lat1],[lon2,lat2]]]. Roads intersecting these rings
            will be avoided during path finding. If you only need to avoid a few specific roads, it's much more
            efficient to use avoid_locations. Valhalla will close open rings (i.e. copy the first coordingate to the
            last position).

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in format YYYY-MM-DDThh:mm, local time.

            E.g. date_time = {type: 0, value: 2021-03-03T08:06}

        :param id: Name your route request. If id is specified, the naming will be sent thru to the response.

        :param dry_run: Print URL and parameters without sending the request.

        :returns: An isochrone with the specified range.
        :rtype: :class:`routingpy.isochrone.Isochrones`
        """

        params = self.get_isochrone_params(
            locations,
            profile,
            intervals,
            interval_type,
            colors,
            polygons,
            denoise,
            generalize,
            preference,
            options,
            avoid_locations,
            avoid_polygons,
            date_time,
            show_locations,
            id,
            **kwargs
        )

        return self.parse_isochrone_json(
            self.client._request("/isochrone", post_params=params, dry_run=dry_run),
            intervals,
            locations,
            interval_type,
        )

    @staticmethod  # noqa: C901
    def get_isochrone_params(  # noqa: C901
        locations,
        profile,
        intervals,
        interval_type,
        colors=None,
        polygons=None,
        denoise=None,
        generalize=None,
        preference=None,
        options=None,
        avoid_locations=None,
        avoid_polygons=None,
        date_time=None,
        show_locations=None,
        id=None,
        **kwargs
    ):
        """
        Builds and returns the router's route parameters. It's a separate function so that
        bindings can use routingpy's functionality. See documentation of .matrix().
        """
        contours = []
        for idx, r in enumerate(intervals):
            key = "time"
            value = r / 60
            if interval_type == "distance":
                key = "distance"
                value = r / 1000

            d = {key: value}
            if colors:
                try:
                    d.update(color=colors[idx])
                except IndexError:
                    raise IndexError("Colors object must have same length as Range object.")
            contours.append(d)

        params = {
            "locations": Valhalla._build_locations(locations),
            "costing": profile,
            "contours": contours,
        }

        if options or preference:
            params["costing_options"] = dict()
            profile = profile if profile != "multimodal" else "transit"
            params["costing_options"][profile] = dict()
            if options:
                params["costing_options"][profile] = options
            if preference == "shortest":
                params["costing_options"][profile]["shortest"] = True

        if polygons is not None:
            params["polygons"] = polygons

        if denoise:
            params["denoise"] = denoise

        if generalize:
            params["generalize"] = generalize

        if avoid_locations:
            params["avoid_locations"] = Valhalla._build_locations(avoid_locations)

        if avoid_polygons:
            params["avoid_polygons"] = avoid_polygons

        if date_time:
            params["date_time"] = date_time

        if show_locations is not None:
            params["show_locations"] = show_locations

        if id:
            params["id"] = id

        params.update(kwargs)

        return params

    @staticmethod
    def parse_isochrone_json(response, intervals, locations, interval_type):
        if response is None:  # pragma: no cover
            return Isochrones()

        isochrones = []
        for idx, feature in enumerate(reversed(response["features"])):
            if feature["geometry"]["type"] in ("LineString", "Polygon"):
                isochrones.append(
                    Isochrone(
                        geometry=feature["geometry"]["coordinates"],
                        interval=intervals[idx],
                        center=locations,
                        interval_type=interval_type,
                    )
                )

        return Isochrones(isochrones, response)

    def matrix(
        self,
        locations: List[List[float]],
        profile: str,
        sources: Optional[List[int]] = None,
        destinations: Optional[List[int]] = None,
        preference: Optional[str] = None,
        options: Optional[dict] = None,
        avoid_locations: Optional[List[List[float]]] = None,
        avoid_polygons: Optional[List[List[List[float]]]] = None,
        units: Optional[str] = None,
        date_time: Optional[dict] = None,
        id: Optional[str] = None,
        dry_run: Optional[bool] = None,
        **kwargs
    ):
        """
        Gets travel distance and time for a matrix of origins and destinations.

        For more information, visit https://github.com/valhalla/valhalla/blob/master/docs/docs/api/matrix/api-reference.md.

        Use ``kwargs`` for any missing ``matrix`` request options.

        :param locations: Multiple pairs of lng/lat values.

        :param profile: Specifies the mode of transport to use when calculating
            matrices. One of ["auto", "bicycle", "multimodal", "pedestrian".

        :param sources: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.

        :param destinations: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.

        :param str preference: Convenience argument to set the cost metric, one of ['shortest', 'fastest']. Note,
            that shortest is not guaranteed to be absolute shortest for motor vehicle profiles. It's called ``preference``
            to be inline with the already existing parameter in the ORS adapter.

        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options

        :param avoid_locations: A set of locations to exclude or avoid within a route.
            Specified as a list of coordinates, similar to coordinates object.

        :param List[List[List[float]]] avoid_polygons: One or multiple exterior rings of polygons in the form of nested
            JSON arrays, e.g. [[[lon1, lat1], [lon2,lat2]],[[lon1,lat1],[lon2,lat2]]]. Roads intersecting these rings
            will be avoided during path finding. If you only need to avoid a few specific roads, it's much more
            efficient to use avoid_locations. Valhalla will close open rings (i.e. copy the first coordingate to the
            last position).

        :param units: Distance units for output. One of ['mi', 'km']. Default km.

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in format YYYY-MM-DDThh:mm, local time.

        :param id: Name your route request. If id is specified, the naming will be sent through to the response.

        :param dry_run: Print URL and parameters without sending the request.

        :returns: A matrix from the specified sources and destinations.
        :rtype: :class:`routingpy.matrix.Matrix`
        """

        params = self.get_matrix_params(
            locations,
            profile,
            sources,
            destinations,
            preference,
            options,
            avoid_locations,
            avoid_polygons,
            units,
            date_time,
            id,
            **kwargs
        )

        return self.parse_matrix_json(
            self.client._request("/sources_to_targets", post_params=params, dry_run=dry_run),
            units,
        )

    @staticmethod
    def get_matrix_params(
        locations,
        profile,
        sources=None,
        destinations=None,
        preference=None,
        options=None,
        avoid_locations=None,
        avoid_polygons=None,
        units=None,
        date_time=None,
        id=None,
        **kwargs
    ):
        """
        Builds and returns the router's route parameters. It's a separate function so that
        bindings can use routingpy's functionality. See documentation of .matrix().
        """
        params = {
            "costing": profile,
        }

        locations = Valhalla._build_locations(locations)

        sources_coords = locations
        if sources is not None:
            sources_coords = itemgetter(*sources)(sources_coords)
            if isinstance(sources_coords, dict):
                sources_coords = [sources_coords]
        params["sources"] = sources_coords

        dest_coords = locations
        if destinations is not None:
            dest_coords = itemgetter(*destinations)(dest_coords)
            if isinstance(dest_coords, dict):
                dest_coords = [dest_coords]
        params["targets"] = dest_coords

        if options or preference:
            params["costing_options"] = dict()
            profile = profile if profile != "multimodal" else "transit"
            params["costing_options"][profile] = dict()
            if options:
                params["costing_options"][profile] = options
            if preference == "shortest":
                params["costing_options"][profile]["shortest"] = True

        if avoid_locations:
            params["avoid_locations"] = Valhalla._build_locations(avoid_locations)

        if avoid_polygons:
            params["avoid_polygons"] = avoid_polygons

        if units:
            params["units"] = units

        if date_time:
            params["date_time"] = date_time

        if id:
            params["id"] = id

        params.update(kwargs)

        return params

    @staticmethod
    def parse_matrix_json(response, units):
        if response is None:  # pragma: no cover
            return Matrix()

        factor = 0.621371 if units == "mi" else 1
        durations = [
            [destination["time"] for destination in origin] for origin in response["sources_to_targets"]
        ]
        distances = [
            [
                int(destination["distance"] * 1000 * factor)
                if destination["distance"] is not None
                else None
                for destination in origin
            ]
            for origin in response["sources_to_targets"]
        ]

        return Matrix(durations=durations, distances=distances, raw=response)

    def expansion(
        self,
        locations: Sequence[float],
        profile: str,
        intervals: Sequence[int],
        skip_opposites: Optional[bool] = None,
        expansion_properties: Optional[Sequence[str]] = None,
        interval_type: Optional[str] = "time",
        options: Optional[dict] = None,
        date_time: Optional[dict] = None,
        id: Optional[str] = None,
        dry_run: Optional[bool] = None,
        **kwargs
    ) -> Expansions:
        """Gets the expansion tree for a range of time or distance values around a given coordinate.

        For more information, visit https://valhalla.readthedocs.io/en/latest/api/expansion/api-reference/.

        :param locations: One pair of lng/lat values. Takes the form [Longitude, Latitude].

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "bicycle", "multimodal", "pedestrian".

        :param intervals: Time ranges to calculate isochrones for. In seconds or meters, depending on `interval_type`.

        :param skip_opposites: If set to true the output won't contain an edge's opposing edge. Opposing edges can be thought of as both directions of one road segment. Of the two, we discard the directional edge with higher cost and keep the one with less cost.

        :param expansion_properties: A JSON array of strings of the GeoJSON property keys you'd like to have in the response. One or multiple of "durations", "distances", "costs", "edge_ids", "statuses". Note, that each additional property will increase the output size by minimum ~ 25%.

        :param interval_type: Set 'time' for isochrones or 'distance' for equidistants.
            Default 'time'.

        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in format YYYY-MM-DDThh:mm, local time.

            E.g. date_time = {type: 0, value: 2021-03-03T08:06}

        :param id: Name your route request. If id is specified, the naming will be sent thru to the response.

        :param dry_run: Print URL and parameters without sending the request.

        :returns: An expansions object consisting of single line strings and their attributes (if specified).
        """
        params = self.get_expansion_params(
            locations,
            profile,
            intervals,
            skip_opposites,
            expansion_properties,
            interval_type,
            options,
            date_time,
            id,
            **kwargs
        )
        return self.parse_expansion_json(
            self.client._request("/expansion", post_params=params, dry_run=dry_run),
            locations,
            expansion_properties,
            interval_type,
        )

    @classmethod
    def get_expansion_params(
        cls,
        locations,
        profile,
        intervals,
        skip_opposites=None,
        expansion_properties=None,
        interval_type=None,
        options=None,
        date_time=None,
        id=None,
        **kwargs
    ):
        params = cls.get_isochrone_params(
            locations,
            profile,
            intervals,
            interval_type,
            options=options,
            date_time=date_time,
            id=id,
        )
        params["action"] = "isochrone"
        if skip_opposites:
            params["skip_opposites"] = skip_opposites
        if expansion_properties:
            params["expansion_properties"] = expansion_properties

        params.update(kwargs)

        return params

    @staticmethod
    def parse_expansion_json(response, locations, expansion_properties, interval_type):
        if response is None:  # pragma: no cover
            return Expansions()

        expansions = []
        for idx, line in enumerate(response["features"][0]["geometry"]["coordinates"]):
            properties = {}
            if expansion_properties:
                for expansion_prop in expansion_properties:
                    properties[expansion_prop] = response["features"][0]["properties"][expansion_prop][
                        idx
                    ]
            expansions.append(Edge(geometry=line, **properties))

        return Expansions(expansions, locations, interval_type, response)

    def trace_attributes(
        self,
        locations: Optional[Sequence[Union[Sequence[float], Waypoint]]] = None,
        profile: str = "bicycle",
        shape_match: str = "walk_or_snap",
        encoded_polyline: Optional[str] = None,
        filters: Optional[List[str]] = None,
        filters_action: Optional[str] = None,
        options: Optional[dict] = None,
        dry_run: Optional[bool] = None,
        **kwargs
    ) -> MatchedResults:
        """
        Map-matches the input locations to form a route on the Valhalla base network and
        returns detailed attribution for encountered edges and nodes.

        For more information, visit https://valhalla.readthedocs.io/en/latest/api/map-matching/api-reference/.

        :param locations: One pair of lng/lat values or :class:`Waypoint`. Takes the form [Longitude, Latitude].
        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "bicycle", "multimodal", "pedestrian".
        :param shape_match: It allows some control of the matching algorithm based on the type of input. One of
            ["edge_walk", "map_snap", "walk_or_snap"]. See for full reference:
            https://github.com/valhalla/valhalla/blob/master/docs/api/map-matching/api-reference.md#shape-matching-parameters
        :param encoded_polyline: The encoded polyline string with precision 6.
        :param filters: A list of response object to either include or exclude, depending on the filter_action
            attribute
        :param filters_action: Whether to include or exclude the filters. One of ["include", "exclude"].
        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options
        :param dry_run: Print URL and parameters without sending the request.

        :raises: ValueError if 'locations' and 'encoded_polyline' was specified
        :returns: A :class:`MatchedResults` object with matched edges and points set.
        """
        if locations and encoded_polyline:
            raise ValueError

        params = self.get_trace_attributes_params(
            locations, profile, shape_match, encoded_polyline, filters, filters_action, options, **kwargs
        )

        return self.parse_trace_attributes_json(
            self.client._request("/trace_attributes", post_params=params, dry_run=dry_run)
        )

    @classmethod
    def get_trace_attributes_params(
        cls,
        locations: Optional[Sequence[Union[Sequence[float], Waypoint]]] = None,
        profile: str = "bicycle",
        shape_match: str = "walk_or_snap",
        encoded_polyline: Optional[str] = None,
        filters: Optional[List[str]] = None,
        filters_action: Optional[str] = None,
        options: Optional[dict] = None,
        **kwargs
    ):
        params = dict()
        if locations:
            params["shape"] = cls._build_locations(locations)
        elif encoded_polyline:
            params["encoded_polyline"] = encoded_polyline
        else:
            raise ValueError("Need to specify 'shape' or 'encoded_polyline")

        if filters and filters_action:
            params["filters"] = dict()
            params["filters"]["attributes"] = filters
            params["action"] = filters_action

        params["costing"] = profile
        params["shape_match"] = shape_match

        if options:
            params["costing_options"] = dict()
            profile = profile if profile != "multimodal" else "transit"
            params["costing_options"][profile] = dict()
            if options:
                params["costing_options"][profile] = options

        params.update(kwargs)

        return params

    @staticmethod
    def parse_trace_attributes_json(response):
        if response is None:  # pragma: no cover
            return MatchedResults()

        return MatchedResults(response)

    @staticmethod
    def _build_locations(coordinates):
        """Build the locations object for all methods"""

        locations = []

        # Isochrones only support one coordinate tuple, so check for type of first element
        if isinstance(coordinates, Valhalla.Waypoint):
            locations.append(coordinates._make_waypoint())
        elif isinstance(coordinates[0], float):
            locations.append({"lon": coordinates[0], "lat": coordinates[1]})
        elif isinstance(coordinates[0], (list, tuple, Valhalla.Waypoint)):
            for idx, coord in enumerate(coordinates):
                if isinstance(coord, (list, tuple)):
                    locations.append({"lon": coord[0], "lat": coord[1]}),
                elif isinstance(coord, Valhalla.Waypoint):
                    locations.append(coord._make_waypoint())
                else:
                    raise TypeError(
                        "Location type {} at index {} is not supported: {}".format(
                            type(coord), idx, coord
                        )
                    )

        return locations
