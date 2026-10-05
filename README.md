Nama : Forza Derian
NPM : 2506596041
Kelas : PBP F

## Pertanyaan Reflektif (Tugas 1):

1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti <section>, <article>, atau <aside>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?
   Jawaban: Ya, saya menggunakan berbagai elemen semantik HTML5 seperti <header> <nav> <main> <section> dan <footer>, serta elemen semantik pendukung lainnya seperti <dl> <dt> <dd> dan <ol>.
   Penggunaan elemen semantik ini membagi halaman ke blok-blok kode yang terpisah, sehingga kode lebih readable.

2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?
   Jawaban: Tantangan utama yaitu menjaga keseimbangan layout agar tetap proporsional dan tidak terjadi horizontal overflow saat beralih dari layar desktop ke layar mobile yang lebih sempit.

3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?
   Jawaban:
   -Konten bersifat hardcoded di dalam file HTML. Setiap pembaruan data mengharuskan saya untuk mengubah source code secara langsung dan melakukan deployment ulang.
   -Tidak ada penyimpanan database.
   Fungsionalitas dinamis yang ingin dipersiapkan & ditambahkan:
   -Integrasi Model dan Database Django: Memanfaatkan fitur ORM Django untuk memodelkan data portofolio ke dalam database.

AI DISCLOSURE TUGAS 1:
Tugas ini dikerjakan menggunakan bantuan Gemini AI dalam berbagai aspek, seperti penambahan elemen yang bersifat repetitif, merapikan layout CSS, dan juga untuk bertanya mengenai kode saya.

## Pertanyaan Reflektif (Tugas 2):

1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.
   Jawaban: Browser mengirim HTTP request ke Django, lalu urls.py proyek meneruskannya ke urls.py aplikasi main yang mencocokkan pola URL dengan view yang sesuai. View memanggil model untuk mengambil data dari database, memasukkannya ke context, lalu merender template HTML yang akhirnya dikembalikan sebagai HTTP response ke browser.

2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.
   Jawaban: Menyimpan data di model memisahkan logika data dari tampilan, sehingga perubahan data cukup dilakukan di satu tempat (database) tanpa menyentuh kode template. Hal ini membuat aplikasi lebih mudah dipelihara, dikembangkan, dan mencegah duplikasi data di berbagai halaman.

3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.
   Jawaban: makemigrations membuat file migrasi berdasarkan perubahan yang terdeteksi pada models.py, sedangkan migrate menerapkan file migrasi tersebut ke database secara nyata. Contohnya ketika saya menambahkan model Education baru saya harus menjalankan makemigrations untuk menghasilkan 0002_education.py, lalu migrate agar tabel Education benar-benar terbentuk di database.

AI DISCLOSURE TUGAS 2:
Tugas ini dikerjakan menggunakan bantuan Gemini AI untuk membantu tahapan implementasi MVT dan penulisan unit test.

DOKUMENTASI TUGAS 2:
Pada Tugas 2, ditambahkan halaman Education sebagai bagian portofolio baru menggunakan MVT Django. Model Education didefinisikan di models.py dengan field institution, degree, description, started_at, dan ended_at, lalu dimigrasikan ke database. View show_education mengambil seluruh data Education dari database dan meneruskannya ke template education.html yang menampilkan setiap entri sebagai kartu menggunakan Django Template Language. Halaman ini dapat diakses melalui URL /education/ dan terhubung ke navbar di seluruh halaman portofolio.

## Tugas 3
1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!
   Jawaban: ModelForm digunakan karena secara otomatis menghasilkan form, memvalidasi input, dan menyimpan data langsung sesuai skema model tanpa perlu menulis kode HTML atau logika validasi berulang secara manual. Sementara itu, {% csrf_token %} wajib disertakan untuk melindungi aplikasi dari serangan Cross-Site Request Forgery (CSRF) dengan memastikan bahwa permintaan POST benar-benar berasal dari pengguna sah pada form aplikasi kita.


2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
   Jawaban: JSON lebih disukai karena sintaksnya jauh lebih ringkas dan ringan dibandingkan XML yang redundan dengan tag pembuka penutup, sehingga lebih hemat bandwidth dan cepat ditransmisikan. Selain itu, JSON didukung secara native oleh JavaScript sehingga dapat langsumg di-parse menjadi objek tanpa memerlukan parser XML eksternal yang rumit.


3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
   Jawaban: Alurnya dimulai saat fungsi view mengambil QuerySet data dari database, mengubahnya ke format string JSON menggunakan serializers.serialize(), lalu mengembalikannya melalui HttpResponse dengan content_type="application/json". Proses serialization perlu dilakukan karena QuerySet model Django adalah objek Python kompleks yang tidak dapat langsung dikirim melalui HTTP sebelum diubah ke format teks standar seperti JSON.


AI DISCLOSURE: Tugas ini dikerjakan mengguakan bantuan Gemini AI untuk membantu pembuatan ModelForm, implementasi operasi CRUD serta serialisasi data JSON.

DOKUMENTASI: Pada Tugas 3, diimplementasikan formulir dan pengelolaan data dinamis menggunakan ModelForm untuk entitas Education dan Project. Dibuat fitur CRUD lengkap (Create, Read, Update, Delete) beserta proteksi token CSRF dan flash messages untuk memberi umpan balik bagi pengguna. Selain itu, ditambahkan endpoint serialisasi JSON untuk menyajikan data portofolio secara terstruktur serta pemanfaatan deserialisasi data sebelum ditampilkan ke template HTML.

## Tugas 4
AI DISCLOSURE: Tugas ini dikerjakan dengan bantuan Claude AI untuk membantu 
implementasi sistem autentikasi dan otorisasi brbasis peran: pembuatan helper `_is_editor()`, 
penambahan `@login_required` dan `PermissionDenied` pada view CRUD, serta penyesuaian 
template agar tombol hanya tampil sesuai hak akses.

DOKUMENTASI: Pada Tugas 4, diterapkan sistem autentikasi dan otorisasi berbasis peran menggunakan Django Group. Ada 4 peran dengan hak akses berbeda: pengunjung: hanya dapat membaca, pengguna biasa: dapat memberikan star, Editor: dapat mengubah data, dan superuser: memiliki akses penuh CRUD. Selain itu, endpoint JSON dijaga agar tidak membocorkan data sensitif seperti informasi starred_by

### Tugas 5

AI DISCLOSURE: Tugas ini menggunakan bantuan Codex untuk mengecek kesesuaian dengan ketentuan tugas, mengimplementasikan pencarian AJAX dengan debouncing, modal tambah Education, toast, sanitasi input, serta pengujian backend. Codex juga membantu menyusun jawaban reflektif pada README.

1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

   Jawaban: Debouncing menunda pencarian hingga pengguna berhenti mengetik selama waktu tertentu, misalnya 300 ms. Teknik ini mengurangi permintaan AJAX yang berlebihan sehingga beban server lebih ringan dan pencarian lebih efisien.

2. Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?

   Jawaban: `await` menunggu Promise dari `fetch()` selesai sebelum kode berikutnya dalam fungsi async dijalankan, tanpa memblokir seluruh halaman. Tanpa `await` atau penanganan melalui `.then()`, hasilnya masih berupa Promise, sehingga respons belum bisa langsung dibaca melalui `response.json()`.

3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!

   Jawaban: XSS adalah serangan yang menyisipkan skrip berbahaya agar dijalankan di browser pengguna. Template Django secara default melakukan escaping, sedangkan data AJAX yang dimasukkan melalui `innerHTML` tidak otomatis di-escape sehingga lebih berisiko jika tidak ditangani. Karena itu, teks ditampilkan melalui `textContent` dan input dibersihkan di server menggunakan `strip_tags`.


