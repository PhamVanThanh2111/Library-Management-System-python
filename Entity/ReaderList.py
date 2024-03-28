from ReaderNode import ReaderNode
from Reader import Reader
import csv

class ReaderList:
    def __init__(self):
        self.head = None

    def add_reader(self, reader):
        if not self.head:
            self.head = ReaderNode(reader)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = ReaderNode(reader)
            
    def insert_to_csv(self, reader):
        with open('../Data/readers.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([reader.rcode, reader.name, reader.byear])

    def search(self, rcode):
        current = self.head
        while current:
            if current.reader.rcode == rcode:
                return current.reader
            current = current.next
        return None

    def delete(self, rcode):
        if not self.head:
            return
        if self.head.reader.rcode == rcode:
            self.head = self.head.next
            return
        prev = self.head
        current = self.head.next
        while current:
            if current.reader.rcode == rcode:
                prev.next = current.next
                return
            prev = current
            current = current.next

    def update(self, rcode, new_reader):
        current = self.head
        while current:
            if current.reader.rcode == rcode:
                current.reader = new_reader
                return
            current = current.next
        print("Không tìm thấy độc giả!")
        
    def load_from_csv(self, file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                rcode = row['rcode']
                name = row['name']
                byear = int(row['byear'])
                reader = Reader(rcode, name, byear)
                self.add_reader(reader)
                
    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            current = self.head
            while current:
                file.write(f"{current.reader.rcode},{current.reader.name},{current.reader.byear}\n")
                current = current.next
                
    def display_readers(self):
        current = self.head
        while current:
            print("rcode:", current.reader.rcode)
            print("name:", current.reader.name)
            print("byear:", current.reader.byear)
            print()
            current = current.next
