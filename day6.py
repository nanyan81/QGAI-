import datetime

# 定义基类（Book）
class Book:
    def __init__(self,name,type,address):
        self.__name = name
        self.__type = type
        self.__address = address

        self.book_stauts = "馆藏中"
        self.borrow_time = None
        self.ddl_time = None
        self.borrower_name = None
        self.borrower_ID = None

book_instance = {}

def create_book():
    new_book = input("请依次输入【图书名称】，【图书类型】，【存放地址（如A1-7564）】(请用空格分开)\n").split()
    book_name,book_type,book_address = new_book

    if book_name in book_instance:
        print(f"❌ 实例名「{book_name}」已存在！\n")
        return

    book_instance[book_name] = Book(book_name,book_type,book_address)

    print(f"新书{book_name}已成功入库！\n")

def borrow_book():
    need_book = input("请输入书本的名字：\n")
    if need_book in book_instance:
        if book_instance[need_book].book_stauts == "馆藏中":
            book_instance[need_book].book_stauts = "借出中"
            book_instance[need_book].borrower_name = input("请输入借阅人的名字：\n")
            book_instance[need_book].borrower_ID = input("请输入借阅人的ID\n")

            now_time = datetime.datetime.now()
            book_instance[need_book].borrow_time = now_time.strftime("%Y-%m-%d")
            return_time = now_time + datetime.timedelta(days = 60)
            book_instance[need_book].ddl_time = return_time.strftime("%Y-%m-%d")

            print(f"已成功借阅该书【{book_instance[need_book]}】")
        else:
            print("该书已被借走")
    else:
        print("馆中暂时没有这本书")

def return_book():
    the_book = input("请输入这本书的名字：")
    if the_book in book_instance:
        if book_instance[the_book].book_stauts == "借出中":
            book_instance[the_book].book_stauts = "馆藏中"
            book_instance[the_book].borrower_name = None
            book_instance[the_book].borrower_ID = None
            book_instance[the_book].ddl_time = None
            book_instance[the_book].borrow_time = None

            print(f"该书【 {the_book} 】已成功归还！")
        else:
            print(f"该书【 {the_book} 】已在库中！")
    else:
        print(f"该书【 {the_book} 】不是本图书馆的！")




def main():
    while True:
        selection = int(input("请输入操作数：\n1:新书入库\n2:图书借出\n3:图书归还\n"))

        match selection:
                case 1:
                    print("=====现在进行新书的初始化入库=====\n")
                    create_book()
                case 2:
                    print("=====现在开始进行图书借出操作=====\n")
                    borrow_book()
                case 3:
                    print("=====现在开始图书归还操作=====\n")
                    return_book()
                case 0:
                    return

if __name__ == "__main__":
    main()