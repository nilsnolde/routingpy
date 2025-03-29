In case anyone has interest to take over this repository, please write me on my public email. To be eligible you should have a proven track record of FOSS python projects and ideally some PyPI package management experience.

routingpy
==========

.. image:: https://github.com/gis-ops/routing-py/workflows/tests/badge.svg
    :target: https://github.com/gis-ops/routing-py/actions/workflows/ci-tests.yml
    :alt: tests

.. image:: https://readthedocs.org/projects/routingpy/badge/?version=latest
    :target: https://routingpy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/gis-ops/routing-py/master?filepath=examples
    :alt: MyBinder.org


*One lib to route them all* - **routingpy** is a Python 3 client for several
popular routing webservices.

Inspired by `geopy <https://github.com/geopy/geopy>`_ and its great community of contributors, **routingpy** enables
easy and consistent access to third-party spatial webservices to request **route directions**, **isochrones**
or **time-distance matrices**.

**routingpy** currently includes support for the following services:

-  `Mapbox, OSRM`_
-  `Openrouteservice`_
-  `Here Maps`_
-  `Google Maps`_
-  `Graphhopper`_
-  `OpenTripPlannerV2`_
-  `Local Valhalla`_
-  `Local OSRM`_

This list is hopefully growing with time and contributions by other developers. An up-to-date list is always available
in our documentation_.

**routing-py** is tested against CPython versions 3.8, 3.9, 3.10, 3.11. PyPy3 is currently not supported, see `#60 <https://github.com/gis-ops/routingpy/issues/60>`_.

© routingpy contributors 2022 under the `Apache 2.0 License`_.

.. image:: https://user-images.githubusercontent.com/10322094/57357720-e180c080-7173-11e9-97a4-cecb4670065d.jpg
    :alt: routing-py-image


Why routingpy?
---------------

You want to

- get from A to B by transit, foot, bike, car or hgv
- compute a region of reachability
- calculate a time distance matrix for a N x M table

and don't know which provider to use? Great. Then **routingpy** is exactly what you're looking for.

For the better or worse, every provider works on different spatial global datasets and uses a plethora of algorithms on top.
While Google or HERE build on top of proprietary datasets, providers such as Mapbox or Graphhopper consume OpenStreetMap data
for their base network. Also, all providers offer a different amount of options one can use to restrict the wayfinding.
Ultimately this means that **results may differ** - and our experience tells us: they do, and not
too little. This calls for a careful evaluation which service provider to use for which specific use case.

With **routingpy** we have made an attempt to simplify this process for you.

Installation
------------

.. image:: https://badge.fury.io/py/routingpy.svg
    :target: https://badge.fury.io/py/routingpy
    :alt: PyPI version

**Recommended**: Install via poetry_:

.. code:: bash

    poetry add routingpy

Install using ``pip`` with

.. code:: bash

   pip install routingpy

Or the lastest from source

.. code:: bash

   pip install git+git://github.com/gis-ops/routingpy


API
-----------

Every provider has its own specifications and features. However the basic blueprints are the same across all. We tried hard
to make the transition from one provider to the other as seamless as possible. We follow two dogmas for all implementations:

- All basic parameters have to be the same for all routers for each endpoint

- All routers still retain their special parameters for their endpoints, which make them unique in the end

This naturally means that usually those **basic parameters are not named the same way** as the endpoints they query. However,
all **provider specific parameters are named the exact same** as their remote counterparts.

The following table gives you an overview which basic arguments are abstracted:

+-----------------------+-------------------+--------------------------------------------------------------+
|       Endpoint        |     Argument      | Function                                                     |
+=======================+===================+==============================================================+
|   ``directions``      | locations         | | Specify the locations to be visited in order. Usually this |
|                       |                   | | is done with ``[Lon, Lat]`` tuples, but some routers offer |
|                       |                   | | additional options to create a location element.           |
|                       +-------------------+--------------------------------------------------------------+
|                       | profile           | | The mode of transport, i.e. car, bicycle, pedestrian. Each |
|                       |                   | | router specifies their own profiles.                       |
+-----------------------+-------------------+--------------------------------------------------------------+
|   ``isochrones``      | locations         | | Specify the locations to calculate isochrones for. Usually |
|                       |                   | | this is done with ``[Lon, Lat]`` tuples, but some routers  |
|                       |                   | | offer additional options to create a location element.     |
|                       +-------------------+--------------------------------------------------------------+
|                       | profile           | | The mode of transport, i.e. car, bicycle, pedestrian. Each |
|                       |                   | | router specifies their own profiles.                       |
|                       +-------------------+--------------------------------------------------------------+
|                       | intervals         | | The ranges to calculate isochrones for. Either in seconds  |
|                       |                   | | or in meters, depending on ``interval_type``.              |
|                       +-------------------+--------------------------------------------------------------+
|                       | intervals _type   | | The dimension of ``intervals``, which takes router         |
|                       |                   | | dependent values, but generally describes time or distance |
+-----------------------+-------------------+--------------------------------------------------------------+
|      ``matrix``       | locations         | | Specify all locations you want to calculate a matrix       |
|                       |                   | | for. If ``sources`` or ``destinations`` is not set, this   |
|                       |                   | | will return a symmetrical matrix. Usually this is done     |
|                       |                   | | with ``[Lon, Lat]`` tuples, but some routers offer         |
|                       |                   | | additional options to create a location element.           |
|                       +-------------------+--------------------------------------------------------------+
|                       | profile           | | The mode of transport, i.e. car, bicycle, pedestrian. Each |
|                       |                   | | router specifies their own profiles.                       |
|                       +-------------------+--------------------------------------------------------------+
|                       | sources           | | The indices of the ``locations`` parameter iterable to     |
|                       |                   | | take as sources for the matrix calculation. If not         |
|                       |                   | | specified all ``locations`` are considered to be sources.  |
|                       +-------------------+--------------------------------------------------------------+
|                       | destinations      | | The indices of the ``locations`` parameter iterable to     |
|                       |                   | | take as destinations for the matrix calculation. If not    |
|                       |                   | | specified all ``locations`` are considered to be           |
|                       |                   | | destinations.                                              |
+-----------------------+-------------------+--------------------------------------------------------------+

Contributing
------------

We :heart: contributions and realistically think that's the only way to support and maintain most
routing engines in the long run. To get you started, we created a `Contribution guideline <./CONTRIBUTING.md>`_.

Examples
--------

Follow our examples to understand how simple **routingpy** is to use.

On top of the examples listed below, find interactive notebook(s) on mybinder.org_.

Basic Usage
~~~~~~~~~~~

Get all attributes
++++++++++++++++++

**routingpy** is designed to take the burden off your shoulder to parse the JSON response of each provider, exposing
the most important information of the response as attributes of the response object. The actual JSON is always accessible via
the ``raw`` attribute:

.. code:: python

    from routingpy import Valhalla
    from pprint import pprint

    # Some locations in Berlin
    coords = [[13.413706, 52.490202], [13.421838, 52.514105],
              [13.453649, 52.507987], [13.401947, 52.543373]]
    client = Valhalla()

    route = client.directions(locations=coords, profile='pedestrian')
    isochrones = client.isochrones(locations=coords[0], profile='pedestrian', intervals=[600, 1200])
    matrix = client.matrix(locations=coords, profile='pedestrian')

    pprint((route.geometry, route.duration, route.distance, route.raw))
    pprint((isochrones.raw, isochrones[0].geometry, isochrones[0].center, isochrones[0].interval))
    pprint((matrix.durations, matrix.distances, matrix.raw))


Multi Provider
++++++++++++++

Easily calculate routes, isochrones and matrices for multiple providers:

.. code:: python

    from routingpy import Graphhopper, ORS, MapboxOSRM
    from shapely.geometry import Polygon

    # Define the clients and their profile parameter
    apis = (
       (ORS(api_key='ors_key'), 'cycling-regular'),
       (Graphhopper(api_key='gh_key'), 'bike'),
       (MapboxOSRM(api_key='mapbox_key'), 'cycling')
    )
    # Some locations in Berlin
    coords = [[13.413706, 52.490202], [13.421838, 52.514105],
              [13.453649, 52.507987], [13.401947, 52.543373]]

    for api in apis:
        client, profile = api
        route = client.directions(locations=coords, profile=profile)
        print("Direction - {}:\n\tDuration: {}\n\tDistance: {}".format(client.__class__.__name__,
                                                                       route.duration,
                                                                       route.distance))
        isochrones = client.isochrones(locations=coords[0], profile=profile, intervals=[600, 1200])
        for iso in isochrones:
            print("Isochrone {} secs - {}:\n\tArea: {} sqm".format(client.__class__.__name__,
                                                                   iso.interval,
                                                                   Polygon(iso.geometry).area))
        matrix = client.matrix(locations=coords, profile=profile)
        print("Matrix - {}:\n\tDurations: {}\n\tDistances: {}".format(client.__class__.__name__,
                                                                      matrix.durations,
                                                                      matrix.distances))


Dry run - Debug
+++++++++++++++

Often it is crucial to examine the request before it is sent. Mostly useful for debugging:

.. code:: python

    from routingpy import ORS

    client = ORS(api_key='ors_key')
    route = client.directions(
        locations = [[13.413706, 52.490202], [13.421838, 52.514105]],
        profile='driving-hgv',
        dry_run=True
    )


Advanced Usage
~~~~~~~~~~~~~~

Local instance of FOSS router
+++++++++++++++++++++++++++++

All FOSS routing engines can be run locally, such as openrouteservice, Valhalla, OSRM and GraphHopper. To be able
to use **routingpy** with a local installation, just change the ``base_url`` of the client. This assumes that you did
not change the URL(s) of the exposed endpoint(s):

.. code:: python

    from routingpy import Valhalla

    # no trailing slash, api_key is not necessary
    client = Valhalla(base_url='http://localhost:8088/v1')

Proxies, Rate limiters and API errors
+++++++++++++++++++++++++++++++++++++

Proxies are easily set up using following ``requests`` scheme for proxying. Also, when batch requesting, **routingpy**
can be set up to resume its requests when the remote API rate limits (i.e. responds
with HTTP 429). Also, it can be set up to ignore API errors and instead print them as warnings to ``stdout``. Be careful,
when ignoring ``RouterApiErrors``, those often count towards your rate limit.

All these parameters, and more, can optionally be **globally set** for all router modules or individually per instance:

.. code:: python

    from routingpy import Graphhopper, ORS
    from routingpy.routers import options

    request_kwargs = dict(proxies=dict(https='129.125.12.0'))

    client = Graphhopper(
        api_key='gh_key',
        retry_over_query_limit=False,
        skip_api_error=True,
        requests_kwargs=request_kwargs
    )

    # Or alternvatively, set these options globally:
    options.default_proxies = {'https': '129.125.12.0'}
    options.default_retry_over_query_limit = False
    options.default_skip_api_error = True


.. _Mapbox, OSRM: https://docs.mapbox.com/api/navigation
.. _Openrouteservice: https://openrouteservice.org/dev/#/api-docs
.. _Here Maps: https://developer.here.com/documentation
.. _Google Maps: https://developers.google.com/maps/documentation
.. _Graphhopper: https://graphhopper.com/api/1/docs
.. _OpenTripPlannerV2: https://docs.opentripplanner.org/en/latest/
.. _Local Valhalla: https://valhalla.github.io/valhalla/
.. _Local OSRM: https://github.com/Project-OSRM/osrm-backend/wiki
.. _documentation: https://routingpy.readthedocs.io/en/latest
.. _routing-py.routers: https://routingpy.readthedocs.io/en/latest/#module-routingpy.routers
.. _Apache 2.0 License: https://github.com/gis-ops/routing-py/blob/master/LICENSE
.. _mybinder.org: https://mybinder.org/v2/gh/gis-ops/routing-py/master?filepath=examples
.. _poetry: https://github.com/sdispater/poetry
