import logging
import sys
from datetime import datetime
from typing import Any, Dict

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',    
        'INFO': '\033[32m',     
        'WARNING': '\033[33m',  
        'ERROR': '\033[31m',    
        'CRITICAL': '\033[35m', 
        'RESET': '\033[0m'      
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        
        if hasattr(record, 'layer'):
            record.layer = f"[{record.layer}]"
        else:
            record.layer = ""
            
        return super().format(record)

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = ColoredFormatter(
        '%(asctime)s %(layer)s %(levelname)s [%(name)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

class LayerLogger:
    
    def __init__(self, layer_name: str):
        self.layer_name = layer_name
        self.logger = setup_logger(f"netscout.{layer_name}")
    
    def _log_with_layer(self, level: str, message: str, **kwargs):
        extra = {'layer': self.layer_name.upper()}
        getattr(self.logger, level)(message, extra=extra, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self._log_with_layer('debug', message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self._log_with_layer('info', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log_with_layer('warning', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log_with_layer('error', message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log_with_layer('critical', message, **kwargs)

controller_logger = LayerLogger("controller")
service_logger = LayerLogger("service")
repository_logger = LayerLogger("repository")
database_logger = LayerLogger("database")

def log_function_entry(logger: LayerLogger, func_name: str, **params):
    params_str = ", ".join([f"{k}={v}" for k, v in params.items()])
    logger.info(f"🚀 {func_name}({params_str}) - BAŞLADI")

def log_function_exit(logger: LayerLogger, func_name: str, result: Any = None):
    if result is not None:
        logger.info(f"✅ {func_name}() - TAMAMLANDI: {type(result).__name__}")
    else:
        logger.info(f"✅ {func_name}() - TAMAMLANDI")

def log_database_query(query: str, params: Dict = None):
    if params:
        database_logger.debug(f"🗄️  SQL: {query} | Params: {params}")
    else:
        database_logger.debug(f"🗄️  SQL: {query}")