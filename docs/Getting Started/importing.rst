Importing The Class
+++++++++++++++++++

To import the class into your code:
::

    import sys
    sys.path.insert(0, r"<Location of Repo>")
    from Logging_Import import *

Initializing The Class
++++++++++++++++++++++++

To initialize the class, instantiate ``log`` as a global variable,
::

    log = LogUpload('<ENTER LOG FILE NAME>', 'ENTER LOGGING LEVEL')

The first parameter ``<ENTER LOG FILE NAME>`` is the name of which your log file will be saved.
It will have the following naming convention: ``%d_%m_%Y-%H-%M-%S_<LOG FILE NAME>_<LOGGING LEVEL>_Log.log``

The second parameter is the Logging Level, there are 3 options to choose from:

#. ``'Silent'``
    * Logs **will not** be printed in the Python Terminal, logs will be published in the log file, and uploaded to Grafana Loki if it is initialized (below). 
    * This is equivalent to choosing a logging level of ``logging.INFO``
#. ``'Print'`` 
    * Logs **will** be printed in the Python Terminal, logs will be published in the log file, and uploaded to Grafana Loki if it is initialized (below).
    * This is equivalent to choosing a logging level of ``logging.INFO``
#. ``'Debug'``
    * Logs **will** be printed in the Python Terminal, logs will be published in the log file and uploaded to Grafana Loki if it is initialized (below). 
    * This is equivalent to choosing a logging level of ``Level=logging.DEBUG``

If no parameter is given default is ``'Print'`` 

Enabling Loki Logging
+++++++++++++++++++++
After initializing the class run the following command:
::

    initialize_loki(url, system_name)

The first parameter ``url`` is the Loki URL, it should be in the following format: "https://my-loki-instance/loki/api/v1/push"

The second parameter ``system_name`` is added as a tag so that you can filter for this specific system in Grafana Loki. 

.. autofunction:: Logging_Import.LogUpload.initialize_loki

To learn more about Loki Logging go 
`here <https://grafana.com/oss/loki/>`_