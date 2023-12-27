Miner API
=========

.. py:module:: web3.bub.miner

The ``web3.bub.miner`` object exposes methods to interact with the RPC APIs under
the ``miner_`` namespace that are supported by the Bub client.


Methods
-------

The following methods are available on the ``web3.bub.miner`` namespace.


.. py:method:: NodeMiner.make_dag(number)

    * Delegates to ``miner_makeDag`` RPC Method

    Generate the DAG for the given block number.

    .. code-block:: python

        >>> web3.bub.miner.make_dag(10000)


.. py:method:: NodeMiner.makeDAG(number)

   .. warning:: Deprecated: This method is deprecated in favor of
      :meth:`~NodeMiner.make_dag`


.. py:method:: NodeMiner.set_extra(extra)

    * Delegates to ``miner_setExtra`` RPC Method

    Set the 32 byte value ``extra`` as the extra data that will be included
    when this node mines a block.

    .. code-block:: python

        >>> web3.bub.miner.set_extra('abcdefghijklmnopqrstuvwxyzABCDEF')

.. py:method:: NodeMiner.setExtra(extra)

   .. warning:: Deprecated: This method is deprecated in favor of
      :meth:`~NodeMiner.set_extra`


.. py:method:: NodeMiner.set_gas_price(gas_price)

    * Delegates to ``miner_setGasPrice`` RPC Method

    Sets the minimum accepted gas price that this node will accept when mining
    transactions.  Any transactions with a gas price below this value will be
    ignored.

    .. code-block:: python

        >>> web3.bub.miner.set_gas_price(19999999999)


.. py:method:: NodeMiner.setGasPrice(gas_price)

   .. warning:: Deprecated: This method is deprecated in favor of
      :meth:`~NodeMiner.set_gas_price`


.. py:method:: NodeMiner.start(num_threads)

    * Delegates to ``miner_start`` RPC Method

    Start the CPU mining process using the given number of threads.

    .. code-block:: python

        >>> web3.bub.miner.start(2)


.. py:method:: NodeMiner.stop()

    * Delegates to ``miner_stop`` RPC Method

    Stop the CPU mining operation

    .. code-block:: python

        >>> web3.bub.miner.stop()


.. py:method:: NodeMiner.start_auto_dag()

    * Delegates to ``miner_startAutoDag`` RPC Method

    Enable automatic DAG generation.

    .. code-block:: python

        >>> web3.bub.miner.start_auto_dag()

.. py:method:: NodeMiner.startAutoDag()

   .. warning:: Deprecated: This method is deprecated in favor of
      :meth:`~NodeMiner.start_auto_dag`


.. py:method:: NodeMiner.stop_auto_dag()

    * Delegates to ``miner_stopAutoDag`` RPC Method

    Disable automatic DAG generation.

    .. code-block:: python

        >>> web3.bub.miner.stop_auto_dag()

.. py:method:: NodeMiner.stopAutoDag()

   .. warning:: Deprecated: This method is deprecated in favor of
      :meth:`~NodeMiner.stop_auto_dag`
