# 🗂️ Файловый Менеджер (CLI)

Простой файловый менеджер на Python с текстовым интерфейсом. Работает только внутри указанной директории, не даёт выйти за её пределы.

## 🔧 Возможности

- `ls` — список файлов
- `cd`, `pwd` — навигация
- `mkdir`, `rmdir` — работа с папками
- `touch`, `cat`, `write`, `rm` — работа с файлами
- `cp`, `mv` — копирование и перемещение
- `help`, `exit` — справка и выход

## 🚀 Запуск

```bash
git clone https://github.com/yourusername/file_manager_lab.git
cd file_manager_lab
python file_manager.py

Настрой путь к рабочей директории в config.ini.

## 💡 Пример
[.]$ mkdir notes
[.]$ cd notes
[notes]$ touch todo.txt
[notes]$ write todo.txt w
Введите текст:
Сделать проект
<пустая строка>

[notes]$ cat todo.txt
Сделать проект
