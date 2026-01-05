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
"""
:class:`.OptimizedDirection` returns TSP-optimized directions results.
"""
from typing import List, Optional


class OptimizedDirection(object):
    """
    Contains a parsed optimized_directions's response. Access via properties ``geometry``, ``duration``, ``distance``
    and ``original_indices``.
    """

    def __init__(self, geometry=None, duration=None, distance=None, original_indices=None, raw=None):
        """
        Initialize a :class:`OptimizedDirection` object to hold the properties of an optimized direction request.

        :param geometry: The geometry list in [[lon1, lat1], [lon2, lat2]] order.
        :type geometry: list of list

        :param duration: The duration of the direction in seconds.
        :type duration: int or float

        :param distance: The distance of the direction in meters.
        :type distance: int

        :param original_indices: An array of the original location indices to easily correlate the reordered
            waypoints to the input.
        :param original_indices: list[int]

        :param raw: The raw JSON response
        :type raw: dict
        """
        self._geometry = geometry
        self._duration = duration
        self._distance = distance
        self._original_indices = original_indices
        self._raw = raw

    @property
    def geometry(self) -> Optional[List[List[float]]]:
        """
        The geometry of the route as [[lon1, lat1], [lon2, lat2], ...] list.

        :rtype: list or None
        """
        return self._geometry

    @property
    def duration(self) -> int:
        """
        The duration of the entire trip in seconds.

        :rtype: int
        """
        return self._duration

    @property
    def distance(self) -> int:
        """
        The distance of the entire trip in meters.

        :rtype: int
        """
        return self._distance

    @property
    def km(self) -> float:
        """
        The distance of the entire trip in kilometers.

        :rtype: float
        """
        return self.distance / 1000

    @property
    def mi(self) -> float:
        """
        The distance of the entire trip in miles.

        :rtype: float
        """
        return self.distance * 0.0006213712

    @property
    def original_index(self, reordered_index: int) -> int:
        """
        The original (input) location index for the ``reordered_index`` element of the response locations.

        :param: The index of the optimized location.
        :rtype: int
        """
        return self._original_indices[reordered_index]

    @property
    def raw(self) -> Optional[dict]:
        """
        Returns the route's raw, unparsed response. For details, consult the routing engine's API documentation.

        :rtype: dict or None
        """
        return self._raw

    def __repr__(self):  # pragma: no cover
        return "OptimizedDirection({}, {}, {})".format(self.geometry, self.duration, self.distance)
