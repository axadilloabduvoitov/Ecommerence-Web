# NovaStore — yangilangan Django shop

Loyiha Django 6.1 uchun tayyorlangan.

## Nimalar tuzatildi?

- Mahsulot kartochkasini bosganda alohida chiroyli detail sahifasi ochiladi.
- Mahsulot rasmi, nomi va narxi detail sahifasiga olib boradi.
- Savatga qo'shish uchun login/register talab qilinadi.
- Sevimliga qo'shish uchun login/register talab qilinadi.
- Savat Django bazasida saqlanadi, faqat brauzer localStorage'iga bog'liq emas.
- `−` va `+` tugmalari bilan mahsulot soni boshqariladi.
- Bir mahsulot soni 1 dan 100 gacha va ombordagi mavjud sondan oshmaydi.
- Har bir mahsulotning subtotali va savatning umumiy summasi real narx × son bo'yicha hisoblanadi.
- `$0.00` olib tashlandi; narxlar `so'm` ko'rinishida chiqadi.
- 5 ta kategoriya tayyor:
  1. Noutbuklar
  2. Smartfonlar
  3. Kompyuter aksessuarlari
  4. Maishiy texnika
  5. Elektronika
- Eski mahsulotlar bazadan tozalandi.
- Admin panelda kategoriya, mahsulot, savat va sevimlilarni boshqarish qulaylashtirildi.
- Mahsulotlarni kategoriya bo'yicha filtrlash va qidirish qo'shildi.
- Bosh sahifa va detail sahifalari NovaStore dizayniga moslashtirildi.
- Mobil ko'rinish ham moslashtirildi.

## Ishga tushirish

Terminalni `myproject` papkasida oching:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Keyin:

`http://127.0.0.1:8000/`

Admin:

`http://127.0.0.1:8000/admin/`

ZIP ichidagi `db.sqlite3` da avvalgi `admin` superuser saqlanib qolgan. Uning paroli o'zgartirilmagan.

## Admin paneldan mahsulot qo'shish

1. `/admin/` ga kiring.
2. **Kategoriyalar** bo'limidan 5 ta kategoriya tayyorligini tekshiring.
3. **Mahsulotlar** → Add Product.
4. Kategoriya tanlang.
5. Mahsulot nomi, narxi, ombordagi soni va rasmini kiriting.
6. `Faol`ni yoqing.
7. Saqlang.

Mahsulot narxini masalan `1299000` qilib kiritsangiz, saytda `1,299,000 so'm` ko'rinishida chiqadi.
