# 日志系统

import logging
from logging import handlers


class Logger(object):

    """
    日志系统使用方法：
    demo1：Logger().getLogger().info("info")
    demo2：Logger(logLevel='error').getLogger().error("error")
    """

    # 字典存储日志级别映射
    format_dict = {
        # 10
        'debug': logging.DEBUG,
        # 20
        'info': logging.INFO,
        # 30
        'warning': logging.WARNING,
        # 40
        'error': logging.ERROR,
        # 50
        'critical': logging.CRITICAL
    }

    def __init__(self, fileName='info', logLevel='info', when='D', backCount=365, format='%(asctime)s - %(thread)d - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        """
        :param fileName: 文件名，和下面的根据日志级别来设置文件名是有重冲突的
        :param logLevel: 日志级别
        :param when: 输出到文件时的参数：按时间来切割文件
        :param backCount: 输出到文件时的参数：文件保留数量
        :param format: 日志格式化
        """

        # 根据日志级别来设置文件名，设置两种类型的文件，info.log 和 error.log
        if logLevel == 'error':
            fileName = 'error.log'
        else:
            fileName = 'info.log'
        # 创建一个logger
        self.logger = logging.getLogger(fileName)
        # 设置日志级别
        self.logger.setLevel(self.format_dict.get(logLevel))

        # 格式化
        formatter = logging.Formatter(format)

        # 创建一个handler写入日志文件，并且按照天来分割日志文件
        # fh = logging.FileHandler(file_name)
        # fh.setFormatter(formatter)
        th = handlers.TimedRotatingFileHandler(filename=fileName, when=when, backupCount=backCount, encoding='utf-8')
        th.setFormatter(formatter)
        """
        实例化 TimedRotatingFileHandler：
        when 是文件分割的间隔时间，S、M、H、D==MIDNIGHT、W，分别代表每秒、每分钟、每小时、每天、每周进行分割
        backupCount 代表有效个数，超过则删除
        """

        # 创建一个handler输出至控制台
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(th)
        self.logger.addHandler(sh)

    def getLogger(self):
        return self.logger
