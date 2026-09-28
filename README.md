Nama : Kevin R

NPM : 2506621466

Kelas : PBP C

#Hi from another branch

# 7/9/2026 - Tugas 1
## A.Weekly Instruction Step :
1. Clone this repository
    git clone https://github.com/ke-Vyn/myportofolio.git
    cd myportofolio
2. Create a virtual environment and activate it
    python -m venv env
    env\Scripts\activate
3. Install Dependencies 
    pip install -r requirements.txt
4. Run server
    python manage.py runserver
5. Open `http://localhost:8000` in any browser

## B. Weekly Updates :
1. Added a new Highlights section containing 3 cards: Skill, Education, Projects 
2. Added a navigation button in the social links area that scrolls to the new section via anchor link (#highlights)
3. CSS styling:
    a. 3 column grid layout (display: grid), collapses into a single column on mobile / smaller screen
    b. Hover effect on each card (lift & shadow)
    c. Short fade-in entrance animation (@keyframes) when the page loads
4. Adjusted the Hero section to fill the full viewport height (min-height: 100vh) so that Highlights stays hidden until the user scrolls
5. Replaced all sample data with my own information

## C. Reflection :
### Assignment 1
1. Yes, i used semantic HTML5 elements (`<header>`, `<main>`, `<section>`, `<footer>`) to structure the page based on its content's purpose. I separated the "About Me" content into a `<section class="hero">` and the new content into `<section class="Highlights">`. I also used `<dl>`, `<dt>` and `<dd>` to display NPM and study program since they're a label value pair. This made the structure easier to read from the HTML, and should also make the page look more readable for readers.

2. The main challenge was deciding how elements should reflow when the grid changes from 2 column to 1 column (mobile). On laptop / desktop, the hero section places the photo beside the identity and details using 'grid-template-areas'. If it wasn't reordered, the photo could end up appearing last, even though it's one of more important elements. I addressed this by rearranging 'grid-template'areas' so the order becomes identity > photo > details when stacked vertically on mobile. I also set the photo's maximum width to 220px on mobile so that it wouldn't dominate smaller screen. For the highlights section, i changed the grid from 3 columns to 1 column below 700px, so each card would have enough horizontal space to read comfortably.

3. Static website forces me to write every content directly into the HTML and redeploy it whenever theres changes. This becomes limiting if i want to frequently add new contents. Not only that, it also limits the website's ability to process visitor input. For example, the current "Email" button only uses a mail:to link, which opens the visitor's email client instead of allowing the web to process the message directly. For the next iteration, i'd like to add a database so contents can easily managed through an admin panel without directly editing the index.html file.

## D. AI Disclosure : 
- Tool used: Gemini AI
- How it was used: Discussed suitable CSS styling approaches, such as: grid layout, hover effects and entrance animation, for the highlights section and hero layout, based on a web design i previously created in Figma without implementing JavaScript and relying solely on CSS3

---

# 14/9/2026 - Tugas 2
## A. Weekly Instruction Step :
1. Clone this repository
    git clone https://github.com/ke-Vyn/myportofolio.git
    cd myportofolio
2. Create a virtual environment and activate it
    python -m venv env
    env\Scripts\activate
3. Install Dependencies 
    pip install -r requirements.txt
4. Run server
    python manage.py runserver
5. Open `http://localhost:8000` in any browser

## B. Weekly Updates :
1. Menerapkan Model View Template (MVT) untuk dua section, yaitu Experience dan Projects, masing-masing dengan model, view, dan template Django-nya sendiri
2. Menambahkan routing untuk /experience/ dan /projects/ di main/urls.py dan menghubungkan navigasi antar halaman lewat navbar
3. Mengubah kartu "Projects" di section Highlights menjadi link dinamis menuju GitHub dan halaman Projects yang baru
4. Menambahkan unit test (memastikan URL dapat diakses, template yang digunakan benar dan data model tampil dengan baik)


## C. Reflection :
### Assignment 2
1. Ketika user membuka /projects/, request diterima oleh urls.py project, lalu diteruskan ke urls.py aplikasi main melalui include(). Di main/urls.py, path "projects/" dicocokkan dengan fungsi view show_projects, yang kemudian mengambil seluruh data dari model Project lewat Project.objects.all(), memasukkannya ke dalam context, lalu memanggil render() untuk menggabungkan data tersebut dengan template projects.html. Template mengubah data menjadi HTML, kemudian dikirim sebagai reponse dan ditampilkan di browser

2. Data disimpan di model agar data dan tampilan terpisah sehingga mengubah tampilan cukup dilakukan dengan mengedit template tanpa menyentuh data. Selain itu, mengubah data dapat dilakukan lewat database tanpa mengedit HTML secara manual. Hal ini membuat pengembangan aplikasi lebih mudah karena tidak memerlukan redeploy kode ulang setiap data berubah, data bisa divalidasi secara konsisten oleh Django (misalnya URLField), dan data tersebut dapat difilter / ditampilkan ulang di halaman lain tanpa perlu tulis ulang kode HTML

3. - makemigrations --> membuat file migration berdasarkan perubahan pada `models.py`, tetapi belum menerapkannya ke database.
   - migrate --> menerapkan migration tersebut ke database yang aktif.
     Contoh : Saat menambahkan model `Project` dengan field `title`, `description`, `tech_stack`, dan `project_url`, jalankan `makemigrations` untuk membuat migration, lalu `migrate` untuk membuat tabel `Project` di database.

## D. AI Disclosure : 
- Tool used: Claude.ai
- How it was used: Diskusi mengenai alur MVT untuk section Experience dan Projects, termasuk desain field model, struktur view/context, dan sintaks Django Template Language untuk loop dan empty state. Selain itu, Ai juga digunakan untuk debugging masalah saat deployment di PWS, seperti perbedaan database lokal dan production

---

# 21/9/2026 - Tugas 3
## A. Weekly Instruction Step :
1. Clone this repository
    git clone https://github.com/ke-Vyn/myportofolio.git
    cd myportofolio
2. Create a virtual environment and activate it
    python -m venv env
    env\Scripts\activate
3. Install Dependencies 
    pip install -r requirements.txt
4. Run server
    python manage.py runserver
5. Open `http://localhost:8000` in any browser

## B. Weekly Updates :
1. Menerapkan template inheritance menggunakan base.html sebagai kerangka utama halaman (navbar, head, dan footer)
2. Mengimplementasikan fitur Create & Delete pada bagian Projects, serta endpoint data JSON via Django serializers
3. Menambahkan section Education dengan model, form, fungsionalitas penuh CRUD, serta endpoint JSON
4. Mengintegrasikan rute halaman Education ke dalam navbar di base.html

## C. Reflection : 
### Assignment 3
1. A. Modelform digunakan karena secara otomatis memetakan field input HTML sesuai tipe data dan validasi pada model Django (contoh: validasi format URL,batas panjang karakter, ataau status required). Selain itu, `ModelForm` menyediakan method `save()` yang otomatis menangani logika *insert* & *update* ke database tanpa query manual, sehingga meminimalkan redundansi kode dan mencegah inkonsistensi antara struktur form & database
   B. Fungsi `{% csrf_token %}` untuk melindungi aplikasi dari serangan Cross-Site Request Forgery, yaitu upaya pihak luar mengirimkan request seperti submit form atas nama sesi/identitas pengguna yang sedang aktif. Token ini memastikan bahwa data yang diproses server benar-benar berasal dari form resmi aplikasi sendiri, bukan situs luar/eksternal

2. -Struktur data lebih ringkas: JSON menggunakan format pasangan key-value tanpa memerlukan tag (`<tag>...</tag>`) pada XML , sehingga ukuran payload jaringan lebih kecil dan transmisi data lebih cepat.
   -JSON bersifat native terhadap JavaScript, sehingga dapat langsung diubah menjadi objek menggunakan `JSON.parse()` tanpa memerlukan parser tambahan seperti pada XML
   -JSON lebih _human-readable_ dan didukung oleh banyak bahasa pemrograman modern, sehingga menjadi format standar yang efisien untuk data delivery

3. A.Alur Pengembalian Data:
   1. Data entitas diambil dari database melalui Django ORM (misalnya `Education.objects.all()`), menghasilkan QuerySet berupa sekumpulan objek Python
   2. QuerySet diproses melalui `serializers.serialize('json', ...)` untuk diubah menjadi string JSON, lalu dibungkus ke dalam `HttpResponse` dengan header `content_type="application/json"` agar dikenali dengan tepat oleh user
   3. Pada halaman yang menampilkan data, string JSON tersebut dideserialisasi kembali (`serializers.deserialize()`) menjadi objek model, agar dapat dimasukkan ke context dan ditampilkan oleh template engine Django

   B.Pentingnya Serialization: Protokol HTTP hanya dapat mentransmisikan data dalam bentuk  raw text / binary, bukan struktur objek dalam memori internal Python. Serialization bertindak sebagai penerjemah yang mengonversi objek model kompleks Django menjadi format teks universal (seperti JSON) yang dapat dikirim melalui internet dan dipahami oleh berbagai platform user

## D. AI Closure : 
- Tool used: Claude.ai
- How it was used: 
    -Diskusi mengenai konsep template inheritance, seperti perbedaan struktur file sebelum/sesudah menggunakan `{% extends %}`, dan bagian-bagian /templates/ yang harus dipindahkan ke base.html
    -Diskusi fungsi Create & Update seperti pemahaman parameter `instance=` pada `ModelForm`
    -Debugging bug ketika isi berkas education.html dan education_form.html tertukar (membandingkan kode di kedua berkas sekaligus melihat apa yang terjadi pada preview local dengan runserver)

---
# 28/9/2026 - Tugas 4
## A. Weekly Instruction Step :
1. Clone this repository
    git clone https://github.com/ke-Vyn/myportofolio.git
    cd myportofolio
2. Create a virtual environment and activate it
    python -m venv env
    env\Scripts\activate
3. Install Dependencies 
    pip install -r requirements.txt
4. Run server
    python manage.py runserver
5. Open `http://localhost:8000` in any browser

## B. Weekly Updates :
1. Menambahkan role Editor lewat Django `Group` dan menerapkan pembatasan hak akses server untuk 4 role (pengunjung, pengguna biasa, editor, pemilik) pada view Projects dan Education
2. Menambahkan view `update_project` dan penyesuaian tombol Tambah/Edit/Hapus pada template sesuai role pengguna
3. Menambahkan button toggle star Projects, serta jumlah star dan status pengguna; membatasi field pada endpoint `/api/projects/` agar `starred_by` tidak terekspos

## D. AI Closure : 
- Tool used: Gemini AI
- How it was used: diskusi konsep otorisasi berbasis role (`@login_required` sebelum pengecekan role / Principle of Least Privilege), serta debugging beberapa kesalahan kecil