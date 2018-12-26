def init_check_process():
    from method.utils import logFileExist
    logFileExist.exist_csv_log_directory()


def main():
    from method.gui import mainGui
    from method.dbInit import dbInit
    from method.utils import chms_logger, logFileLimit

    logger = chms_logger.set_operate_logger(__name__)

    logFileLimit.check_logfile()
    dbInit.db_init()
    logger.info("START chms")
    mainGui.call_mainGui()
    logFileLimit.check_logfile()
    logger.info("END chms")


if __name__ == "__main__":
    init_check_process()
    main()
