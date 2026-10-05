import shlex
import sys


def parse_command(command):
    return shlex.split(command)


def execute_command(parts):
    if not parts:
        return True

    name = parts[0]
    args = parts[1:]

    if name == "exit":
        return False
    elif name == "ls":
        print("ls", args)
    elif name == "cd":
        print("cd", args)
    else:
        print("Ошибка: неизвестная команда")

    return True


def run_script(script_path):
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
                    print("Ошибка: неправильные кавычки")
                    continue

                if not execute_command(parts):
                    return False

    except FileNotFoundError:
        print("Ошибка: стартовый скрипт не найден")

    return True


def main():
    if len(sys.argv) != 3:
        print("Использование: python main.py <путь_к_VFS> <путь_к_скрипту>")
        return

    vfs_path = sys.argv[1]
    script_path = sys.argv[2]

    print("VFS:", vfs_path)
    print("Script:", script_path)

    if not run_script(script_path):
        return

    vfs_name = "default"

    while True:
        command = input(f"{vfs_name}> ")

        try:
            parts = parse_command(command)
        except ValueError:
            print("Ошибка: неправильные кавычки")
            continue

        if not execute_command(parts):
            break


if __name__ == "__main__":
    main()