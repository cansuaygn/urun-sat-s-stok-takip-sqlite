# Ürün – Satış – Stok Takip Sistemi (Python + SQLite)

Bu proje, Python ve SQLite kullanılarak hazırlanmış basit bir ürün / stok / satış takip sistemidir.

Bu projeyi yapma amacım SQL komutlarını ezberlemek yerine, Python içinde gerçek bir senaryo ile tekrar etmekti.

## Projede Neler Yapılabiliyor?

- Ürün ekleme
- Ürünleri listeleme
- Satış yapma
- Satış yapınca stok düşürme
- Satışları listeleme
- Toplam ciroyu hesaplama
- Ürün silme (ID ile)
- Ürün güncelleme (fiyat ve stok)
- En çok satılan ürünü bulma

## Kullanılan Yapılar

- Python (`sqlite3`)
- SQLite veritabanı
- SQL komutları:
  - CREATE TABLE
  - INSERT
  - SELECT
  - UPDATE
  - DELETE
  - JOIN
  - SUM / GROUP BY

## Kurallar

- ORM kullanılmadı (SQLAlchemy yok)
- SQL sorguları string olarak yazıldı
- Her fonksiyon tek iş yapacak şekilde yazıldı
- Veritabanı işlemlerinde `commit()` unutulmadı

## Çalıştırma

Terminalden dosyayı çalıştır:

```bash
python stok_satis_sistemi.py

