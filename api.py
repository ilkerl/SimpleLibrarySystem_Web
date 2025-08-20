# api.py

# Gerekli modülleri import et
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# PostgreSQL kullanan güncel Library sınıfını import et
from library import Library

# --- 1. FastAPI uygulamasını oluştur ---
app = FastAPI(
    title="Simple Library API",
    description="An API for managing a small book library using a persistent PostgreSQL database.",
    version="2.0.0" # Sürümü güncelleyelim
)

# --- 2. CORS Ayarları ---
# Web sitesinin API'ye erişebilmesi için gerekli
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Veritabanı Bağlantısını Ayarla ---
# Render'da ayarlayacağımız DATABASE_URL ortam değişkenini oku
DATABASE_URL = os.getenv("DATABASE_URL")

# Eğer ortam değişkeni ayarlanmamışsa, programı bir hata ile durdur
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set! The application cannot start.")

# Library sınıfını, veritabanı bağlantı URL'si ile başlat
# Bu, tüm API'nin kullanacağı tek veritabanı bağlantı nesnesidir
lib = Library(db_url=DATABASE_URL)


# --- 4. Pydantic Veri Modelleri ---
# API'nin girdi ve çıktı veri yapılarını tanımlar (değişiklik yok)
class BookModel(BaseModel):
    title: str
    author: str
    isbn: str

class ISBNModel(BaseModel):
    isbn: str


# --- 5. API Uç Noktaları (Endpoints) ---

@app.get("/books", response_model=List[BookModel])
def get_books():
    """
    Kütüphanedeki tüm kitapların listesini veritabanından getirir.
    """
    # lib.list_books() artık doğrudan JSON uyumlu bir sözlük listesi döndürüyor
    return lib.list_books()


@app.post("/books", response_model=BookModel, status_code=201)
def add_book_by_isbn(item: ISBNModel):
    """
    ISBN kullanarak yeni bir kitap ekler ve veritabanına kaydeder.
    """
    new_book = lib.add_book(item.isbn)
    if new_book is None:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ISBN {item.isbn} not found or already exists in the database."
        )
    # Dönen Book nesnesi Pydantic modeliyle uyumlu olduğu için doğrudan döndürülebilir
    return new_book


@app.delete("/books/{isbn}", status_code=200)
def delete_book(isbn: str):
    """
    ISBN kullanarak bir kitabı veritabanından siler.
    """
    was_removed = lib.remove_book(isbn)
    if not was_removed:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ISBN {isbn} not found in the database."
        )
    return {"message": "Book successfully deleted", "isbn": isbn}
