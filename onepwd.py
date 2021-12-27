#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright(c) 2021-12-27 Asper, All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
 following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import uuid
from Crypto.Cipher import AES
from hashlib import blake2b
from base64 import b64encode, b64decode
import binascii
import os
import platform


CRYPT_BITS = 16


class OnePwd:
    def __init__(self, root):

        # 初始化主框架
        self.root = root
        self.root.title("one password")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # 初始化库表
        self.conn = self.init_table()

        self.root.option_add('*tearOff', FALSE)

        # 加载主窗口
        root_menu = Menu(self.root)
        self.root['menu'] = root_menu

    @staticmethod
    def init_table():
        if not os.path.exists("./data"):
            os.mkdir("./data")

        conn = sqlite3.connect("./data/crypher.db")
        cur = conn.cursor()
        sql_is_table_exist = "select count(*) from sqlite_master where type='table' and name='account_info'"
        is_table_exist = cur.execute(sql_is_table_exist).fetchone()[0]
        if not is_table_exist:
            try:
                sql_crt_table = "create table account_info(id text, title text, username text, password text)"
                cur.execute(sql_crt_table)
                conn.commit()
            except EXCEPTION as e:
                print(e)

        cur.close()
        return conn

    def __del__(self):
        if self.conn:
            self.conn.close()


class AddFrame:

    def __init__(self, root, conn):
        self.root = root
        self.frame = None
        self.conn = conn
        self.key = StringVar()
        self.key_tip = StringVar()
        self.title_tip = StringVar()
        self.username_tip = StringVar()
        self.password_tip = StringVar()
        self.entry_key = StringVar()
        self.entry_title = StringVar()
        self._add_window()

    def _add_window(self):
        self.frame = ttk.Frame(self.root, padding="20 20 20 20")
        # self.addframe.configure(width=self.width, height=self.height)
        self.frame.grid(column=0, row=0, sticky="ewsn")
        self.frame.columnconfigure(4, weight=1)
        # self.mainframe.lower(self.addframe)
        err_style = ttk.Style()
        err_style.configure("Error.TLabel", foreground="red")
        column_init = 1
        row_init = 1
        # -生成新增页面元素
        # --标签
        # ---key
        label_key = ttk.Label(self.frame, text="Key:")
        label_key.grid(column=column_init, row=row_init, sticky=E)

        # ---entry
        self.entry_key = ttk.Entry(self.frame, textvariable=self.key, show="*")
        self.entry_key.grid(column=column_init+1, row=row_init, columnspan=3, sticky="we")

        # ---key_tip
        label_key_tip = ttk.Label(self.frame, textvariable=self.key_tip, style="Error.TLabel")
        label_key_tip.grid(column=column_init+1, row=row_init+1, columnspan=3, sticky=W)

        # ---title
        label_title = ttk.Label(self.frame, text="Title:")
        label_title.grid(column=column_init, row=row_init+2, sticky=E)

        # ---entry
        self.title = StringVar()
        self.entry_title = ttk.Entry(self.frame, textvariable=self.title)
        self.entry_title.grid(column=column_init+1, row=row_init+2, columnspan=3, sticky="we")

        # ---title tip
        label_title_tip = ttk.Label(self.frame, textvariable=self.title_tip, style="Error.TLabel")
        label_title_tip.grid(column=column_init+1, row=row_init+3, columnspan=3, sticky=W)

        # --标签
        # ---username
        label_username = ttk.Label(self.frame, text="Username:")
        label_username.grid(column=column_init, row=row_init+4, sticky=E)

        # ---entry
        self.username = StringVar()
        entry_username = ttk.Entry(self.frame, textvariable=self.username)
        entry_username.grid(column=column_init+1, row=row_init+4, columnspan=3, sticky="we")

        # ---username tip
        label_username_tip = ttk.Label(self.frame, textvariable=self.username_tip, style="Error.TLabel")
        label_username_tip.grid(column=column_init+1, row=row_init+5, columnspan=3, sticky=W)

        # --标签
        # ---password
        label_password = ttk.Label(self.frame, text="Password:")
        label_password.grid(column=column_init, row=row_init+6, sticky=E)

        # ---entry
        self.password = StringVar()
        entry_password = ttk.Entry(self.frame, textvariable=self.password, show="*")
        entry_password.grid(column=column_init+1, row=row_init+6, columnspan=3, sticky="we")
        entry_password.bind("<KeyPress-Return>", lambda e: self.add_data())

        # ---password tip
        label_password_tip = ttk.Label(self.frame, textvariable=self.password_tip, style="Error.TLabel")
        label_password_tip.grid(column=column_init+1, row=row_init+7, columnspan=3, sticky=W)

        # --按钮
        # ---新增
        button_add = ttk.Button(self.frame, text="add", command=self.add_data)
        button_add.grid(column=column_init+1, row=row_init+8, sticky=W)
        # button_add.bind("<KeyPress-Return>", lambda e: self.add_data())

        # ---返回
        self.button_return = ttk.Button(self.frame, text="return")
        self.button_return.grid(column=column_init+2, row=row_init+8, sticky=W)

    def back_mainframe(self, other_frame):
        self.frame.lower(other_frame.frame)
        for v in self.frame.children.values():
            if v.cget("takefocus") == 1:
                v.configure(takefocus=False)

        for v in other_frame.frame.children.values():
            if v.cget("takefocus") == 0:
                v.configure(takefocus=True)
        other_frame.show_data(other_frame.frame.children["!treeview"])
        other_frame.entry_key.focus()

    def add_data(self):
        flag = 0
        if not self.title.get():
            self.title_tip.set("title should not none!")
            flag = 1
        else:
            self.title_tip.set("")

        if not self.username.get():
            self.username_tip.set("username should not none!")
            flag = 1
        else:
            self.username_tip.set("")

        if not self.password.get():
            self.password_tip.set("password should not none!")
            flag = 1
        else:
            self.password_tip.set("")

        if not self.key.get():
            self.key_tip.set("private key should not none!")
            flag = 1
        else:
            self.key_tip.set("")

        if flag == 1:
            return None

        cur = self.conn.cursor()
        t_id = str(uuid.uuid4())
        h = blake2b(digest_size=CRYPT_BITS)
        h.update(bytes(self.key.get(), encoding='utf-8'))
        key = bytes.fromhex(h.hexdigest())

        crypt_aes = AES.new(key, AES.MODE_EAX, key)
        title = crypt_aes.encrypt(b64encode(self.title.get().encode('utf-8')))
        username = crypt_aes.encrypt(b64encode(self.username.get().encode('utf-8')))
        password = crypt_aes.encrypt(b64encode(self.password.get().encode('utf-8')))

        cur.execute("insert into account_info (id, title, username, password) values (?, ?, ?, ?)",
                    (t_id, title.hex(), username.hex(), password.hex()))
        self.conn.commit()
        self.title.set("")
        self.username.set("")
        self.password.set("")

        cur.close()

        return None


class MainFrame:

    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.frame = None
        self.button_add = None
        self.button_show_text = StringVar(value="decrypt")
        self.pri_key = StringVar()
        self.entry_key = None

    def main_window(self):

        self.frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.frame.grid(column=0, row=0, sticky="nwes")
        # 支持窗口元素大小自动匹配
        self.frame.columnconfigure(4, weight=1)
        self.frame.rowconfigure(2, weight=1)

        # -生成首页元素
        # --"新增"按钮

        self.button_add = ttk.Button(self.frame, text="add...")
        self.button_add.grid(column=1, row=1, sticky="w")
        button_show = ttk.Button(self.frame, text="decrypt", textvariable=self.button_show_text,
                                 command=lambda: self.switch_button(self.button_show_text))
        button_show.grid(column=2, row=1, sticky="w")

        # --二次解密密钥提示标签和输入框
        label_key = ttk.Label(self.frame, text="key:", width=10, anchor="e")
        label_key.grid(column=3, row=1, sticky="e")

        self.entry_key = ttk.Entry(self.frame, textvariable=self.pri_key, show="*")
        self.entry_key.grid(column=4, row=1, sticky="we")
        self.entry_key.focus_set()
        self.entry_key.bind("<KeyPress-Return>", lambda e: self.switch_button(self.button_show_text))

        # --已保存账户信息列表框
        tree = ttk.Treeview(self.frame, columns=("title", "username", "password"), show="headings")
        tree.heading("title", text="Title")
        tree.heading("username", text="Username")
        tree.heading("password", text="Password")

        self.show_data(tree)

        tree_scroll = ttk.Scrollbar(self.frame, orient=VERTICAL, command=tree.yview)
        tree_scroll.grid(column=5, row=2, sticky="ns")
        tree.configure(yscrollcommand=tree_scroll.set)
        tree.grid(column=1, row=2, columnspan=4, sticky="wsen")

        # 窗口在屏幕居中显示
        self.root.withdraw()
        self.frame.update()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("+{}+{}".format((screen_width - width) // 2, (screen_height - height) // 2))
        self.root.deiconify()

    def switch_button(self, text):
        content = text.get()
        if content == "recover":
            self.show_data(self.frame.children["!treeview"])
            self.button_show_text.set("decrypt")
            self.pri_key.set("")
        else:
            res = self._show_password()
            if res:
                self.button_show_text.set("recover")

    def switch_frame(self, other_frame):
        for v in self.frame.children.values():
            if v.cget("takefocus") == "ttk::takefocus" or v.cget("takefocus") == 1:
                v.configure(takefocus=False)

        other_frame.frame.lift()
        for v in other_frame.frame.children.values():
            if v.cget("takefocus") == "ttk::takefocus" or v.cget("takefocus") == 0:
                v.configure(takefocus=True)
        other_frame.key_tip.set("")
        other_frame.title_tip.set("")
        other_frame.username_tip.set("")
        other_frame.password_tip.set("")
        if not other_frame.key.get():
            other_frame.entry_key.focus()
        else:
            other_frame.entry_title.focus()

    def show_data(self, tree):
        for i in tree.get_children():
            tree.delete(i)

        account_data = self.query_data()

        if account_data:
            for i in account_data:
                t_id = i[0]
                title = i[1]
                username = i[2]
                password = i[3]
                tree.insert('', 'end', t_id, values=(title, username, password))
                indx = tree.index(t_id)

                if indx % 2 == 0:
                    tree.item(t_id, tags=('ttk',))
                    tree.tag_configure('ttk', background="grey")
                else:
                    tree.item(t_id, tags=())

        right_menu = Menu(tree)
        right_menu.add_command(label="Delete")

        if self.root.tk.call('tk', 'windowingsystem') == 'aqua':
            tree.bind('<2>', lambda e: self.show_right_menu(e, tree, right_menu))
        else:
            tree.bind('<3>', lambda e: self.show_right_menu(e, tree, right_menu))

    def _show_password(self):

        private_key = self.pri_key.get()
        if not private_key:
            messagebox.showinfo(message='the key should not Null', parent=self.frame)
            return False

        tree = self.frame.children["!treeview"]

        for i in tree.get_children():
            title = tree.item(i)["values"][0]
            username = tree.item(i)["values"][1]
            password = tree.item(i)["values"][2]

            try:
                h = blake2b(digest_size=CRYPT_BITS)
                h.update(bytes(private_key, encoding='utf-8'))
                decode_key = bytes.fromhex(h.hexdigest())
                decrypt_aes = AES.new(decode_key, AES.MODE_EAX, decode_key)
                title = decrypt_aes.decrypt(bytes.fromhex(title))
                username = decrypt_aes.decrypt(bytes.fromhex(username))
                password = decrypt_aes.decrypt(bytes.fromhex(password))
                title = b64decode(title).decode('utf-8')
                username = b64decode(username).decode('utf-8')
                password = b64decode(password).decode('utf-8')
            except (UnicodeDecodeError, binascii.Error):
                messagebox.showinfo(message="key error!", parent=self.frame)
                self.pri_key.set("")
                return False
            except EXCEPTION:
                messagebox.showinfo(message="key error!", parent=self.frame)
                self.pri_key.set("")
                return False
            tree.set(i, "title", title)
            tree.set(i, "username", username)
            tree.set(i, "password", password)

        return True

    def query_data(self):
        cur = self.conn.cursor()

        is_table_exist = cur.execute("select count(*) from sqlite_master where type='table' and name='account_info'")
        if not is_table_exist.fetchone()[0]:
            return None

        data = cur.execute("select * from account_info").fetchall()

        return data

    def show_right_menu(self, e, tree, right_menu):
        item_id = tree.identify_row(e.y)
        tree.selection_set(item_id)
        right_menu.post(e.x_root, e.y_root)
        right_menu.entryconfigure(0, command=self.del_tree_item(tree, item_id))

    def del_tree_item(self, tree, item_id):
        tree.delete(item_id)
        cur = self.conn.cursor()
        cur.execute("delete from account_info where id = ?", (item_id, ))
        self.conn.commit()

        for i in tree.get_children():
            indx = tree.index(i)
            if indx % 2 == 0:
                tree.item(i, tags=('ttk',))
                tree.tag_configure('ttk', background="grey")
            else:
                tree.item(i, tags=())


if __name__ == '__main__':
    win = Tk()
    onepwd = OnePwd(win)
    mainframe = MainFrame(onepwd.root, onepwd.conn)
    addframe = AddFrame(onepwd.root, onepwd.conn)

    mainframe.main_window()
    mainframe.button_add.bind("<1>", lambda e: mainframe.switch_frame(addframe))
    addframe.button_return.bind("<1>", lambda e: addframe.back_mainframe(mainframe))
    if platform.system() == 'Windows':
        onepwd.root.bind("<Alt-a>", lambda e: mainframe.switch_frame(addframe))
        onepwd.root.bind("<Alt-r>", lambda e: addframe.back_mainframe(mainframe))
    elif platform.system() == 'Darwin':
        onepwd.root.bind("<Command-a>", lambda e: mainframe.switch_frame(addframe))
        onepwd.root.bind("<Command-r>", lambda e: addframe.back_mainframe(mainframe))

    win.mainloop()
