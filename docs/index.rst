Welcome to routingpy's documentation!
=====================================

:Documentation: https://routingpy.readthedocs.io/
:Source Code: https://github.com/mthh/routingpy
:Issue Tracker: https://github.com/mthh/routingpy/issues
:PyPI: https://pypi.org/project/routingpy
:MyBinder Interactive Examples: https://mybinder.org/v2/gh/mthh/routingpy/master?filepath=examples

.. automodule:: routingpy
   :members: __doc__

.. toctree::
    :maxdepth: 4
    :caption: Contents

    index


Installation
~~~~~~~~~~~~

::

    pip install routingpy

Routers
~~~~~~~

.. automodule:: routingpy.routers
   :members: __doc__

.. autofunction:: routingpy.routers.get_router_by_name

Default Options Object
----------------------

.. autoclass:: routingpy.routers.options
   :members:
   :undoc-members:

Google
------

.. autoclass:: routingpy.routers.Google
   :members:

   .. automethod:: __init__

Graphhopper
-----------

.. autoclass:: routingpy.routers.Graphhopper
   :members:

   .. automethod:: __init__

HereMaps
--------

.. autoclass:: routingpy.routers.HereMaps
   :members:

   .. automethod:: __init__

MapboxOSRM
----------

.. autoclass:: routingpy.routers.MapboxOSRM
   :members:

   .. automethod:: __init__

OpenTripPlannerV2
-----------------

.. autoclass:: routingpy.routers.OpenTripPlannerV2
   :members:
   :inherited-members:
   :show-inheritance:

   .. automethod:: __init__

ORS
---

.. autoclass:: routingpy.routers.ORS
   :members:

   .. automethod:: __init__

OSRM
----

.. autoclass:: routingpy.routers.OSRM
   :members:

   .. automethod:: __init__

Valhalla
--------

.. autoclass:: routingpy.routers.Valhalla
   :members:

   .. automethod:: __init__

Client
~~~~~~~
.. autoclass:: routingpy.client_default.Client
    :members:

    .. automethod:: __init__

Data
~~~~

.. autoclass:: routingpy.direction.Directions
    :members: raw

.. autoclass:: routingpy.direction.Direction
    :members: geometry, duration, distance, km, mi

.. autoclass:: routingpy.optimized.OptimizedDirection
    :members: geometry, duration, distance, km, mi, original_index

.. autoclass:: routingpy.isochrone.Isochrones
    :members: raw

.. autoclass:: routingpy.isochrone.Isochrone
    :members: geometry, center, range

.. autoclass:: routingpy.matrix.Matrix
    :members: durations, distances, raw

.. autoclass:: routingpy.expansion.Expansions
    :members: expansions, center, raw

.. autoclass:: routingpy.expansion.Edge
    :members: geometry, distance, duration, cost, edge_id, status

.. autofunction:: routingpy.utils.decode_polyline5

.. autofunction:: routingpy.utils.decode_polyline6

Exceptions
~~~~~~~~~~

.. autoclass:: routingpy.exceptions.RouterError
    :show-inheritance:

.. autoclass:: routingpy.exceptions.RouterApiError
    :show-inheritance:

.. autoclass:: routingpy.exceptions.RouterServerError
    :show-inheritance:

.. autoclass:: routingpy.exceptions.RouterNotFound
    :show-inheritance:

.. autoclass:: routingpy.exceptions.Timeout
    :show-inheritance:

.. autoclass:: routingpy.exceptions.RetriableRequest
    :show-inheritance:

.. autoclass:: routingpy.exceptions.OverQueryLimit
    :show-inheritance:

Changelog
~~~~~~~~~

See our `Changelog.md`_.

.. _Changelog.md: https://github.com/mthh/routingpy/CHANGELOG.md

Indices and search
==================

* :ref:`genindex`
* :ref:`search`
