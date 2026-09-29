import shlex


def parse_command(command):
    return shlex.split(command)


def main():
    vfs_name = "default"

    while True:
        command = input(f"{vfs_name}> ")

        try:
            parts = parse_command(command)
        except ValueError:
            print("Ошибка: неправильные кавычки")
            continue

        if not parts:
            continue

        name = parts[0]
        args = parts[1:]

        if name == "exit":
            break
        elif name == "ls":
            print("ls", args)
        elif name == "cd":
            print("cd", args)
        else:
            print("Ошибка: неизвестная команда")


if __name__ == "__main__":
    main()