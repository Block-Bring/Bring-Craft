import sys
import logging
import threading
from colorama import Fore, Style, init

init()

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
    }
    def format(self, record):
        record = logging.makeLogRecord(record.__dict__)
        if record.levelname in self.COLORS:
            record.levelname = self.COLORS[record.levelname] + record.levelname + Style.RESET_ALL
        return super().format(record)


# ---------- 新增过滤器，用于控制台开关 ----------
class ConsoleFilter(logging.Filter):
    def filter(self, record):
        # 只有 record 中 console 属性为 True 时才输出到控制台
        return getattr(record, 'console', False)


class EasyLogger:
    def __init__(self, log_file=None):
        self.logger = logging.getLogger('BringMigrator')
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            # 控制台处理器（带颜色）
            console = logging.StreamHandler(sys.stdout)
            console.setLevel(logging.DEBUG)
            console.setFormatter(ColoredFormatter(
                '[%(asctime)s] [%(thread_name)s/%(levelname)s] %(message)s',
                datefmt='%y/%m/%d %H:%M:%S'
            ))
            # 添加过滤器，控制是否输出到控制台
            console.addFilter(ConsoleFilter())
            self.logger.addHandler(console)

            # 文件处理器（纯文本，不加过滤器，始终输出）
            if log_file:
                file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(logging.Formatter(
                    '[%(asctime)s] [%(thread_name)s/%(levelname)s] %(message)s',
                    datefmt='%y/%m/%d %H:%M:%S'
                ))
                self.logger.addHandler(file_handler)

    # 修改 _log 方法，增加 console 参数
    def _log(self, level, msg, thread_name=None, console=False):
        extra = {
            'thread_name': thread_name or threading.current_thread().name,
            'console': console   # 将控制台开关放入 extra
        }
        self.logger.log(level, msg, extra=extra)

    # 修改各个便捷方法，增加 console 参数
    def info(self, msg, thread_name=None, console=False):
        self._log(logging.INFO, msg, thread_name, console)

    def warning(self, msg, thread_name=None, console=False):
        self._log(logging.WARNING, msg, thread_name, console)

    def error(self, msg, thread_name=None, console=False):
        self._log(logging.ERROR, msg, thread_name, console)

if __name__ == '__main__':
    logger = EasyLogger('log.txt')
    logger.info('hello world', "NoneThread", True)
    logger.warning('hello world')
    logger.error('hello world')