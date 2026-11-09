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

AI DISCLOSURE: Tugas ini menggunakan bantuan Codex untuk mengecek kesesuaian dengan ketentuan implementasi pada tugas, mengimplementasikan pencarian AJAX dengan debouncing, modal tambah Education, toast, sanitasi input, dan pengujian backend.

1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!
   Jawaban: Debouncing menunda pencarian hingga pengguna berhenti mengetik selama waktu tertentu. Ini mengurangi permintaan AJAX yang berlebihan sehingga beban server lebih ringan.

2. Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?
   Jawaban: await menunggu Promise dari fetch() selesai sebelum kode berikutnya dalam fungsi async dijalankan, tanpa memblokir seluruh halaman. Tanpa await atau penanganan melalui .then(), hasilnya masih berupa Promise, sehingga respons belum bisa langsung dibaca melalui response.json().

3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!
   Jawaban: XSS adalah serangan yang menyisipkan script berbahaya agar dijalankan di browser pengguna. Template Django secara default melakukan escaping, sedangkan data AJAX yang dimasukkan melalui innerHTML tidak otoatis di-escape sehingga lebih berisiko jika dibiarkan. Oleh karena itu, teks ditampilkan melalui textContent dan input dibersihkan di server menggunakan strip_tags.

DOKUMENTASI: Pada Tugas 5, halaman Education memuat data beserta informasi star melalui AJAX, dilengkapi pencarian berdasarkan institusi dengan debouncing 300 ms serta tampilan loading, kosong, dan error. Superuser dapat menambahkan pendidikan melalui modal menggunakan AJAX tanpa reload halaman, dengan validasi ModelForm, proteksi CSRF, dan notifikasi toast. Perlindungan XSS diterapkan melalui textContent di sisi JavaScript dan strip_tags pada field teks di sisi server.


### Tugas 6

AI DISCLOSURE: Tugas ini menggunakan bantuan Claude dan Gemini untuk membantu pengecekan kesesuaian checklist penugasan, perancangan arsitektur permission class berbasis peran pada DRF, penambahan validasi tanggal pada serializer, implementasi endpoint API berbasis fungsi, dan penyusunan test suite APITestCase.

1. Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!
   Jawaban: REST adalah gaya arsitektur sistem web berbasis standar seperti resource-based URI, statelessness, dan HTTP verbs, sehingga mengembalikan JSON saja belum cukup tanpa mematuhi prinsip-prinsip tersebut. PUT digunakan untuk memperbarui seluruh data resource secara utuh (misalnya form edit profil pendidikan lengkap), sedangkan PATCH digunakan untuk memperbarui sebagian field saja tanpa menimpa data lainnya (misalnya hanya mengubah tanggal selesai).

2. Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?
   Jawaban: Serializer bertindak sebagai jembatan untuk mengubah instance model menjadi format JSON (serialisasi) sekaligus memvalidasi data masukan dari klien sebelum disimpan ke database (deserialisasi). Keuntungannya adalah menyediakan validasi tipe data otomatis, sanitasi teks terpusat, dan struktur pesan error yang konsisten tanpa perlu menulis percabangan dictionary manual.

3. Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?
   Jawaban: Autentikasi memverifikasi identitas pengguna yang sedang mengakses sistem, sedangkan otorisasi menentukan tindakan atau hak akses apa saja yang diizinkan untuk pengguna tersebut. Pemeriksaan hak akses wajib dilakukan di server melalui permission class karena elemen antarmuka di template dapat dengan mudah di-bypass menggunakan HTTP request langsung seperti cURL atau Postman.

4. Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?
   Jawaban: Permintaan pengubah data tetap memerlukan token CSRF karena SessionAuthentication memanfaatkan cookie sesi browser yang rentan terhadap pemalsuan request dari situs pihak ketiga (CSRF). Pengujian dengan force_authenticate tidak cukup untuk membuktikan proteksi ini karena fungsi tersebut sengaja melewati seluruh pipeline autentikasi dan middleware CSRF bawaan Django.

DOKUMENTASI: Pada Tugas 6, diimplementasikan REST API menggunakan Django REST Framework (DRF) untuk entitas Education dan Project. Dibuat ModelSerializer dengan field eksplisit, field read-only untuk informasi star (star_count dan is_starred), sanitasi teks menggunakan strip_tags pada method validate_<field>(), serta validasi rentang tanggal. Hak akses dikelola secara modular pada permission class (IsPortfolioOwnerOrEditorOrReadOnly dan IsPortfolioOwnerOrReadOnly) yang membedakan hak akses untuk 4 peran (Pengunjung, Pengguna Biasa, Editor, dan Pemilik Portofolio/Superuser). Endpoint API berbasis fungsi dibuat dengan @api_view dan SessionAuthentication di bawah prefix /api/v1/ dengan parameter query untuk pencarian, didukung status HTTP yang semantik (200, 201, 204, 400, 403, 404). Halaman frontend diintegrasikan dengan Fetch API untuk operasi CRUD dan star tanpa reload halaman, dilengkapi notifikasi toast, perlindungan XSS, dan token CSRF. Seluruh fungsionalitas diuji secara komprehensif menggunakan APITestCase sebanyak 32 test case baru (total 57 test lulus tanpa error).




