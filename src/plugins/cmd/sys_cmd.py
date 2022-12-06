from subprocess import Popen, PIPE
from html import unescape


def help() -> str:
    return (
        "调用系统命令行\n"
        "⚠危险操作, 谨慎使用!\n\n"
        "/cmd {命令}\n"
        "For example:\n"
        "/cmd echo \"Hello World\""
    )


def shell(opt: str) -> str:

    if not opt:
        return "发送 /cmd.help 获取帮助"

    if opt == ".help":
        return help()

    content = Popen(
        unescape(opt.strip()),
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        universal_newlines=True
    ).communicate()

    if content == ('',''):
        msg = "执行完毕, 没有任何输出呢~"
    elif content[1] == '':
        msg = f"stdout:\n{content[0]}\n>执行完毕"
    elif content[0] == '':
        msg = f"stderr:\n{content[1]}"
    else :
        msg = f"stdout:\n{content[0]}\nstderr:\n{content[1]}\n>执行完毕"
    return msg


