# Python'un resmi, hafif bir imajını kullan
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /code

# Bağımlılık dosyalarını kopyala (requirements.txt olduğunu varsayıyoruz)
COPY ./requirements.txt /code/requirements.txt

# Bağımlılıkları yükle
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Proje dosyalarının tamamını kopyala
COPY ./ /code/

# Uygulamanın çalışacağı portu belirt (FastAPI genellikle 8000 portunda çalışır)
EXPOSE 8000

# Uygulamayı Uvicorn ile başlat
# ÖNEMLİ: "main:app" kısmını kendi dosya ve FastAPI uygulama adınıza göre güncelleyin.
# Örneğin, dosyanız "api.py" ve uygulama `my_api = FastAPI()` ise bu satır "api:my_api" olmalı.
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]