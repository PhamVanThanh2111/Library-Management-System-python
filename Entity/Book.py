import csv

class Book:
    def __init__(self, bcode, title, quantity, lended, price):
        self.bcode = bcode
        self.title = title
        self.quantity = quantity
        self.lended = lended
        self.price = price
    
    @staticmethod
    def get_book_from_csv_by_bcode(bcode):
        # Mở tệp CSV và tìm kiếm cuốn sách có mã bcode tương ứng
        with open('../Data/books.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == bcode:
                    # Nếu tìm thấy cuốn sách có mã bcode, tạo một đối tượng Book từ thông tin đọc được và trả về
                    return Book(row[0], row[1], int(row[2]), int(row[3]), float(row[4]))

        # Nếu không tìm thấy cuốn sách, trả về None
        return None
    
    @staticmethod
    def increase_lended_in_books_csv(bcode):
        # Đường dẫn đến file books.csv
        csv_file_path = "../Data/books.csv"
        # Tạo một danh sách tạm thời để lưu trữ dữ liệu đọc từ file
        temp_data = []

        # Đọc dữ liệu từ file và lưu vào danh sách tạm thời
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Kiểm tra nếu mã sách của dòng hiện tại trùng với bcode cần cập nhật
                if row[0] == bcode:
                    # Cập nhật giá trị lended mới
                    book = Book.get_book_from_csv_by_bcode(bcode)
                    if book:
                        row[3] = str(book.lended + 1)
                # Thêm dòng hiện tại vào danh sách tạm thời
                temp_data.append(row)

        # Ghi lại dữ liệu đã được cập nhật vào file
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(temp_data)
            
    @staticmethod
    def decrease_lended_in_books_csv(bcode):
        # Đường dẫn đến file books.csv
        csv_file_path = "../Data/books.csv"
        # Tạo một danh sách tạm thời để lưu trữ dữ liệu đọc từ file
        temp_data = []

        # Đọc dữ liệu từ file và lưu vào danh sách tạm thời
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Kiểm tra nếu mã sách của dòng hiện tại trùng với bcode cần cập nhật
                if row[0] == bcode:
                    # Cập nhật giá trị lended mới
                    book = Book.get_book_from_csv_by_bcode(bcode)
                    if book:
                        row[3] = str(book.lended - 1)
                # Thêm dòng hiện tại vào danh sách tạm thời
                temp_data.append(row)

        # Ghi lại dữ liệu đã được cập nhật vào file
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(temp_data)
