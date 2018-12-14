import logging

"""
Logging levels supported by this program.
"""
Log_levels = dict(CRITICAL=logging.CRITICAL, FATAL=logging.FATAL, ERROR=logging.ERROR, WARN=logging.WARNING, WARNING=logging.WARNING, INFO=logging.INFO, DEBUG=logging.DEBUG)
"""
Log level to use for any loggers created by this module.
"""
"""
    Define logging based on what logging level the user provides.
    When provided with None, logs will be dropped in the nearest class-D star.

    :param log_level: Logging level to log with
    :param log_level: Logging level to log with
    :type log_level: str
    :param log_to_console: If the log contents should also be routed to the console
    :type log_to_console: bool
"""
_global_log_level: str = logging.DEBUG


def setup_loggers(log_level):

	global _global_log_level
	logging.getLogger().addHandler(logging.StreamHandler())

	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	script_logger = logging.getLogger('script')
	script_logger.setLevel(logging.DEBUG)
	lh = logging.FileHandler('script.log')
	lh.setFormatter(formatter)
	lh.setLevel(logging.DEBUG)
	script_logger.addHandler(lh)
	script_logger.debug('Defined global log level as %s', log_level)

	if log_level is None:
		return
	_global_log_level = Log_levels[log_level.upper()]

	#websocket logger

	ws_logger = logging.getLogger('websockets')
	ws_logger.setLevel(logging.DEBUG)
	wh = logging.FileHandler('websockets.log')
	wh.setFormatter(formatter)
	wh.setLevel(logging.DEBUG)
	ws_logger.addHandler(wh)

	# Controller specific
	c_logger = logging.getLogger('controller')
	c_logger.setLevel(logging.DEBUG)
	ch = logging.FileHandler('controller.log')
	ch.setFormatter(formatter)
	ch.setLevel(logging.DEBUG)
	c_logger.addHandler(ch)


def get_logger(logger):
	"""
	Obtain a logger.

	:param logger: Logging to obtain
	:type logger: str
	:returns logger for the requested channel
	:rtype Logger
	"""

	# Whenever no log level has been defined, logging for controller should just go to /dev/null
	if _global_log_level is None and logger is 'controller':
		return logging.getLogger('dummy')
	else:
		return logging.getLogger(logger)
