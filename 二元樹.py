# 課堂練習
#  使用二元搜尋樹製作一個通訊錄程式
#  功能
#  輸入’i’ 新增節點,可輸入姓名, 電話, 依據姓名字母順序
# 插入節點(假設輸入之姓名不會重覆)
#  輸入’d’接著輸入姓名，可將一筆資料節點中之姓名相
# 同者刪除(假設輸入之姓名不會重覆)
#  輸入’f’接著輸入一個姓名，可將一筆資料節點中之姓
# 名相同者印出資料
#  輸入’l’依據姓名字母順序印出所有節點內容
#  輸入’q’ 讀取離開程式
#  輸入格式
#  格式不拘
from random import randint
from enum import Enum
import time

traversal_result = []


class ChildNodeType(Enum):
    LEFT = "left"
    RIGHT = "right"


class AddressBook:
    name: 'str'
    phone_number: 'str'
    left: 'AddressBook'
    right: 'AddressBook'

    def __init__(self, name=None, phone_number=None):
        self.name = name
        self.phone_number = phone_number
        self.left = None
        self.right = None

    @staticmethod
    def insert(node: 'AddressBook', new_obj: 'AddressBook'):
        if new_obj.name == node.name:
            return
        elif new_obj.name > node.name:
            if node.right is None:
                node.right = new_obj
            else:
                AddressBook.insert(node.right, new_obj)
        else:
            if node.left is None:
                node.left = new_obj
            else:
                AddressBook.insert(node.left, new_obj)

    @staticmethod
    def delete(root: 'AddressBook', name: 'str'):
        delete_node = AddressBook.search(root, name)
        if delete_node is None:
            return
        parent_node = AddressBook.find_parent(root, delete_node)

        # 沒有左樹
        if delete_node.left is None:
            # 又是父節點
            if parent_node is None:
                return delete_node.right
            else:
                if parent_node[1] == ChildNodeType.RIGHT:
                    parent_node[0].right = delete_node.right
                else:
                    parent_node[0].left = delete_node.right
        # 沒有右樹
        elif delete_node.right is None:
            # 又是父節點
            if parent_node is None:
                return delete_node.left
            else:
                if parent_node[1] == ChildNodeType.RIGHT:
                    parent_node[0].right = delete_node.left
                else:
                    parent_node[0].left = delete_node.left
        else:
            replace_node = delete_node.right
            while replace_node.left is not None:
                replace_node = replace_node.left

            AddressBook.delete(root, replace_node.name)
            if parent_node[1] == ChildNodeType.RIGHT:
                parent_node[0].right = replace_node
            else:
                parent_node[0].left = replace_node
            replace_node.left = delete_node.left
            replace_node.right = delete_node.right

        return root

    @staticmethod
    def search(node: 'AddressBook', name: 'str'):
        if node is None:
            return
        elif node.name == name:
            return node

        l_return = AddressBook.search(node.left, name)
        if l_return is not None:
            return l_return
        return AddressBook.search(node.right, name)

    @staticmethod
    def find_parent(node: 'AddressBook', target: 'AddressBook') -> ('AddressBook', 'ChildNodeType'):
        if target is None:
            return None
        elif node is None:
            return
        if target == node.left:
            return node, ChildNodeType.LEFT
        elif target == node.right:
            return node, ChildNodeType.RIGHT

        l_return = AddressBook.find_parent(node.left, target)
        if l_return is not None:
            return l_return
        return AddressBook.find_parent(node.right, target)

    # 中走訪
    @staticmethod
    def show_all_data_in_order_traversal(node: 'AddressBook'):
        if node is None:
            return
        AddressBook.show_all_data_in_order_traversal(node.left)
        print(node.name, node.phone_number)
        AddressBook.show_all_data_in_order_traversal(node.right)

    # 前走訪
    @staticmethod
    def show_all_data_pre_order_traversal(node: 'AddressBook'):
        global traversal_result
        if node is None:
            return
        traversal_result.append(node.name)
        AddressBook.show_all_data_pre_order_traversal(node.left)
        AddressBook.show_all_data_pre_order_traversal(node.right)


def main_process():
    root = None
    while True:
        cmd = input("請輸入命令:")
        if cmd == "q":
            break
        elif cmd == "i":
            name = input("請輸入姓名:")
            phone_number = input("請輸入手機:")
            new_obj = AddressBook(name=name, phone_number=phone_number)
            if root is None:
                root = new_obj
            else:
                AddressBook.insert(root, new_obj)
        elif cmd == "d":
            name = input("請輸入欲刪除姓名:")
            root = AddressBook.delete(root, name)
        elif cmd == "f":
            name = input("請輸入姓名:")
            node = AddressBook.search(root, name)
            if node is not None:
                print(node.name, node.phone_number)
        elif cmd == "l":
            AddressBook.show_all_data_in_order_traversal(root)
        elif cmd == "q":
            break


def basic_test():
    test_data = [5, 4, 6, 2, 8, 1, 3, 7, 9]
    root = make_data(test_data)

    time.sleep(0.5)

    node = AddressBook.search(root, 8)
    if node.name != 8:
        print("search basic_test ERROR")
        return

    node_2 = AddressBook.find_parent(root, node)
    if node_2[0].name != 6 or node_2[1] != ChildNodeType.RIGHT:
        print("find_parent ERROR")
        return
    print("basic_test pass")


def delete_test():
    global traversal_result
    traversal_result = []
    test_data = [17, 5, 35, 2, 11, 29, 38, 9, 16, 7, 8]
    root = make_data(test_data)
    AddressBook.delete(root, 35)
    AddressBook.show_all_data_pre_order_traversal(root)
    if traversal_result != [17, 5, 2, 11, 9, 7, 8, 16, 38, 29]:
        print("delete ERROR!!!")
        return
    print("delete_test pass")


def make_data(data_list):
    root = None
    for data in data_list:
        new_obj = AddressBook(name=data)
        if root is None:
            root = new_obj
        else:
            AddressBook.insert(root, new_obj)
    return root


def random_name():
    name_length = randint(4, 12)
    aph = "qazwsxedcrfvtgbyhnujmikolp"
    name = ""
    for _ in range(name_length):
        name += aph[randint(0, 25)]
    return name


if __name__ == '__main__':
    basic_test()
    delete_test()
    main_process()
