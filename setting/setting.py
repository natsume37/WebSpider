
import logging.config
import os

# 动态获取项目根目录，假设项目目录与当前脚本在同一层级
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取父级目录作为项目根目录
print(BASE_DIR)
INFO_LOG_DIR = os.path.join(BASE_DIR, "log", 'info.log')
ERROR_LOG_DIR = os.path.join(BASE_DIR, "log", 'error.log')
print(INFO_LOG_DIR)
# 确保日志目录存在
os.makedirs(os.path.dirname(INFO_LOG_DIR), exist_ok=True)
os.makedirs(os.path.dirname(ERROR_LOG_DIR), exist_ok=True)

LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # 日志格式
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s [%(name)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'test': {
            'format': '%(asctime)s %(message)s',
        },
    },
    'filters': {},
    # 日志处理器
    'handlers': {
        'console_debug_handler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_info_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': INFO_LOG_DIR,
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'file_debug_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': ERROR_LOG_DIR,
            'encoding': 'utf-8',
            'formatter': 'test',
        },
    },
    'loggers': {
        'logger1': {
            'handlers': ['console_debug_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'logger2': {
            'handlers': ['console_debug_handler', 'file_info_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console_debug_handler', 'file_debug_handler'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(LOGGING_DIC)

# 使用
logging1 = logging.getLogger("logger2")

