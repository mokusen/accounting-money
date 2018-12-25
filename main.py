from method.dbInit import dbInit
from method.gui import mainGui
from method.utils import logger, logFileLimit

logger = logger.set_operate_logger(__name__)

logFileLimit.check_logfile()
dbInit.db_init()
logger.info("START chms")
mainGui.call_mainGui()
logger.info("END chms")
logFileLimit.check_logfile()
