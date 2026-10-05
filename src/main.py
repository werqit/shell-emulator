import csv
import shlex
import sys
import time


ARGUMENT_COUNT = 3
ROOT_PATH = "/"


def parse_command(command):
    return shlex.split(command)


def load_vfs(vfs_path):
    vfs = {}

    try:
        with open(vfs_path, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                vfs[row["path"]] = row["type"]

    except FileNotFoundError:
        print("Ошибка: VFS не найден")
        return None

    except (KeyError, csv.Error):
        print("Ошибка: неправильный формат VFS")
        return None

    return vfs


def get_parent_path(path):
    if path == ROOT_PATH:
        return ROOT_PATH

    parent = path.rsplit("/", 1)[0]

    if not parent:
        return ROOT_PATH

    return parent


def get_item_path(current_path, item_name):
    if current_path == ROOT_PATH:
        return ROOT_PATH + item_name

    return current_path + "/" + item_name


def list_directory(vfs, current_path):
    items = []

    for path in vfs:
        if path == current_path:
            continue

        parent = get_parent_path(path)

        if parent == current_path:
            item_name = path.rsplit("/", 1)[-1]
            items.append(item_name)

    if items:
        print(" ".join(sorted(items)))
    else:
        print("Папка пуста")


def change_directory(vfs, current_path, args):
    if len(args) != 1:
        print("Ошибка: cd требует один аргумент")
        return current_path

    target = args[0]

    if target == "..":
        return get_parent_path(current_path)

    if target == ROOT_PATH:
        return ROOT_PATH

    if target.startswith(ROOT_PATH):
        new_path = target
    else:
        new_path = get_item_path(current_path, target)

    if new_path not in vfs:
        print("Ошибка: папка не найдена")
        return current_path

    if vfs[new_path] != "dir":
        print("Ошибка: это не папка")
        return current_path

    return new_path


def execute_command(parts, vfs, current_path, start_time):
    if not parts:
        return True, current_path

    name = parts[0]
    args = parts[1:]

    if name == "exit":
        return False, current_path

    if name == "ls":
        list_directory(vfs, current_path)
    elif name == "cd":
        current_path = change_directory(vfs, current_path, args)
    elif name == "pwd":
        print(current_path)
    elif name == "uptime":
        seconds = int(time.time() - start_time)
        print("Время работы:", seconds, "секунд")
    else:
        print("Ошибка: неизвестная команда")

    return True, current_path


def run_script(script_path, vfs, current_path, start_time):
    try:
        with open(script_path, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                print(f"> {line}")

                try:
                    parts = parse_command(line)
                except ValueError:
                    print(
                        "Ошибка: неправильные кавычки"
                    )
                    continue

                running, current_path = execute_command(
                    parts, vfs, current_path, start_time
                )

                if not running:
                    return False, current_path

    except FileNotFoundError:
        print("Ошибка: стартовый скрипт не найден")

    return True, current_path

def run_interactive(
    vfs, current_path, start_time, vfs_name
):
    while True:
        command = input(f"{vfs_name}:{current_path}> ")
        try:
            parts = parse_command(command)
        except ValueError:
            print(
                "Ошибка: неправильные кавычки"
            )
            continue

        running, current_path = execute_command(
            parts, vfs, current_path, start_time
        )

        if not running:
            break

def main():
    if len(sys.argv) != ARGUMENT_COUNT:
        print(
            "Использование: python main.py "
            "<путь_к_VFS> <путь_к_скрипту>"
        )
        return

    vfs_path = sys.argv[1]
    script_path = sys.argv[2]

    print("VFS:", vfs_path)
    print("Script:", script_path)

    vfs = load_vfs(vfs_path)

    if vfs is None:
        return

    vfs_name = vfs_path.split("/")[-1]

    print("VFS загружена:", len(vfs), "элементов")

    start_time = time.time()
    current_path = ROOT_PATH

    running, current_path = run_script(
        script_path, vfs, current_path, start_time
    )

    if not running:
        return

    run_interactive(
        vfs, current_path, start_time, vfs_name
    )


if __name__ == "__main__":
    main()