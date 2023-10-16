import sys
import os
import inspect
import time
import logging
import logging_loki
from datetime import datetime
from icecream import ic
from colors import *

class LogUpload:
    def __init__(self, log_name, log_level='Print'):
        """This is the initialization function for the Log Upload Class

        Args:
            log_name (str): Enter the name you would like the log file to have.
            log_level (str, optional): Enter the type of logging you would like to see. Options Are: 'Silent' , 'Print' or 'Debug'. Defaults to 'Print'.
        """
        # log_level = 'Silent' , 'Print' or 'Debug'
        
        log_file = datetime.now().strftime("%d_%m_%Y-%H-%M-%S") + f"_{log_name}_{log_level}_Log.log"
        
        self.logger = logging.getLogger(f"{log_name}_Log")
        self.loki_logger = logging.getLogger(f"{log_name}_Log")
        self.print_output = False
        self.debugging = False
        
        if log_level == 'Silent':
            logging.basicConfig(level=logging.INFO, filename=log_file, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
            self.print_output = False
            self.debugging = False
            
        elif log_level == 'Print':
            logging.basicConfig(level=logging.INFO, filename=log_file, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
            self.print_output = True
            self.debugging = False
            
        elif log_level == 'Debug':
            logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
            self.print_output = False
            self.debugging = True
        
        else:
            print(color("Invalid Log Level Parameter, Options Are: 'Silent' , 'Print' or 'Debug'", fg='red', style='bold'))
            print(color("Now EXITING", fg='red', style='italic'))
            exit()
            
        self.log_upload = False
        self.tags = {"MODULE": "", "CLASS": "", "FUNCTION": ""}
        
        print(color("Logging Class Sucessfully Imported", fg='green'))
        
    def initialize_loki(self, url, system_name):
        """This function is used to initialize a connection to your loki logging server. 

        Args:
            url (str): Enter the url to your loki logging server instance, should be in the following format : "https://my-loki-instance/loki/api/v1/push"
            system_name (str): Enter a name that will be used as a tag for your system, so that you can filter for this specific system in Grafana Loki. 
        """
        try:
            
            handler = logging_loki.LokiHandler(url=url, version="1",)
            self.loki_logger.addHandler(handler)

            self.system_tag = system_name
            self.user_tag = os.environ['USERNAME']
            self.default_tag = {"SYSTEM": "", "USER": "", "MODULE": "", "CLASS": "", "FUNCTION": ""}
            self.tags = self.default_tag
            self._append_tags({"SYSTEM": self.system_tag, "USER": self.user_tag})
            self.log_upload = True
            print(color('Loki Logging Initialized', fg='green'))

        except:
            print(color('Log Function Import Unsuccessful', fg='red', style='bold'))

    def _append_tags(self, tags):
        """This is an internal function that appends tags from tag functions below. If you want to add more custom tags, invoke this function.

        Args:
            tags (dict): Dictionary with {tag name: tag value format}
        """
        for key in tags:
            self.tags[key] = tags[key]

    def _module_tag(self, module_name):
        """Appends the module (if exists) from which this log function is called from in your code to the tag. Automatically generated, not user defined. 

        Args:
            module_name (str): Name of the module the log function is being called from
        """
        self._append_tags({"MODULE": module_name})

    def _class_tag(self, class_name):
        """Appends the class (if exists) from which this log function is called from in your code to the tag. Automatically generated, not user defined.

        Args:
            class_name (str): Name of the class the log function is being called from
        """
        self._append_tags({"CLASS": class_name})

    def _function_tag(self, function_name):
        """Appends the function (if exists) from which this log function is called from in your code to the tag. Automatically generated, not user defined.

        Args:
            function_name (str): Name of the function the log function is being called from
        """
        self._append_tags({"FUNCTION": function_name})

    def debug(self, debug_string: str):
        """To log a debug level message

        Args:
            debug_string (str): Message to log
        """

        caller_frame = inspect.stack()[1]

        self._module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self._class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self._function_tag(caller_frame[0].f_code.co_name)
        
        if self.log_upload:
            self.loki_logger.debug(debug_string, extra={"tags": self.tags})
            
        if self.debugging:
            ic.configureOutput(prefix=f"CLASS: {self.tags['CLASS']} - FUNCTION: {self.tags['FUNCTION']} - MODULE: {self.tags['MODULE']} - DEBUG_")
            MESSAGE = debug_string
            self.logger.debug(ic(MESSAGE))
            
        else:
            self.logger.debug(debug_string)

    def info(self, info_string: str):
        """To log a info level message

        Args:
            info_string (str): Message to log
        """

        caller_frame = inspect.stack()[1]

        self._module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self._class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self._function_tag(caller_frame[0].f_code.co_name)
        
        if self.log_upload:
            self.loki_logger.info(info_string, extra={"tags": self.tags})

        if self.print_output:
            print(color(info_string, fg='blue'))
            
        if self.debugging:
            ic.configureOutput(prefix=f"CLASS: {self.tags['CLASS']} - FUNCTION: {self.tags['FUNCTION']} - MODULE: {self.tags['MODULE']} - INFO_")
            MESSAGE = info_string
            self.logger.info(ic(MESSAGE))
            
        else:
            self.logger.info(info_string)

    def warning(self, warn_string: str):
        """To log a warning level message

        Args:
            warn_string (str): Message to log
        """

        caller_frame = inspect.stack()[1]

        self._module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self._class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self._function_tag(caller_frame[0].f_code.co_name)

        if self.log_upload:
            self.loki_logger.warning(warn_string, extra={"tags": self.tags})

        if self.print_output:
            print(color(f"Warning: {warn_string}", fg=3, style='underline'))
            
        if self.debugging:
            ic.configureOutput(prefix=f"CLASS: {self.tags['CLASS']} - FUNCTION: {self.tags['FUNCTION']} - MODULE: {self.tags['MODULE']} - WARNING_")
            MESSAGE = warn_string
            self.logger.warning(ic(MESSAGE))
            
        else:
            self.logger.warning(warn_string)

    def error(self, err_string: str):
        """To log a error level message

        Args:
            err_string (str): Message to log
        """
        
        caller_frame = inspect.stack()[1]

        self._module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self._class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self._function_tag(caller_frame[0].f_code.co_name)

        if self.log_upload:
            self.loki_logger.error(err_string, extra={"tags": self.tags})

        if self.print_output:
            print(color(f"ERROR: {err_string}", fg=196, style='bold'))
            
        if self.debugging:
            ic.configureOutput(prefix=f"CLASS: {self.tags['CLASS']} - FUNCTION: {self.tags['FUNCTION']} - MODULE: {self.tags['MODULE']} - ERROR_")
            MESSAGE = err_string
            self.logger.error(ic(MESSAGE))
            
        else:
            self.logger.error(err_string)

    def critical(self, crit_string: str):
        """To log a critical level message

        Args:
            crit_string (str): Message to log
        """

        caller_frame = inspect.stack()[1]

        self._module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self._class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self._function_tag(caller_frame[0].f_code.co_name)

        if self.log_upload:
            self.loki_logger.critical(crit_string, extra={"tags": self.tags})

        if self.print_output:
            print(color(f"CRITICAL: {crit_string}", fg=200, style='bold+underline'))
            
        if self.debugging:
            ic.configureOutput(prefix=f"CLASS: {self.tags['CLASS']} - FUNCTION: {self.tags['FUNCTION']} - MODULE: {self.tags['MODULE']} - CRITICAL_")
            MESSAGE = crit_string
            self.logger.critical(ic(MESSAGE))
            
        else:
            self.logger.critical(crit_string)


### ------------------------------- USAGE ------------------------------- ###

# log = LogUpload('Test', 'Print') # Options Are: 'Silent' , 'Print' or 'Debug'" Default is 'Print'
# log.debug("This is a Debug Message")
# log.info("This is Info Message")
# log.warning("This is a Warning Message")
# log.error("This is a Error Message")
# log.critical("This is a Critical Message")
