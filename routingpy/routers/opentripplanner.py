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
from typing import List, Union, Optional

from routingpy.client_base import DEFAULT
from routingpy.client_default import Client
from routingpy.isochrone import Isochrone, Isochrones


class OpenTripPlanner:
    def __init__(
        self,
        base_url,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        retry_over_query_limit=False,
        skip_api_error=None,
        client=Client,
        router_id="default",
        **client_kwargs,
    ):
        self.router_id = router_id
        self.client = client(
            base_url,
            user_agent,
            timeout,
            retry_timeout,
            retry_over_query_limit,
            skip_api_error,
            **client_kwargs,
        )

    def isochrones(
        self,
        locations: List[float],
        intervals: List[int],
        profile: Optional[Union[str, List[str]]] = None,
        date: str = None,
        time: str = None,
        arrive_by: bool = False,  # TODO: check whether param makes sense (if so, keep in mind that toPlace must be specified)
        bike_speed: Optional[float] = None,
        max_time_sec: Optional[int] = None,
        walk_speed: Optional[float] = None,
        transfer_penalty: Optional[int] = None,
        wheelchair: bool = None,
        max_walk_distance: Optional[float] = None,
        min_transfer_time: Optional[int] = None,
        dry_run: bool = None,
    ) -> Isochrones:

        get_params = self._get_isochrone_params(
            locations,
            profile,
            intervals,
            date,
            time,
            arrive_by,
            bike_speed,
            max_time_sec,
            walk_speed,
            transfer_penalty,
            wheelchair,
            max_walk_distance,
            min_transfer_time,
        )

        return self._parse_isochrone_json(
            self.client._request(
                f"/otp/routers/{self.router_id}/isochrone", get_params=get_params, dry_run=dry_run
            ),
            intervals,
            locations,
        )

    @staticmethod
    def _get_isochrone_params(
        locations,
        profile,
        intervals,
        date,
        time,
        arrive_by,
        bike_speed,
        max_time_sec,
        walk_speed,
        transfer_penalty,
        wheelchair,
        max_walk_distance,
        min_transfer_time,
    ):

        params = [("fromPlace", locations)]
        params.extend([("cutoffSec", interval) for interval in intervals])

        if profile:
            profiles = profile if type(profile) == str else ",".join(profile)
            params.append(("mode", profiles))
        if date:
            params.append(("date", date))
        if time:
            params.append(("time", time))
        if arrive_by:
            params.append(("arriveBy", arrive_by))
        if bike_speed:
            params.append(("bikeSpeed", bike_speed))
        if max_time_sec:
            params.append(("maxTimeSec", max_time_sec))
        if walk_speed:
            params.append(("walkSpeed", walk_speed))
        if transfer_penalty:
            params.append(("transferPenalty", transfer_penalty))
        if wheelchair:
            params.append(("wheelchair", wheelchair))
        if max_walk_distance:
            params.append(("maxWalkDistance", max_walk_distance))
        if min_transfer_time:
            params.append(("minTransferTime", min_transfer_time))

        return sorted(params)

    @staticmethod
    def _parse_isochrone_json(response, intervals, locations):
        if response is None:
            return Isochrones()

        isochrones = []
        for idx, feature in enumerate(response["features"]):
            isochrones.append(
                Isochrone(
                    geometry=feature["geometry"]["coordinates"],
                    interval=intervals[idx],
                    center=locations,
                )
            )

        return Isochrones(isochrones, response)
