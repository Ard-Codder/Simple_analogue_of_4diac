### Updated README with `requirements.txt`

#### English

# FB Editor

This project is an IDE for creating and managing function blocks (FB) in a graphical environment using PyQt5.

## Features

- Create and manage function blocks.
- Connect blocks using lines.
- Save and load projects in XML format.
- Generate and deploy `.fboot` files.

## Structure

- `connection.py`: Manages the connections between blocks.
- `custom_blocks.py`: Defines custom function blocks.
- `editable_label.py`: Provides editable labels for blocks.
- `file_manager.py`: Handles file operations like saving and loading projects.
- `func_block.py`: Base class for function blocks.
- `main_window.py`: Main window of the application.
- `tcp_sender.py`: Sends `.fboot` files via TCP.

## Usage

1. Run the application using `main_window.py`.
2. Create blocks using the "Blocks" menu.
3. Connect blocks by clicking and dragging from one block to another.
4. Save the project using the "File" menu.
5. Deploy the project using the "Run" menu.

## Adding Custom Blocks

To add your own custom blocks, follow these steps:

1. **Define the Block Class**: Create a new class in `custom_blocks.py` that inherits from `FuncBlock`.

    ```python
    from func_block import FuncBlock

    class MyCustomBlock(FuncBlock):
        def __init__(self, main_window, name='MyCustomBlock', x=500, y=500):
            super().__init__(main_window, name=name, width=100, height=100, x=x, y=y, n_rects_left=2, n_rects_right=2, labels=['MyCustomBlock', 'REQ', 'IN', 'CNF', 'OUT'])
    ```

2. **Create Block Function**: Add a function to create an instance of your custom block in `custom_blocks.py`.

    ```python
    def create_my_custom_block(main_window):
        k_blocks = main_window.block_count.get('MyCustomBlock', 1)
        main_window.blocks.append(MyCustomBlock(main_window, f'MyCustomBlock_{k_blocks}'))
        main_window.block_count['MyCustomBlock'] = k_blocks + 1
        main_window.update_all()
    ```

3. **Update Block Classes Dictionary**: Add your custom block class to the `all_block_classes` function in `custom_blocks.py`.

    ```python
    def all_block_classes():
        classes = {
            'E_RESTART': BlockStart,
            'INT2INT': BlockInt2Int,
            'OUT_ANY_CONSOLE': BlockOutAnyConsole,
            'STRING2STRING': BlockString2String,
            'F_ADD': BlockFAdd,
            'MyCustomBlock': MyCustomBlock  # Add your custom block here
        }
        return classes
    ```

4. **Update Block Count Dictionary**: Add your custom block to the `count_blocks` function in `custom_blocks.py`.

    ```python
    def count_blocks():
        count = {
            'BlockInt2Int': 1,
            'BlockOutAnyConsole': 1,
            'BlockString2String': 1,
            'BlockFAdd': 1,
            'MyCustomBlock': 1  # Add your custom block here
        }
        return count
    ```

5. **Add Menu Action**: Add an action to the "Blocks" menu in `main_window.py` to create your custom block.

    ```python
    my_custom_block_action = QAction("MyCustomBlock", self)
    my_custom_block_action.triggered.connect(lambda: cb.create_my_custom_block(self))
    self.menu_blocks.addAction(my_custom_block_action)
    ```

## Requirements

- Python 3.x
- Libraries listed in `requirements.txt`

## Installation

1. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

## License

This project is licensed under the MIT License.

#### Russian

# Редактор FB

Этот проект представляет собой среду разработки (IDE) для создания и управления функциональными блоками (FB) в графической среде с использованием PyQt5.

## Возможности

- Создание и управление функциональными блоками.
- Соединение блоков с помощью линий.
- Сохранение и загрузка проектов в формате XML.
- Генерация и развертывание файлов `.fboot`.

## Структура

- `connection.py`: Управление соединениями между блоками.
- `custom_blocks.py`: Определение пользовательских функциональных блоков.
- `editable_label.py`: Предоставление редактируемых меток для блоков.
- `file_manager.py`: Обработка файловых операций, таких как сохранение и загрузка проектов.
- `func_block.py`: Базовый класс для функциональных блоков.
- `main_window.py`: Основное окно приложения.
- `tcp_sender.py`: Отправка файлов `.fboot` по TCP.

## Использование

1. Запустите приложение с помощью `main_window.py`.
2. Создайте блоки с помощью меню "Blocks".
3. Соедините блоки, щелкнув и перетащив мышь от одного блока к другому.
4. Сохраните проект с помощью меню "File".
5. Разверните проект с помощью меню "Run".

## Добавление Пользовательских Блоков

Чтобы добавить свои собственные пользовательские блоки, следуйте этим шагам:

1. **Определите Класс Блока**: Создайте новый класс в `custom_blocks.py`, который наследуется от `FuncBlock`.

    ```python
    from func_block import FuncBlock

    class MyCustomBlock(FuncBlock):
        def __init__(self, main_window, name='MyCustomBlock', x=500, y=500):
            super().__init__(main_window, name=name, width=100, height=100, x=x, y=y, n_rects_left=2, n_rects_right=2, labels=['MyCustomBlock', 'REQ', 'IN', 'CNF', 'OUT'])
    ```

2. **Создайте Функцию Блока**: Добавьте функцию для создания экземпляра вашего пользовательского блока в `custom_blocks.py`.

    ```python
    def create_my_custom_block(main_window):
        k_blocks = main_window.block_count.get('MyCustomBlock', 1)
        main_window.blocks.append(MyCustomBlock(main_window, f'MyCustomBlock_{k_blocks}'))
        main_window.block_count['MyCustomBlock'] = k_blocks + 1
        main_window.update_all()
    ```

3. **Обновите Словарь Классов Блоков**: Добавьте ваш пользовательский класс блока в функцию `all_block_classes` в `custom_blocks.py`.

    ```python
    def all_block_classes():
        classes = {
            'E_RESTART': BlockStart,
            'INT2INT': BlockInt2Int,
            'OUT_ANY_CONSOLE': BlockOutAnyConsole,
            'STRING2STRING': BlockString2String,
            'F_ADD': BlockFAdd,
            'MyCustomBlock': MyCustomBlock  # Добавьте ваш пользовательский блок здесь
        }
        return classes
    ```

4. **Обновите Словарь Подсчета Блоков**: Добавьте ваш пользовательский блок в функцию `count_blocks` в `custom_blocks.py`.

    ```python
    def count_blocks():
        count = {
            'BlockInt2Int': 1,
            'BlockOutAnyConsole': 1,
            'BlockString2String': 1,
            'BlockFAdd': 1,
            'MyCustomBlock': 1  # Добавьте ваш пользовательский блок здесь
        }
        return count
    ```

5. **Добавьте Действие Меню**: Добавьте действие в меню "Blocks" в `main_window.py` для создания вашего пользовательского блока.

    ```python
    my_custom_block_action = QAction("MyCustomBlock", self)
    my_custom_block_action.triggered.connect(lambda: cb.create_my_custom_block(self))
    self.menu_blocks.addAction(my_custom_block_action)
    ```

## Требования

- Python 3.x
- Библиотеки, перечисленные в `requirements.txt`

## Установка

1. Установите необходимые библиотеки:

    ```bash
    pip install -r requirements.txt
    ```

## Лицензия

Этот проект распространяется по лицензии MIT.