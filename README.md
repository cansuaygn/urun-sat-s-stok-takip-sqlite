# Ürün – Satış – Stok Takip Sistemi (Python + SQLite)

Bu projede Python ve SQL birlikte kullanılarak basit bir stok ve satış takip sistemi geliştirildi.

Amaç, SQL komutlarını ezberlemek yerine Python ile gerçek bir senaryo içinde kullanmayı öğrenmekti.

## Projede Neler Yapılıyor?

- Ürün eklenebiliyor
- Ürünler listelenebiliyor
- Satış yapılabiliyor
- Satış yapıldığında stok otomatik düşüyor
- Yapılan satışlar listelenebiliyor
- Toplam ciro hesaplanabiliyor
- Ürün silme ve güncelleme işlemleri yapılabiliyor
- En çok satılan ürün bulunabiliyor

## Kullanılan Teknolojiler

- Python
- SQLite (`sqlite3`)
- SQL (CREATE, INSERT, SELECT, UPDATE, DELETE, JOIN)

ORM kullanılmadı.  
Tüm SQL sorguları string olarak yazıldı.

## Neden SQLite?

- Ekstra kurulum gerektirmiyor
- Küçük projeler için yeterli
- SQL mantığını öğrenmek için ideal

## Örnek Kullanım

```python
create_tables()

add_product("Laptop", 25000, 10)
add_product("Mouse", 500, 50)

make_sale(1, 2)
make_sale(2, 5)

list_products()
list_sales()
