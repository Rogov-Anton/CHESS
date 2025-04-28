class FileSystem:
    def __init__(self):
        self.files = [
            Directory('bin'),
            Directory('boot'),
            Directory('dev'),
            Directory('etc'),
            Directory('home'),
            File('swap.img')
        ]  # корневой каталог
        self.names = [
            'bin',
            'boot',
            'dev',
            'etc',
            'home',
            'swap.img'
        ]  # строки с именами существующих файлов

    def make_directory(self, name: str, path: str):
        parts = path.split('/')
        current_dir = self  # текущая дериктория
        idx = 0

        if path == '/':  # создать директорию в корневом каталоге
            if name not in self.names:
                self.files.append(Directory(name))
                self.names.append(name)
                return ''
            else:
                return f"mkdir: cannot create directory ‘{name}’: File exists"

        while len(parts) - 1 >= idx:
            for elem in current_dir.files:  # перебор по файлам в текущей директории
                if isinstance(elem, Directory) and elem.name == parts[idx]:
                    current_dir = elem
                    idx += 1
                    break
            else:
                return f"mkdir: cannot create directory ‘{path}’: No such file or directory"
        else:
            if name in current_dir.names:
                return f"mkdir: cannot create directory ‘{name}’: File exists"
            else:
                current_dir.files.append(Directory(name))
                current_dir.names.append(name)
                return ''

    def list_directory(self, path):
        parts = path.split('/')
        current_dir = self  # текущая дериктория
        idx = 0

        if path == '/':  # вывести список директорий в корневом каталоге
            return self.files
        while len(parts) - 1 >= idx:
            for elem in current_dir.files:
                if isinstance(elem, Directory) and elem.name == parts[idx]:
                    current_dir = elem
                    idx += 1
                    break
            else:
                return 'Error'
        else:
            return current_dir.files


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.names = []


class File:
    def __init__(self, name):
        self.name = name
        self.text = ''


def print_quide():
    print('exit          --  quit')
    print('mkdir {path}  --  make directory')
    print('ls {path}     --  list directory contents')


def execute_command(filesystem: FileSystem, text):  # Функция для выполнения команд
    if text == 'man':
        print_quide()
        return True
    parts = text.split()
    command = parts[0]
    if command == 'mkdir':
        result = filesystem.make_directory(parts[1], parts[2])
        if result != '':
            print(result)
    elif command == 'ls':
        result = filesystem.list_directory(parts[1])
        if result == 'Error':
            print(f"ls: cannot access {text}: No such file or directory")
        else:
            for elem in result:
                if isinstance(elem, Directory):
                    print(f"\033[34m{elem.name}\033[0m")
                else:
                    print(elem.name)


print('This is my file-system. Type <man> to get guide')
filesystem = FileSystem()
command = input('--> ')
while command != 'exit':
    execute_command(filesystem, command)
    command = input('--> ')
