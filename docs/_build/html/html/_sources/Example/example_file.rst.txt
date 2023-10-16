Example Usage
+++++++++++++++++++++++++++++++++

::
    
    import sys
    sys.path.insert(0, r"<Location of Repo>")
    from Logging_Import import *

    log = LogUpload('Test', 'Print') # Default is 'Print'

    log.debug("This is a Debug Message")

    log.info("This is Info Message")

    log.warning("This is a Warning Message")

    log.error("This is a Error Message")

    log.critical("This is a Critical Message")