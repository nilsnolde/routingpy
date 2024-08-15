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
:class:`Matrix` returns matrix results.
"""
from typing import List, Optional


class Matrix(object):
    """
    Contains a parsed matrix response. Access via properties ``geometry`` and ``raw``.
    """

    def __init__(self, durations=None, distances=None, raw=None):
        self._durations = durations
        self._distances = distances
        self._raw = raw

    @property
    def durations(self) -> Optional[List[List[Optional[float]]]]:
        """
        The durations matrix as list akin to::

            [
                [
                    duration(origin1-destination1),
                    duration(origin1-destination2),
                    duration[origin1-destination3),
                    ...
                ],
                [
                    duration(origin2-destination1),
                    duration(origin2-destination2),
                    duration[origin3-destination3),
                    ...
                ],
                ...
            ]

        :rtype: list or None
        """
        return self._durations

    @property
    def distances(self) -> Optional[List[List[float]]]:
        """
        The distance matrix as list akin to::

            [
                [
                    duration(origin1-destination1),
                    duration(origin1-destination2),
                    duration[origin1-destination3),
                    ...
                ],
                [
                    duration(origin2-destination1),
                    duration(origin2-destination2),
                    duration[origin3-destination3),
                    ...
                ],
                ...
            ]

        :rtype: list or None
        """
        return self._distances

    @property
    def raw(self) -> Optional[dict]:
        """
        Returns the matrices raw, unparsed response. For details, consult the routing engine's API documentation.

        :rtype: dict or None
        """
        return self._raw

    def __repr__(self):  # pragma: no cover
        return "Matrix({}, {})".format(self.durations, self.distances)
