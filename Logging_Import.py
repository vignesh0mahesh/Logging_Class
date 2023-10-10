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
        try:
            
            handler = logging_loki.LokiHandler(
                url=url, 
                version="1",
            )
            self.loki_logger.addHandler(handler)

            self.system_tag = system_name
            self.user_tag = os.environ['USERNAME']
            self.default_tag = {"SYSTEM": "", "USER": "", "MODULE": "", "CLASS": "", "FUNCTION": ""}
            self.tags = self.default_tag
            self.append_tags({"SYSTEM": self.system_tag, "USER": self.user_tag})
            self.log_upload = True

        except:
            print(color('Log Function Import Unsucessfull', fg='red', style='bold'))

    def append_tags(self, tags):
        for key in tags:
            self.tags[key] = tags[key]

    def module_tag(self, module_name):
        self.append_tags({"MODULE": module_name})

    def class_tag(self, class_name):
        self.append_tags({"CLASS": class_name})

    def function_tag(self, function_name):
        self.append_tags({"FUNCTION": function_name})

    def debug(self, debug_string: str):

        caller_frame = inspect.stack()[1]

        self.module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self.class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self.function_tag(caller_frame[0].f_code.co_name)
        
        if self.log_upload:
            self.loki_logger.debug(debug_string, extra={"tags": self.tags})
            
        if self.debugging:
            ic.configureOutput(prefix=f"CLASS: {self.tags['CLASS']} - FUNCTION: {self.tags['FUNCTION']} - MODULE: {self.tags['MODULE']} - DEBUG_")
            MESSAGE = debug_string
            self.logger.debug(ic(MESSAGE))
            
        else:
            self.logger.debug(debug_string)
        

    def info(self, info_string: str):

        caller_frame = inspect.stack()[1]

        self.module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self.class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self.function_tag(caller_frame[0].f_code.co_name)
        
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
            

    def warning(self, warn_string):

        caller_frame = inspect.stack()[1]

        self.module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self.class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self.function_tag(caller_frame[0].f_code.co_name)

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

    def error(self, err_string):
        
        caller_frame = inspect.stack()[1]

        self.module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self.class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self.function_tag(caller_frame[0].f_code.co_name)

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
            
    
    def critical(self, crit_string):

        caller_frame = inspect.stack()[1]

        self.module_tag(inspect.getmodule(caller_frame[0]).__name__)

        self.class_tag(caller_frame[0].f_locals.get('self', None).__class__.__name__)

        self.function_tag(caller_frame[0].f_code.co_name)

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
