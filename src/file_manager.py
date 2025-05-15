"""
Команды:
  ls [path]                — показать содержимое каталога
  cd <path>                — перейти в подкаталог
  pwd                      — вывести текущий каталог
  mkdir <name>             — создать директорию
  rmdir <name>             — удалить ПУСТУЮ директорию
  touch <file>             — создать пустой файл
  cat <file>               — вывести содержимое файла
  write <file> <mode>      — записать текст в файл (mode = w|a)
  rm <file>                — удалить файл
  cp <src> <dst>           — скопировать файл
  mv <src> <dst>           — переместить/переименовать
  help                     — справка
  exit                     — выход
"""

import sys
import shutil
import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("config.ini")
cfg = configparser.ConfigParser()
cfg.read(CONFIG_PATH, encoding="utf-8")
ROOT = (Path(CONFIG_PATH).parent / cfg["DEFAULT"]["root_dir"]).resolve()
ROOT.mkdir(exist_ok=True)

current = ROOT  # текущий каталог


def inside_root(path: Path) -> bool:
    """Проверяем, находится ли путь внутри рабочей директории."""
    try:
        path.resolve().relative_to(ROOT)
        return True
    except ValueError:
        return False


def safe_path(path_str: str) -> Path:
    """Преобразуем строку в Path и гарантируем, что он в пределах ROOT."""
    p = (current / path_str).resolve()
    if not inside_root(p):
        print("Отказано: выход за пределы рабочей директории.")
        raise ValueError
    return p


def cmd_ls(args):
    target = safe_path(args[0]) if args else current
    for item in target.iterdir():
        marker = "/" if item.is_dir() else ""
        print(item.name + marker)


def cmd_cd(args):
    global current
    if not args:
        print("cd <path>")
        return
    dest = safe_path(args[0])
    if dest.is_dir():
        current = dest
    else:
        print("Не каталог")


def cmd_pwd(_):
    print(current.relative_to(ROOT))


def cmd_mkdir(args):
    for name in args:
        safe_path(name).mkdir(exist_ok=True)


def cmd_rmdir(args):
    for name in args:
        p = safe_path(name)
        try:
            p.rmdir()
        except OSError as e:
            print(f"Ошибка удаления {p.name}: {e}")


def cmd_touch(args):
    for name in args:
        safe_path(name).touch(exist_ok=True)


def cmd_cat(args):
    for name in args:
        p = safe_path(name)
        try:
            print(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(e)


def cmd_write(args):
    if len(args) < 2:
        print("write <file> <w|a>")
        return
    file, mode = args[0], args[1]
    p = safe_path(file)
    if mode not in ("w", "a"):
        print("mode должен быть w или a")
        return
    print("Введите текст. Завершите пустой строкой:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    text = "\n".join(lines) + "\n"
    if mode == "w":
        p.write_text(text, encoding="utf-8")
    else:  # append
        p.write_text(p.read_text(encoding="utf-8") + text, encoding="utf-8")


def cmd_rm(args):
    for name in args:
        p = safe_path(name)
        if p.is_file():
            p.unlink()
        else:
            print("Не файл")


def cmd_cp(args):
    if len(args) != 2:
        print("cp <src> <dst>")
        return
    src = safe_path(args[0])
    dst = safe_path(args[1])
    shutil.copy2(src, dst)


def cmd_mv(args):
    if len(args) != 2:
        print("mv <src> <dst>")
        return
    src = safe_path(args[0])
    dst = safe_path(args[1])
    shutil.move(src, dst)


def cmd_help(_=None):
    print(__doc__)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "pwd": cmd_pwd,
    "mkdir": cmd_mkdir,
    "rmdir": cmd_rmdir,
    "touch": cmd_touch,
    "cat": cmd_cat,
    "write": cmd_write,
    "rm": cmd_rm,
    "cp": cmd_cp,
    "mv": cmd_mv,
    "help": cmd_help,
    "exit": lambda _: sys.exit(0),
}


def main():
    print("Файловый менеджер. help — список команд.")
    while True:
        try:
            raw = input(f"[{current.relative_to(ROOT)}]$ ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        parts = raw.split()
        cmd, *args = parts
        func = COMMANDS.get(cmd)
        if func:
            try:
                func(args)
            except ValueError:
                pass
            except Exception as e:
                print("Ошибка:", e)
        else:
            print("Неизвестная команда. help — помощь.")


if __name__ == "__main__":
    main()
