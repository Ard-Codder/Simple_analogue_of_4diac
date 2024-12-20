from func_block import FuncBlock

class BlockStart(FuncBlock):
    def __init__(self, main_window, name='START', x=100, y=100):
        """
        Initialize the BlockStart with a specific name, position, and labels.
        """
        super().__init__(main_window, name=name, width=80, height=60, x=x, y=y, n_rects_left=1, n_rects_right=2, labels=['E_RESTART', 'STOP', 'COLD', 'WARM'])

class BlockInt2Int(FuncBlock):
    def __init__(self, main_window, name='INT2INT', x=500, y=500):
        """
        Initialize the BlockInt2Int with a specific name, position, and labels.
        """
        super().__init__(main_window, name=name, width=60, height=62, x=x, y=y, n_rects_left=2, n_rects_right=2, labels=['INT2INT', 'REQ', 'IN', 'CNF', 'OUT'])

class BlockOutAnyConsole(FuncBlock):
    def __init__(self, main_window, name='OUT_ANY_CONSOLE', x=500, y=500):
        """
        Initialize the BlockOutAnyConsole with a specific name, position, and labels.
        """
        super().__init__(main_window, name=name, width=140, height=92, x=x, y=y, n_rects_left=4, n_rects_right=2, labels=['OUT_ANY_CONSOLE', 'REQ', 'QI', 'LABEL', 'IN', 'CNF', 'QO'])

class BlockString2String(FuncBlock):
    def __init__(self, main_window, name='STRING2STRING', x=500, y=500):
        """
        Initialize the BlockString2String with a specific name, position, and labels.
        """
        super().__init__(main_window, name=name, x=x, y=y, width=84, height=62, n_rects_left=2, n_rects_right=2, labels=['STRING2STRING', 'REQ', 'IN', 'CNF', 'OUT'])

class BlockFAdd(FuncBlock):
    def __init__(self, main_window, name='F_ADD', x=500, y=500):
        """
        Initialize the BlockFAdd with a specific name, position, and labels.
        """
        super().__init__(main_window, name=name, width=50, height=76, x=x, y=y, n_rects_left=3, n_rects_right=2, labels=['F_ADD', 'REQ', 'IN1', 'IN2', 'CNF', 'OUT'])

def create_block_start(main_window):
    """
    Create a BlockStart and add it to the main window.
    """
    main_window.start_block = BlockStart(main_window, 'START')
    main_window.blocks.append(main_window.start_block)
    main_window.update_all()

def create_block_int2int(main_window):
    """
    Create a BlockInt2Int and add it to the main window.
    """
    k_blocks = main_window.block_count['BlockInt2Int']
    main_window.blocks.append(BlockInt2Int(main_window, f'INT2INT_{k_blocks}'))
    main_window.block_count['BlockInt2Int'] += 1
    main_window.update_all()

def create_block_out_any_console(main_window):
    """
    Create a BlockOutAnyConsole and add it to the main window.
    """
    k_blocks = main_window.block_count['BlockOutAnyConsole']
    main_window.blocks.append(BlockOutAnyConsole(main_window, f'OUT_ANY_CONSOLE_{k_blocks}'))
    main_window.block_count['BlockOutAnyConsole'] += 1
    main_window.update_all()

def create_block_string2string(main_window):
    """
    Create a BlockString2String and add it to the main window.
    """
    k_blocks = main_window.block_count['BlockString2String']
    main_window.blocks.append(BlockString2String(main_window, f'STRING2STRING_{k_blocks}'))
    main_window.block_count['BlockString2String'] += 1
    main_window.update_all()

def create_block_f_add(main_window):
    """
    Create a BlockFAdd and add it to the main window.
    """
    k_blocks = main_window.block_count['BlockFAdd']
    main_window.blocks.append(BlockFAdd(main_window, f'F_ADD_{k_blocks}'))
    main_window.block_count['BlockFAdd'] += 1
    main_window.update_all()

def all_block_classes():
    """
    Return a dictionary of all block classes.
    """
    classes = {
        'E_RESTART': BlockStart,
        'INT2INT': BlockInt2Int,
        'OUT_ANY_CONSOLE': BlockOutAnyConsole,
        'STRING2STRING': BlockString2String,
        'F_ADD': BlockFAdd
    }
    return classes

def count_blocks():
    """
    Return a dictionary with the initial count of each block type.
    """
    count = {
        'BlockInt2Int': 1,
        'BlockOutAnyConsole': 1,
        'BlockString2String': 1,
        'BlockFAdd': 1
    }
    return count
