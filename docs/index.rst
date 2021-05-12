.. AI Trading documentation master file, created by
   sphinx-quickstart on Sat May  8 12:49:50 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AI Trading
-----------

|Logo|

`TensorTrade`_ is an open source Python framework for building,
training, evaluating, and deploying robust trading algorithms using
reinforcement learning. The framework focuses on being highly composable
and extensible, to allow the system to scale from simple trading
strategies on a single CPU, to complex investment strategies run on a
distribution of HPC machines.



Guiding principles
------------------

*Inspired by* `Keras' guiding principles`_.

*User friendliness.* TensorTrade is an API designed for human beings,
not machines. It puts user experience front and center. TensorTrade
follows best practices for reducing cognitive load: it offers consistent
& simple APIs, it minimizes the number of user actions required for
common use cases, and it provides clear and actionable feedback upon
user error.

*Modularity.* A trading environment is a conglomeration of fully
configurable modules that can be plugged together with as few
restrictions as possible. In particular, exchanges, feature pipelines,
action schemes, reward schemes, trading agents, and performance reports
are all standalone modules that you can combine to create new trading
environments.

*Easy extensibility.* New modules are simple to add (as new classes and
functions), and existing modules provide ample examples. To be able to
easily create new modules allows for total expressiveness, making
TensorTrade suitable for advanced research and production use.

.. _TensorTrade: https://github.com/notadamking/tensortrade
.. _Medium tutorial: https://medium.com/@notadamking/trade-smarter-w-reinforcement-learning-a5e91163f315
.. _Keras' guiding principles: https://github.com/keras-team/keras

.. |Logo| image:: _static/logo.jpg


Welcome to AI Trading's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/overview.md
   source/installation.md
   source/drl_models.md
   source/sample_data.md
   source/cryptocurrency_data.md
   source/forex_data.md
   source/stock_data.md
   source/reference.md

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
