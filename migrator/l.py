import os
from urllib.parse import urlparse
import time
from packaging.version import parse
# 简化设置标题
def title(line_title: str):
    os.system(f'title {line_title}' if os.name == 'nt' else None)

def version_compare(v1, v2):
    return parse(v1) < parse(v2)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(seconds = None):
    if seconds is not None:
        try:
            seconds_int = int(seconds)
            while seconds_int > 0:
                print(f"{seconds_int} 秒后继续...", end="\r")
                time.sleep(1)
                seconds_int -= 1
            return
        except Exception:
            return
    input("按 Enter 键继续...")

def stop(seconds = None):
    if seconds is not None:
        try:
            seconds_int = int(seconds)
            while seconds_int > 0:
                print(f"{seconds_int} 秒后结束...", end="\r")
                time.sleep(1)
                seconds_int -= 1
            return
        except Exception:
            return
    input("按 Enter 键结束")

def is_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


if __name__ == "__main__":
    # 不进行任何操作
    title("Fast Execute")