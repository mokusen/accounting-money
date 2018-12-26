def check():
    from method.utils import logFileLimit
    logFileLimit.check_logfile()


def main():
    from method.gui import mainGui
    from method.dbInit import dbInit
    from method.utils import logger

    logger = logger.set_operate_logger(__name__)

    dbInit.db_init()
    logger.info("START chms")
    mainGui.call_mainGui()
    logger.info("END chms")
    check()


if __name__ == "__main__":
    check()
    main()
