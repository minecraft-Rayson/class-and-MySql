import pymysql
import tkinter as tk
from tkinter import messagebox

def main():
    # Load the security file or display an error message and exit
    '''try:
        with open("E:\JiYuTrainer.ini", 'r') as fh:
            pass
    except FileNotFoundError:
        messagebox.showerror("错误", "缺少安全文件")
        return'''

    # Prompt the user for the password using a dialog box
    #password = get_password_from_dialog()

    # Create the database connection
    connection = pymysql.connect(
        host='cn-jn-yd-plustmp1.natfrp.cloud',
        port=56536,
        user='root',
        password="16816899abc!!",
        database='dgxt',
        charset='utf8'
    )

    # Initialize the UI
    app = Application(connection)
    app.mainloop()

def get_password_from_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    password_entry = tk.Entry(root, show="*", width=20)
    password_entry.pack()
    ok_button = tk.Button(root, text="OK", command=root.destroy)
    ok_button.pack()

    root.mainloop()
    return password_entry.get()

class Application(tk.Tk):
    def __init__(self, connection):
        super().__init__()
        self.title("数据库管理应用")
        self.connection = connection

        self.init_ui()

    def init_ui(self):
        # Create a frame for options
        options_frame = tk.Frame(self)
        options_frame.pack(pady=10)

        # Add buttons for each option
        self.option_buttons = []
        for i, option_text in enumerate(["查询记录", "减少记录", "增加记录", "退出"]):
            button = tk.Button(options_frame, text=option_text, command=lambda i=i: self.handle_option(i))
            button.pack(side=tk.LEFT, padx=5)
            self.option_buttons.append(button)

    def handle_option(self, option_index):
        if option_index == 0:
            self.query_record()
        elif option_index == 1:
            self.decrease_record()
        elif option_index == 2:
            self.increase_record()
        else:
            self.quit()

    def query_record(self):
        num = self.get_student_number()
        print(f"Received student number: {num}")
        if num is None:
            return

        with self.connection.cursor() as cursor:
            select_data_sql = "SELECT * FROM dgxt WHERE num = %s"
            cursor.execute(select_data_sql, (num,))
            result = cursor.fetchone()

            if result is not None:
                self.show_message(f"找到的记录：{result}")
            else:
                self.show_message(f"未找到学号为 {num} 的记录")

    def decrease_record(self):
        num = self.get_student_number()
        if num is None:
            return

        with self.connection.cursor() as cursor:
            select_data_sql = "SELECT * FROM dgxt WHERE num = %s"
            cursor.execute(select_data_sql, (num,))
            result = cursor.fetchone()

            if result is None:
                self.show_message("没有找到该学号的记录")
                return

            current_jh = result[1]

            if current_jh > 0:
                update_jh_sql = "UPDATE dgxt SET jh = jh - 1 WHERE num = %s"
                cursor.execute(update_jh_sql, (num,))
                self.connection.commit()
                self.show_message(f"成功将学号为 {num} 的记录的 jh 字段减一")
            else:
                self.show_message(f"学号为 {num} 的记录的 jh 字段值已经是 0 或负数，无法继续减一")

    def increase_record(self):
        num = self.get_student_number()
        if num is None:
            return

        with self.connection.cursor() as cursor:
            select_data_sql = "SELECT * FROM dgxt WHERE num = %s"
            cursor.execute(select_data_sql, (num,))
            result = cursor.fetchone()

            if result is None:
                self.show_message("没有找到该学号的记录")
                return

            update_jh_sql = "UPDATE dgxt SET jh = jh + 1 WHERE num = %s"
            cursor.execute(update_jh_sql, (num,))
            self.connection.commit()
            self.show_message(f"成功将学号为 {num} 的记录的 jh 字段加一")

    def get_student_number(self):
        def on_ok():
            nonlocal valid_input, num  # 使用nonlocal关键字引用外层变量
            try:
                num = int(entry.get())
                valid_input = True
            except ValueError:
                self.show_message("请输入有效的数字作为学号")
                return  # 如果发生异常，直接结束on_ok，不销毁对话框

            if valid_input:  # 只有在输入有效时才销毁对话框
                dialog.destroy()

        valid_input = False
        num = None  # 初始化num，用于存储有效输入的学号
        dialog = tk.Toplevel(self)
        dialog.title("请输入学号")

        label = tk.Label(dialog, text="学号:")
        label.pack(side=tk.LEFT, padx=(0, 7))

        entry = tk.Entry(dialog, width=10)
        entry.pack(side=tk.LEFT)

        ok_button = tk.Button(dialog, text="确定", command=on_ok)
        ok_button.pack(side=tk.RIGHT)

        cancel_button = tk.Button(dialog, text="取消", command=dialog.destroy)
        cancel_button.pack(side=tk.RIGHT)

        dialog.focus_set()
        dialog.grab_set()

        dialog.wait_window(dialog)  # 等待对话框关闭

        if valid_input:
            print(f"Returning student number: {num}")
            return num
        else:
            print("Returning student number: None")
            return None
    

    def show_message(self, message):
        messagebox.showinfo("提示", message)

if __name__ == "__main__":
    main()