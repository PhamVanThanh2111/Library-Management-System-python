from LendingNode import LendingNode
from BookList import BookList
from Book import Book
from Lending import Lending
import csv

class LendingList:
    def __init__(self):
        self.head = None

    def add_lending(self, lending):
        if not self.head:
            self.head = LendingNode(lending)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = LendingNode(lending)

    def add_lending_to_file(self, lending):
        # Tìm kiếm sách trong danh sách sách để kiểm tra số lượng có đủ để cho mượn không
        bookList = BookList()
        bookList.load_from_csv("../Data/books.csv")
        book = bookList.search(lending.bcode)
        if book.book and book.book.quantity - book.book.lended >= 1:
            # Thêm dữ liệu vào file Lending.csv
            with open("../Data/lending.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([lending.bcode, lending.rcode, lending.state])
            # Cập nhật lại số lượng sách đã mượn
            Book.increase_lended_in_books_csv(lending.bcode)
        else:
            print("Không đủ sách để cho mượn hoặc không tìm thấy sách")


    def return_book(self, lending):
        # Giảm số lượng đã mượn của sách sau khi trả sách thành công
        Book.decrease_lended_in_books_csv(lending.bcode)
        # Ghi dữ liệu vào file lending.csv
        with open("../Data/lending.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([lending.bcode, lending.rcode, lending.state])


    def search_by_bcode(self, bcode):
        current = self.head
        while current:
            if current.lending.bcode == bcode:
                return current.lending
            current = current.next
        return None

    def search_by_rcode(self, rcode):
        current = self.head
        while current:
            if current.lending.rcode == rcode:
                return current.lending
            current = current.next
        return None
    
    def load_from_csv(self, file_path):
        try:
            with open(file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    bcode = row['bcode']
                    rcode = row['rcode']
                    state = int(row['state'])
                    lending = Lending(bcode, rcode, state)
                    self.add_lending(lending)
        except FileNotFoundError:
            print("Không tìm thấy file được chỉ định.")
        except Exception as e:
            print("Đã xảy ra lỗi khi tải dữ liệu mượn sách từ file:", str(e))
    
    def display_lending(self):
        current = self.head
        while current:
            print("bcode:", current.lending.bcode)
            print("rcode:", current.lending.rcode)
            print("state:", current.lending.state)
            print()
            current = current.next
            
    def sort_by_bcode(self):
        # Tạo một danh sách mượn sách mới để lưu trữ kết quả sắp xếp
        sorted_lending_list = LendingList()

        # Kiểm tra nếu danh sách trống hoặc chỉ có một phần tử
        if not self.head or not self.head.next:
            return sorted_lending_list

        # Chuyển danh sách sang danh sách liên kết
        lending_list = []
        current = self.head
        while current:
            lending_list.append(current.lending)
            current = current.next
        
        # Sắp xếp danh sách theo bcode
        lending_list.sort(key=lambda x: x.bcode)

        # Thêm các mượn sách đã sắp xếp vào danh sách mới
        for lending in lending_list:
            sorted_lending_list.add_lending(lending)

        return sorted_lending_list
    
    def sort_by_rcode(self):
        # Tạo một danh sách mượn sách mới để lưu trữ kết quả sắp xếp
        sorted_lending_list = LendingList()

        # Kiểm tra nếu danh sách trống hoặc chỉ có một phần tử
        if not self.head or not self.head.next:
            return sorted_lending_list

        # Chuyển danh sách sang danh sách liên kết
        lending_list = []
        current = self.head
        while current:
            lending_list.append(current.lending)
            current = current.next
        
        # Sắp xếp danh sách theo rcode
        lending_list.sort(key=lambda x: x.rcode)

        # Thêm các mượn sách đã sắp xếp vào danh sách mới
        for lending in lending_list:
            sorted_lending_list.add_lending(lending)

        return sorted_lending_list