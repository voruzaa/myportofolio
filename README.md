Nama : Forza Derian
NPM : 2506596041
Kelas : PBP F

Pertanyaan Reflektif (Tugas 1):

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

Pertanyaan Reflektif (Tugas 2):

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
