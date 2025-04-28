class FileSystem:
    def __init__(self):
        self.files = [
            Directory('1'),
            Directory('2')
        ]  # корневой каталог

    def make_directory(self, name: str, path: str):
        if path == '/':  # Если путь не указан, то создать папку в корневом каталоге
            self.files.append(Directory(name))
            return True

        parts = path.split('/')
        current_dir = self  # текущая дериктория
        idx = 0

        while len(parts) - 2 >= idx:
            for elem in current_dir.files:  # Проходим по всем файлам в текущей директории
                if isinstance(elem, Directory):  # Если элемент - это дирректория
                    if elem.name == parts[idx]:
                        current_dir = elem
                        idx += 1
                        break
            else:  # Если дирректория не найдена, то выдать сообщение об ошибке
                return False

        current_dir.files.append(Directory(name))

    def list_directory(self, path):
        if path == '/':
            return self.files

        parts = path.split('/')
        current_dir = self  # текущая дериктория
        idx = 0

        while len(parts) - 2 >= idx:
            for elem in current_dir.files:  # Проходим по всем файлам в текущей директории
                if isinstance(elem, Directory):  # Если элемент - это дирректория
                    if elem.name == parts[idx]:
                        current_dir = elem
                        idx += 1
                        break
            else:  # Если дирректория не найдена, то выдать сообщение об ошибке
                return False

        return current_dir.files


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []

    def __repr__(self):
        BLUE = '\033[34m'
        RESET = '\033[0m'
        print(f"{BLUE}{self.name}{RESET}")


def print_quide():
    print('<exit> - quit')
    print('<mkdir> {path} - make directory')
    print('')


def execute_command(filesystem: FileSystem, text):  # Функция для выполнения команд
    if text == 'man':
        print_quide()
        return True
    parts = text.split()
    command = parts[0]
    if command == 'mkdir':
        filesystem.make_directory(parts[1], parts[2])
        return True
    if command == 'ls':
        result = filesystem.list_directory(parts[1])
        print(result)
        return True


print('This is my file-system. Type <man> to get guide')
filesystem = FileSystem()
command = input()

execute_command(filesystem, command)

"""
while command != 'exit':
    execute_command(filesystem, command)
    command = input()
"""