import logging

level = logging.DEBUG
format = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s"
log_file = r"/log/netCloud.log"
logging.basicConfig(level=level, format=format, filename=log_file, filemode='w')
