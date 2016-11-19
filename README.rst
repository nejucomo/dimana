========================
_DIM_ensional _ANA_lysis
========================

A python library for tracking and verifying dimensional units of measure.

For background see the `dimensional analysis wikipedia entry`_.

.. _`dimensional analysis wikipedia entry`: https://en.wikipedia.org/wiki/Dimensional_analysis

Examples
========

Dimana values can be parse with the ``Value.parse`` classmethod:

.. code:: python

   >>> from dimana.value import Value
   >>> reward = Value.parse('12.5 [BTC]')
   >>> reward
   <Value '12.5 [BTC]'>

Values track their units through arithmetic operations:

.. code:: python

   >>> time = Value.parse('10 [min]')
   >>> reward / time
   <Value '1.25 [BTC / min]'>

Incoherent operations raise exceptions:

.. code:: python

   >>> reward + time
   Traceback (most recent call last):
     ...
   Mismatch: Units mismatch: 'BTC' vs 'min'
