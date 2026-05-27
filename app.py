from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel

app = FastAPI()
connection = psycopg2.connect(
    host = 'localhost',
    database = 'Library',
    port = 5432,
    user = 'postgres',
    password = 'root'
)
cursor = connection.cursor()

class Book(BaseModel):      
    title : str
    author : str
    category : str
    published_year : int
    available_copies : int

@app.get('/')
def home_page():
    return {'Hello World'}

@app.get('/View_all')
def View_all():
    cursor.execute('select * from books')
    records = cursor.fetchall()
    result = []
    for row in records:
        result.append({
        'id': row[0],
        'title' : row[1],
        'author' : row[2],
        'category' : row[3],
        'published_year' : row[4],
        'available_copies' : row[5]
        })
    return result

#Get single book
@app.get("/view_book/{id}")
def view_single_book(id : int):
    cursor.execute('select * from books where book_id = %s', (id,))
    record = cursor.fetchone()
    return {
        'id': record[0],
        'title' : record[1],
        'author' : record[2],
        'category' : record[3],
        'published_year' : record[4],
        'available_copies' : record[5]
    }

@app.post('/insert_books')
def insert_books(book : Book):
    cursor.execute('insert into books (title, author, category, published_year, available_copies) values(%s,%s,%s,%s,%s)',(book.title, book.author, book.category, book.published_year, book.available_copies))
    connection.commit()
    return {'message' : 'Book added successfully'}

@app.put('/update_books/{id}')
def update_books(id : int,book : Book):
    cursor.execute('update books set title = %s, author = %s, category = %s, published_year = %s, available_copies = %s where book_id = %s',(book.title, book.author, book.category, book.published_year, book.available_copies,id))
    connection.commit()
    return {'message' : 'Books updated successfully'}

@app.delete('/delete_book/{id}')
def delete_book(id: int):
    cursor.execute('delete from books where book_id = %s', (id,))
    connection.commit()
    return {'message': 'Book deleted successfully'}

