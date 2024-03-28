from BookNode import BookNode
from Book import Book
from collections import deque
import csv

class BookList:
    def __init__(self):
        self.root = None

    def insert(self, book):
        if not self.root:
            self.root = BookNode(book)
        else:
            self._insert_recursive(self.root, book)
            # Ghi dữ liệu vào tệp books.csv

    def insert_to_csv(self, book):
        with open('../Data/books.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([book.bcode, book.title, book.quantity, book.lended, book.price])

    def _insert_recursive(self, node, book):
        if book.bcode < node.book.bcode:
            if node.left:
                self._insert_recursive(node.left, book)
            else:
                node.left = BookNode(book)
        elif book.bcode > node.book.bcode:
            if node.right:
                self._insert_recursive(node.right, book)
            else:
                node.right = BookNode(book)
        else:
            # Handle case when book with same bcode already exists
            pass
        
    
    def delete_by_bcode_copying(self, bcode):
        self.root = self._delete_by_bcode_copying_recursive(self.root, bcode)
        
    def _delete_by_bcode_copying_recursive(self, node, bcode):
        if not node:
            return None
        
        # Nếu mã sách cần xóa nhỏ hơn mã sách của node hiện tại, điều hướng sang node con trái
        if bcode < node.book.bcode:
            node.left = self._delete_by_bcode_copying_recursive(node.left, bcode)
        # Nếu mã sách cần xóa lớn hơn mã sách của node hiện tại, điều hướng sang node con phải
        elif bcode > node.book.bcode:
            node.right = self._delete_by_bcode_copying_recursive(node.right, bcode)
        # Nếu mã sách cần xóa bằng với mã sách của node hiện tại
        else:
            # Trường hợp node có ít hơn hoặc không có node con trái
            if not node.left:
                return node.right
            # Trường hợp node có ít hơn hoặc không có node con phải
            elif not node.right:
                return node.left
            # Trường hợp node có cả hai node con
            else:
                # Tìm node kế thừa (node nhỏ nhất ở phần cây con phải)
                successor = self._find_min_node(node.right)
                # Sao chép thông tin từ node kế thừa vào node hiện tại
                node.book = successor.book
                # Xóa node kế thừa từ cây con phải
                node.right = self._delete_by_bcode_copying_recursive(node.right, successor.book.bcode)
        
        return node
    
    def _find_min_node(self, node):
        current = node
        # Tìm node nhỏ nhất trong cây con bằng cách đi sang trái đến khi không còn node con trái nữa
        while current.left:
            current = current.left
        return current
    
    def update(self, bcode, new_book):
        node = self.search(bcode)
        if node:
            node.book = new_book
        else:
            print("Book not found")

    def search(self, bcode):
        return self._search_recursive(self.root, bcode)

    def _search_recursive(self, node, bcode):
        if not node:
            return "Không tìm thấy sách với mã sách cần tìm"
        elif node.book.bcode == bcode:
            return node
        elif bcode < node.book.bcode:
            return self._search_recursive(node.left, bcode)
        else:
            return self._search_recursive(node.right, bcode)
    
    def head(self):
        return self._head_recursive(self.root)
    
    def _head_recursive(self, node):
        if not node:
            return None
        while node.left:
            node = node.left
        return node
    
    def load_from_csv(self, file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bcode = row['bcode']
                title = row['title']
                quantity = int(row['quantity'])
                lended = int(row['lended'])
                price = float(row['price'])
                book = Book(bcode, title, quantity, lended, price)
                self.insert(book)
    
    def in_order_traversal(self):
        result = []
        self._in_order_traversal_recursive(self.root, result)
        return result

    def _in_order_traversal_recursive(self, node, result):
        if node:
            # Duyệt qua node con trái
            self._in_order_traversal_recursive(node.left, result)
            # Thêm thông tin của node gốc vào kết quả
            result.append((node.book.bcode, node.book.title, node.book.quantity, node.book.lended, node.book.price))
            # Duyệt qua node con phải
            self._in_order_traversal_recursive(node.right, result)

    # Sử dụng hàng đợi (queue) để duyệt cây theo chiều rộng (breadth-first traversal
    def breadth_first_traversal(self):
        result = []
        if not self.root:
            return result

        queue = deque()
        queue.append(self.root)

        while queue:
            node = queue.popleft()
            result.append((node.book.bcode, node.book.title, node.book.quantity, node.book.lended, node.book.price))

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
        return result
    
    # in-order traversal trên cây nhị phân lưu trữ các cuốn sách và ghi thông tin vào một tệp
    def in_order_traverse_to_file(self, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['bcode', 'title', 'quantity', 'lended', 'price'])
            self._in_order_traverse_to_file_recursive(self.root, writer)

    def _in_order_traverse_to_file_recursive(self, node, writer):
        if node:
            self._in_order_traverse_to_file_recursive(node.left, writer)
            writer.writerow([node.book.bcode, node.book.title, node.book.quantity, node.book.lended, node.book.price])
            self._in_order_traverse_to_file_recursive(node.right, writer)
            
    def simply_balancing(self):
        # Thực hiện in-order traversal để lấy ra danh sách các cuốn sách theo thứ tự tăng dần của bcode
        books = self.in_order_traversal()

        # Xóa toàn bộ nút cũ
        self.root = None

        # Xây dựng lại cây từ danh sách các cuốn sách đã được sắp xếp
        self.root = self._build_balanced_tree(books, 0, len(books) - 1)

    def _build_balanced_tree(self, books, start, end):
        if start > end:
            return None

        # Tìm giá trị trung bình của start và end để chọn giữa cuốn sách ở giữa làm root node
        mid = (start + end) // 2
        mid_book = books[mid]

        # Tạo root node từ cuốn sách ở giữa
        root = BookNode(mid_book)

        # Đệ quy xây dựng cây con trái từ cuốn sách bên trái của cuốn sách ở giữa
        root.left = self._build_balanced_tree(books, start, mid - 1)
        # Đệ quy xây dựng cây con phải từ cuốn sách bên phải của cuốn sách ở giữa
        root.right = self._build_balanced_tree(books, mid + 1, end)

        return root
    
    def count_number_of_books(self):
        return self._count_number_of_books_recursive(self.root)

    def _count_number_of_books_recursive(self, node):
        if not node:
            return 0
        # Đếm số lượng cuốn sách trong cây con trái và phải, sau đó cộng lại với 1 (đếm node hiện tại)
        return self._count_number_of_books_recursive(node.left) + self._count_number_of_books_recursive(node.right) + 1
    
    def display_books(self):
        books = self.in_order_traversal()
        for book in books:
            print("bcode:", book[0])
            print("title:", book[1])
            print("quantity:", book[2])
            print("lended:", book[3])
            print("price:", book[4])
            print()