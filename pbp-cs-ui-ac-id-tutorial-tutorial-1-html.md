# Tutorial 01: Django Initial Project, HTML5 dan CSS3

Pemrograman Berbasis Platform (CSGE602022) - diselenggarakan oleh Fakultas Ilmu Komputer Universitas Indonesia, Semester Gasal 2026/2027

**Kontributor:** MUH - Hafiz

* * *

Peringatan

**Tutorial ini adalah prasyarat wajib untuk [Individual Assignment 1](https://pbp.cs.ui.ac.id/assignments/individual/tugas-1.html)** \- kalau belum diselesaikan, Individual Assignment 1 tidak akan dinilai. Deadline Tutorial 01 adalah **Rabu, 2 September 2026**; deadline Individual Assignment 1 adalah **Senin, 7 September 2026**. Lihat [halaman Jadwal](https://pbp.cs.ui.ac.id/index.html#jadwal-semester) untuk tanggal lengkap.

### Tujuan Pembelajaran [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#tujuan-pembelajaran)

Di ujung tutorial ini, kamu bakal bisa:

- Memahami struktur folder sebuah proyek Django dan fungsi tiap bagiannya.
- Menghubungkan sebuah _view_ Django ke sebuah _template_ HTML statis.
- Membangun struktur halaman dengan elemen semantik HTML5 (`header`, `main`, `section`, `footer`, dst).
- Mempercantik halaman tersebut dengan CSS3 (custom properties, Flexbox, CSS Grid, media query dasar).
- Men- _deploy_ proyek Django ke **PWS (Pacil Web Service)** supaya bisa diakses lewat internet.

Tutorial ini adalah **Tutorial 01**, lanjutan langsung dari [Tutorial 0](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html) \- tutorial kedua dari proyek yang akan kamu bangun berkelanjutan sepanjang semester: sebuah **website portofolio pribadi**. Semua tutorial berikutnya akan melanjutkan langsung dari hasil tutorial ini, jadi pastikan proyekmu berjalan dengan baik sebelum lanjut ke tutorial berikutnya.

Sepanjang tutorial ini, contoh yang dipakai adalah portofolio milik **Burhan**, maskot mata kuliah PBP. Setiap kali ada bagian yang berisi data pribadi Burhan (nama, NPM, bio, foto), akan ada catatan eksplisit yang bilang “ganti ini dengan data kamu sendiri” - jangan sampai kelewat.

Tip

Kalau kamu masih ingat, di [Tutorial 0](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html) kita berhenti persis setelah lihat halaman selamat datang Django - Git repository jalan, `env` aktif, Django terinstall, `startproject` udah dijalankan. Sekarang kita ganti halaman default itu dengan halaman “About Me” pertamamu.

Struktur folder proyekmu saat ini (hasil akhir Tutorial 0):

```
myportofolio/
├── env/
├── .git/
├── .gitignore
├── requirements.txt
├── db.sqlite3
├── manage.py
└── myportofolio/          # folder konfigurasi utama proyek
    ├── __init__.py
    ├── asgi.py
    ├── settings.py       # semua konfigurasi proyek ada di sini
    ├── urls.py           # daftar routing URL
    └── wsgi.py
```

PentingGanti Nama Folder Konfigurasi Django

Ada **dua** folder bernama `myportofolio` di atas - folder terluar adalah root proyekmu (tempat `manage.py` berada), folder di dalamnya adalah _package_ konfigurasi Django (tempat `settings.py` dan `urls.py` berada). Supaya keduanya tidak tertukar saat disebut di tutorial-tutorial berikutnya, ganti nama folder konfigurasi Django yang di dalam menjadi `portofolio` (folder terluar tetap `myportofolio`, sesuai nama repositori GitHub-mu):

```
mv myportofolio portofolio
```

Lalu ganti setiap `myportofolio.settings`, `myportofolio.urls`, dan `myportofolio.wsgi.application` menjadi `portofolio.settings`, `portofolio.urls`, `portofolio.wsgi.application` di 4 berkas berikut:

- `manage.py`
- `portofolio/settings.py` (baris `ROOT_URLCONF` dan `WSGI_APPLICATION`)
- `portofolio/wsgi.py`
- `portofolio/asgi.py`

Pastikan proyekmu masih berjalan normal setelah ini:

```
python manage.py check
```

## Menyiapkan Views, URL, Templates, dan Static Files [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#menyiapkan-views-url-templates-dan-static-files)

Buat sebuah _view_ sederhana yang mengembalikan sebuah _template_ HTML. Buat berkas `portofolio/views.py`:

```
from django.shortcuts import render

def landing_page(request):
    return render(request, "index.html")
```

Hubungkan _view_ ini ke URL kosong (`""`) di `portofolio/urls.py`:

```
from django.contrib import admin
from django.urls import path

from portofolio.views import landing_page

urlpatterns = [\
    path('admin/', admin.site.urls),\
    path('', landing_page, name='landing_page'),\
]
```

Buat folder `templates/`, `static/css/`, dan `static/img/` di root proyek (sejajar dengan `manage.py`), lalu daftarkan `templates/` dan `static/` di `portofolio/settings.py` supaya Django tahu harus mencari berkas HTML dan aset statis di sana:

```
TEMPLATES = [\
    {\
        'BACKEND': 'django.template.backends.django.DjangoTemplates',\
        'DIRS': [BASE_DIR / 'templates'],\
        ...\
    },\
]

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

`TEMPLATES.DIRS` memberitahu Django folder tambahan tempat mencari berkas `.html` yang dipanggil lewat `render()`. `STATICFILES_DIRS` melakukan hal yang sama untuk CSS/gambar/JS - tanpa baris ini, berkas di `static/` tidak akan bisa diakses lewat URL `/static/...`.

Struktur folder kamu sekarang:

```
myportofolio/
├── env/
├── manage.py
├── templates/
├── static/
│   ├── css/
│   └── img/
└── portofolio/
    ├── settings.py       # sudah ditambah TEMPLATES.DIRS & STATICFILES_DIRS
    ├── urls.py           # sudah ditambah routing ke landing_page
    ├── views.py          # baru dibuat
    └── ...
```

Penting

Ingat baik-baik langkah wiring views/urls/templates/static di atas - polanya persis sama yang bakal kamu pakai ulang di SETIAP tutorial berikutnya. Dan `myportofolio` ini bukan proyek latihan yang dibuang setelah tutorial selesai - ini website portofolio pribadimu yang beneran, terus berkembang sepanjang semester.

## Struktur Halaman dengan HTML5 [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#struktur-halaman-dengan-html5)

Sekarang kita bangun halaman utama: sebuah section “About Me” yang menampilkan foto, nama, dan bio singkat. Contoh di bawah pakai data Burhan - buat berkas `templates/index.html` persis seperti ini dulu, jalankan, baru nanti kamu ganti bagian yang ditandai dengan data kamu sendiri.

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Burhan - Portfolio</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="#profile" class="brand">Burhan</a>
            <nav>
                <a href="#profile">Profile</a>
            </nav>
        </div>
    </header>

    <main>
        <section class="hero" id="profile">
            <div class="container hero-grid">
                <div class="hero-identity">
                    <p class="hero-kicker">Computer Science &middot; Universitas Indonesia</p>
                    <h1>Burhan</h1>
                </div>
                <div class="hero-photo">
                    <div class="photo-block"></div>
                    <img class="avatar" src="/static/img/burhan.png" alt="Photo of Burhan">
                </div>
                <div class="hero-details">
                    <p class="bio">CS student at Universitas Indonesia for longer than planned, now a familiar (and slightly dreaded) face among Fasilkom students as a teaching assistant across several courses.</p>
                    <dl class="meta-list">
                        <div class="meta-row">
                            <dt>NPM</dt>
                            <dd>2206000000</dd>
                        </div>
                        <div class="meta-row">
                            <dt>Program</dt>
                            <dd>S1 Ilmu Komputer</dd>
                        </div>
                    </dl>
                    <div class="social-links">
                        <a href="https://github.com/" class="social-link">GitHub</a>
                        <a href="https://linkedin.com/" class="social-link">LinkedIn</a>
                        <a href="mailto:burhan@example.com" class="social-link">Email</a>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2026 Burhan. Fakultas Ilmu Komputer, Universitas Indonesia.</p>
        </div>
    </footer>
</body>
</html>
```

Penting

**Bagian yang harus kamu ganti dengan data sendiri:**

| `<title>` | `Burhan - Portfolio` | `<Nama Kamu> - Portfolio` |
| `.brand` (header) | `Burhan` | Nama kamu |
| `.hero-kicker` | `Computer Science · Universitas Indonesia` | Program studi & universitasmu |
| `<h1>` | `Burhan` | Nama lengkap kamu |
| `.bio` | bio contoh Burhan | 2-3 kalimat tentang dirimu sendiri |
| Baris NPM (`.meta-list`) | `2206000000` | NPM asli kamu |
| Baris Program (`.meta-list`) | `S1 Ilmu Komputer` | Program studimu |
| Link GitHub/LinkedIn | `https://github.com/`, `https://linkedin.com/` | tautan profil kamu yang sebenarnya |
| Email | `burhan@example.com` | email kamu |
| `src` avatar | `/static/img/burhan.png` | nama berkas foto kamu sendiri di `static/img/` |
| `alt` avatar | `Photo of Burhan` | `Photo of <Nama Kamu>` |
| Footer | `Burhan` | Nama kamu |

Jangan lupa taruh foto kamu sendiri (format `.jpg` atau `.png`) di folder `static/img/`.

Catatan

Perhatikan elemen semantik HTML5 yang dipakai: `<header>` untuk kop halaman, `<nav>` untuk navigasi, `<main>` untuk konten utama, `<section>` untuk satu bagian konten yang berdiri sendiri, dan `<footer>` untuk kaki halaman. Elemen-elemen ini tidak mengubah tampilan secara otomatis, tapi memberi _makna_ pada struktur halamanmu - lebih baik untuk aksesibilitas (mis. pembaca layar tahu mana bagian navigasi vs. konten utama) dan SEO dibanding menumpuk `<div>` di mana-mana. `<dl>`/`<dt>`/`<dd>` (dipakai untuk NPM dan Program di atas) khusus untuk pasangan label-nilai seperti ini - lebih tepat secara semantik dibanding sekadar `<div>` atau `<span>` biasa. Atribut `alt` pada `<img>` juga penting untuk aksesibilitas - selalu isi dengan deskripsi gambar, jangan dikosongkan.

Struktur folder kamu sekarang:

```
templates/
└── index.html         # baru dibuat, section "About Me"
```

## Mempercantik Halaman dengan CSS3 [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#mempercantik-halaman-dengan-css3)

Buat berkas `static/css/style.css`. Kita bangun bertahap per bagian supaya lebih mudah dipahami - tapi hasil akhirnya harus jadi satu berkas `style.css` yang utuh, gabungan dari semua potongan kode di bawah, sesuai urutannya.

Tip

Desain visual di tutorial ini (warna, font, tata letak, dsb.) cuma salah satu contoh untuk mendemonstrasikan teknik HTML5 dan CSS3 - kamu **tidak wajib** meniru tampilannya persis. Selama halamanmu tetap memakai HTML5 dan CSS3 murni (belum database/MVT) dan strukturnya rapi, kamu bebas berkreasi dengan skema warna, font, atau tata letak versimu sendiri, baik di tutorial ini maupun nanti di Individual Assignment 1.

### Reset Dasar & Custom Properties [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#reset-dasar-custom-properties)

```
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --ink: #1c1917;
    --paper: #faf6f0;
    --accent: #d95d39;
    --accent-dark: #a8442a;
    --line: #e3d9c9;
    --text-muted: #6b6459;
    --radius: 4px;
}

body {
    font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: var(--ink);
    background-color: var(--paper);
    line-height: 1.6;
}

h1, .brand {
    font-family: "Space Grotesk", -apple-system, sans-serif;
}

.container {
    max-width: 960px;
    margin: 0 auto;
    padding: 0 1.5rem;
}
```

`* { margin: 0; padding: 0; box-sizing: border-box; }` adalah _reset_ dasar - browser punya `margin`/`padding` bawaan yang beda-beda untuk tiap elemen, jadi kita nolkan dulu supaya kita yang mengatur semuanya dari nol. `box-sizing: border-box` membuat `padding` dan `border` dihitung _di dalam_ lebar elemen (bukan menambah lebar), lebih intuitif saat mengatur layout.

CSS _custom properties_ (variabel yang ditulis `--nama-variabel`) memudahkan kamu mengganti satu warna aksen di satu tempat (`:root`) dan otomatis berlaku di seluruh halaman lewat `var(--accent)`. Kalau nanti kamu mau ganti warna tema portofoliomu, cukup ubah nilai di `:root`, tidak perlu cari-cari satu per satu di seluruh berkas. Contoh di atas pakai palet warm cream (`--paper`) dan terracotta (`--accent`) \- sengaja bukan biru korporat standar, supaya terlihat lebih personal dan bukan template generik.

`h1, .brand { font-family: "Space Grotesk", ... }` mengganti _hanya_ judul dan logo ke _Space Grotesk_, sebuah _display font_ dari Google Fonts (link-nya ditambahkan di `<head>` pada bagian HTML) - teks body tetap pakai _system font_ untuk keterbacaan. Kombinasi _display font_ yang berbeda dari _body font_ ini yang bikin tipografi halaman terasa lebih dirancang, bukan cuma huruf bawaan browser di semua tempat.

`.container` dipakai berulang di banyak section untuk membatasi lebar maksimum konten (`max-width: 960px`) dan menengahkannya (`margin: 0 auto`), supaya teks tidak melebar penuh mengikuti layar lebar.

### Header dengan Flexbox [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#header-dengan-flexbox)

```
.site-header {
    border-bottom: 1px solid var(--line);
}

.site-header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
}

.brand {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--ink);
    text-decoration: none;
}

.site-header nav {
    display: flex;
    gap: 2rem;
}

.site-header nav a {
    color: var(--ink);
    text-decoration: none;
    font-size: 0.95rem;
}
```

`display: flex` membuat elemen `.brand` dan `<nav>` di dalamnya sejajar secara horizontal secara otomatis. `justify-content: space-between` mendorong keduanya ke ujung kiri dan kanan, `align-items: center` menengahkan secara vertikal. `gap: 2rem` memberi jarak antar link navigasi tanpa perlu `margin` manual di tiap link.

`.brand` di sini sengaja dibiarkan sebagai teks polos - namamu sendiri, di- _style_ dengan `font-family` Space Grotesk yang sudah kita atur lewat `h1, .brand` sebelumnya, plus `text-decoration: none` supaya tidak digarisbawahi seperti link biasa. Tidak perlu logo lingkaran atau ikon buatan - teks nama dengan tipografi yang sedikit lebih tegas sudah cukup untuk jadi identitas header, dan jauh lebih mudah kamu tiru dan sesuaikan sendiri.

### Section Hero dengan CSS Grid [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#section-hero-dengan-css-grid)

```
.hero {
    padding: 4.5rem 0 5rem;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.3fr 1fr;
    grid-template-areas:
        "identity photo"
        "details  photo";
    gap: 1.5rem 3rem;
}

.hero-identity {
    grid-area: identity;
}

.hero-details {
    grid-area: details;
}

.hero-kicker {
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent-dark);
    font-weight: 700;
    margin-bottom: 0.75rem;
}

.hero-identity h1 {
    font-size: clamp(3rem, 7vw, 5rem);
    line-height: 0.95;
}

.bio {
    color: var(--text-muted);
    max-width: 480px;
    margin-bottom: 1.5rem;
}

.meta-list {
    display: flex;
    gap: 2rem;
    margin-bottom: 1.5rem;
}

.meta-row dt {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-bottom: 0.15rem;
}

.meta-row dd {
    font-weight: 600;
}

.social-links {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.social-link {
    display: inline-block;
    font-size: 0.85rem;
    font-weight: 600;
    text-decoration: none;
    color: var(--paper);
    background-color: var(--ink);
    border-radius: var(--radius);
    padding: 0.5rem 1.1rem;
    transition: background-color 0.2s ease;
}

.social-link:hover {
    background-color: var(--accent);
}

.hero-photo {
    grid-area: photo;
    align-self: center;
    position: relative;
}

.photo-block {
    position: absolute;
    top: 1.25rem;
    left: 1.25rem;
    width: 100%;
    height: 100%;
    background-color: var(--accent);
    border-radius: var(--radius);
    z-index: 0;
}

.avatar {
    position: relative;
    z-index: 1;
    display: block;
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: cover;
    border-radius: var(--radius);
    border: 3px solid var(--ink);
}
```

`grid-template-columns: 1.3fr 1fr` membuat kolom teks sedikit lebih lebar dibanding kolom foto (1.3 bagian berbanding 1 bagian) - layout asimetris seperti ini terasa lebih dirancang dibanding kolom yang sama rata atau selebar-konten-saja. `grid-template-areas` memberi nama pada tiap area grid (`identity`, `photo`, `details`) lalu menyusunnya lewat “peta” berbentuk teks - `.hero-photo` muncul di kedua baris pada kolom yang sama, sehingga otomatis menyatu jadi satu area yang membentang dua baris. Elemen anak lalu menempel ke areanya masing-masing lewat `grid-area: nama-area`, tanpa perlu diurutkan manual di HTML. `clamp(3rem, 7vw, 5rem)` pada `.hero-identity h1` membuat judul sangat besar dan otomatis menyesuaikan lebar layar (nilai tengah `7vw`), dibatasi minimum `3rem` dan maksimum `5rem` \- tipografi besar seperti ini yang bikin halaman terasa punya _statement_, bukan sekadar judul kecil di pojok.

Bagian paling menarik ada di `.hero-photo`: `.photo-block` adalah `<div>` kosong yang diposisikan `absolute` sedikit _offset_ (bergeser `1.25rem` ke kanan-bawah) dari foto aslinya, dengan warna solid `var(--accent)` sebagai latar. `.avatar` diposisikan `relative` dengan `z-index: 1` (di atas `.photo-block` yang `z-index: 0`) sehingga terlihat seperti foto punya “bayangan” berwarna solid di belakangnya - efek _layered_ ini yang menggantikan `box-shadow` sederhana dan terasa lebih personal/craft dibanding foto bulat polos.

`aspect-ratio: 1 / 1` pada `.avatar` memaksa foto selalu persegi berapapun ukuran aslinya (mirip `object-fit: cover` yang sudah dipakai untuk memastikan foto tidak gepeng/melar), tanpa perlu tahu tinggi pastinya di CSS.

`.meta-list` memakai `display: flex` sederhana untuk menjajarkan pasangan NPM/Program secara horizontal - lebih ringkas dibanding badge berbentuk pil yang butuh border dan border-radius terpisah untuk tiap potongan info.

`transition: background-color 0.2s ease` pada `.social-link` membuat perubahan warna saat _hover_ terjadi secara halus (0.2 detik), bukan berubah instan.

### Footer & Responsive [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#footer-responsive)

```
.site-footer {
    padding: 1.5rem;
    color: var(--text-muted);
    font-size: 0.85rem;
    border-top: 1px solid var(--line);
}

@media (max-width: 600px) {
    .hero-grid {
        grid-template-columns: 1fr;
        grid-template-areas:
            "identity"
            "photo"
            "details";
    }

    .hero-photo {
        max-width: 220px;
    }

    .social-links {
        justify-content: flex-start;
    }
}
```

Footer sengaja dibiarkan rata kiri (bukan `text-align: center`) dan isinya cuma satu baris teks hak cipta sederhana - footer yang isinya cuma nama dan NPM lagi (yang sudah ada di bagian hero) mudah terasa seperti tempelan generik, jadi lebih wajar diisi baris singkat semacam `&copy; 2026 <Nama Kamu>. <Nama Universitasmu>.`, mirip footer situs pada umumnya.

Perhatikan `.hero-grid` di dalam media query mendefinisikan ulang `grid-template-areas` dengan urutan `identity`, lalu `photo`, lalu `details` \- ini yang membuat di layar sempit, nama tampil dulu, disusul foto, baru bio dan kontak di bawahnya, bukan sekadar menumpuk urutan HTML apa adanya. Karena letak tiap elemen ditentukan oleh nama area (bukan urutan dokumen), kamu bisa mengatur urutan tampilan mobile berbeda dari urutan HTML tanpa menulis ulang markup-nya sama sekali.

`@media (max-width: 600px)` adalah _media query_ \- aturan CSS di dalamnya HANYA berlaku kalau lebar layar 600px atau kurang (misalnya HP). Di sini kita ubah grid dua kolom (`1.3fr 1fr`) menjadi satu kolom (`1fr` saja) supaya foto ada di atas dan teks di bawah - berbeda dari pendekatan umum yang menengahkan semuanya (`text-align: center`), di sini teks tetap rata kiri (`text-align: left`) supaya paragraf bio tetap nyaman dibaca, dan `.hero-photo` dibatasi lebarnya (`max-width: 220px`) supaya foto besarnya tidak berubah jadi berlebihan di layar sempit. Ini yang disebut _responsive design_, tampilan yang menyesuaikan diri ke berbagai ukuran layar.

Struktur folder kamu sekarang (lengkap sampai akhir Tutorial 01):

```
myportofolio/
├── env/
├── .git/
├── .gitignore
├── requirements.txt
├── db.sqlite3
├── manage.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
│       └── burhan.png       # ganti dengan foto kamu sendiri
└── portofolio/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    ├── views.py
    └── wsgi.py
```

## Menjalankan dan Melihat Hasil [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#menjalankan-dan-melihat-hasil)

Jalankan server-nya lagi kalau belum:

```
python manage.py runserver
```

Buka `http://localhost:8000/` \- halaman “About Me” kamu seharusnya sudah tampil. Berikut contoh hasilnya memakai data Burhan di atas:

![](https://pbp.cs.ui.ac.id/img/tutorial-1/hasil-akhir.png)

Hasil akhir Tutorial 01 di tampilan desktop

Pastikan juga tampilannya tidak rusak di layar sempit - coba perkecil lebar browser atau buka lewat DevTools mode responsif:

![](https://pbp.cs.ui.ac.id/img/tutorial-1/hasil-akhir-mobile.png)

Hasil akhir Tutorial 01 di tampilan mobile

Penting

Sebelum lanjut: halaman yang barusan kamu bikin itu bukan contoh latihan, ini halaman utama portofolio pribadimu yang sebenarnya. Ganti semua data contoh Burhan (nama, NPM, foto, bio, link sosial) pakai punya kamu sendiri sesuai tabel di atas - struktur HTML/CSS yang sama ini yang bakal terus kamu kembangkan, dan jadi titik awal untuk **Individual Assignment 1** minggu ini.

## Pembuatan Akun dan Deployment melalui PWS (Pacil Web Service) [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#pembuatan-akun-dan-deployment-melalui-pws-pacil-web-service)

Sekarang halaman “About Me” kamu sudah berjalan di lokal. Langkah terakhir adalah men- _deploy_-nya supaya bisa diakses lewat internet, memakai **PWS (Pacil Web Service)** \- platform _hosting_ milik Fakultas Ilmu Komputer UI.

01. Akses halaman PWS pada [https://pws.cs.ui.ac.id](https://pws.cs.ui.ac.id/). Kamu akan diarahkan ke halaman _login_ with SSO.

02. Login dengan akun SSO UI kamu.

03. Apabila proses _login_ berhasil, kamu akan diarahkan ke _home page_ dari PWS.



    ![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-home.png)

    Home page PWS

04. Buat proyek baru dengan menekan tombol **Create New Project**. Pada halaman berikutnya, isi `Project Name` dengan `myportofolio`, lalu tekan **Create New Project** di bawahnya.



    ![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-create-project.png)

    Halaman Create Project PWS










    Catatan








    Dalam membuat proyek lain nantinya (seperti Individual Assignment atau Tugas Kelompok), kamu bisa mengisi `Project Name` dengan nama lain sesukamu. Ada limitasi bahwa nama proyek harus terdiri dari karakter _alphanumeric_ saja.

05. Akan muncul dua informasi baru: **Project Credentials** dan **Project Command**. Simpan _credentials_ yang kamu peroleh di tempat yang aman, karena kamu **tidak akan bisa melihatnya lagi** setelah ini. Jangan jalankan dulu instruksi _Project Command_-nya.



    ![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-credentials.png)

    Halaman Project Credentials dan Project Command

06. Pada _sidebar_, klik proyek yang kamu buat, lalu pilih tab **Environs**.



    ![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-environs-tab.png)

    Tab Environs pada proyek PWS

    Pada tab tersebut, klik **Raw Editor** dan _copy-paste_ isi berkas `.env.prod` yang sudah kamu buat di Tutorial 0. Pastikan `SCHEMA=tutorial` dan `PRODUCTION=True`, lalu klik **Update All Variables**.



    ![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-raw-editor.png)

    Raw Editor untuk environment variables

    Pastikan _environment variable_ di proyek PWS kamu sudah tersimpan dengan baik.



    ![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-env-saved.png)

    Konfirmasi environment variables tersimpan

07. Pada `settings.py` di proyek Django kamu, tambahkan URL _deployment_ PWS ke `ALLOWED_HOSTS`.










    Catatan








    URL _deployment_ PWS memiliki format `<username-sso>-<nama-proyek>.pws.cs.ui.ac.id`. Kalau username SSO kamu ada karakter titik (`.`), ganti jadi _hyphen_ (`-`). Contoh: kalau username SSO kamu `burhan.25` dan nama proyek `myportofolio`, URL _deployment_-nya `burhan-25-myportofolio.pws.cs.ui.ac.id`.









    ```
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "<URL deployment PWS kamu>"]
    ```













    PentingAktifkan Static Files untuk Produksi








    Server produksi (`gunicorn`) tidak otomatis melayani berkas _static_ seperti `python manage.py runserver` di lokal - tanpa langkah ini, CSS dan gambarmu akan 404 setelah di- _deploy_. Tambahkan `'whitenoise.middleware.WhiteNoiseMiddleware'` ke `MIDDLEWARE` di `settings.py`, tepat di bawah `SecurityMiddleware` (paket `whitenoise` sudah ada di `requirements.txt` kamu sejak Tutorial 0):







    ```
    MIDDLEWARE = [\
        'django.middleware.security.SecurityMiddleware',\
        'whitenoise.middleware.WhiteNoiseMiddleware',\
        # baris MIDDLEWARE lain di bawahnya tetap sama\
        ...\
    ]
    ```







    Lalu tambahkan `STATIC_ROOT` dan `WHITENOISE_USE_FINDERS` di bagian `STATIC_URL`/`STATICFILES_DIRS` yang sudah kamu buat sebelumnya:







    ```
    STATIC_URL = 'static/'
    STATICFILES_DIRS = [BASE_DIR / 'static']
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    WHITENOISE_USE_FINDERS = True
    ```









    Lakukan `git add`, `commit`, dan `push` perubahan ini ke repositori GitHub kamu.










    Peringatan








    Sebelum lanjut ke langkah berikutnya, pastikan struktur repositorimu lengkap: berkas `manage.py`, `requirements.txt`, `.gitignore`, direktori `portofolio/` (folder konfigurasi proyek), dan **bukan** direktori `env/` atau berkas `db.sqlite3` (harusnya sudah di- _gitignore_).





    ![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-repo-structure.png)

    Contoh struktur repositori yang benar

08. Jalankan perintah yang ada pada informasi _Project Command_ di halaman PWS. Saat push ke PWS, akan muncul _window_ yang meminta `username` dan `password` \- gunakan _credentials_ dari proyek PWS-mu ( **bukan** _credentials_ SSO).



    ![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-push-auth.png)

    Autentikasi saat push ke PWS

09. Pada _sidebar_ PWS, klik proyek yang kamu buat untuk melihat status _deployment_. Kalau statusnya `Building`, proyekmu masih diproses. Kalau sudah `Running`, proyekmu sudah bisa diakses - tekan tombol **View Project**.



    ![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-status.png)

    Status deployment proyek PWS

10. Kalau nanti ada perubahan pada proyek Django yang mau kamu push ke PWS lagi, kamu cukup jalankan (setelah `add` dan `commit`):





    ```
    git push pws master
    ```





    Kamu tidak perlu mengulang instruksi _Project Command_ lagi.


Penting

Proyek `myportofolio` yang kamu _deploy_ ini akan menjadi landasan untuk tutorial-tutorial berikutnya - repositori dan _deployment_-nya akan terus berkembang seiring tutorial yang kamu ikuti sepanjang semester.

### Troubleshooting PWS [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#troubleshooting-pws)

**Build Gagal**

Kalau _build_ gagal, coba periksa beberapa hal berikut:

- **Isi Repositori**: pastikan struktur repositorimu sama seperti contoh di Langkah 7 di atas.

- **Berkas `requirements.txt`**: pastikan namanya persis, bukan `requirement.txt` (kurang huruf “s”) atau `requirements.txt.txt` (ekstensi ganda).

- **Berkas `.gitignore`**: pastikan diawali titik, tidak punya ekstensi tambahan, dan berada di _root folder_ bersama `manage.py`, direktori `portofolio/`, `requirements.txt`, `.git`, dan `db.sqlite3`.










Tip








Pengguna Windows bisa centang opsi **File name extensions** di Windows Explorer untuk melihat ekstensi berkas dengan lebih jelas.





![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-file-extensions.png)

Opsi menampilkan ekstensi berkas di Windows

- Pastikan direktori `env/` dan `db.sqlite3` **tidak** ikut ter- _push_ oleh Git. Kalau sudah telanjur, tambahkan `.gitignore` lalu jalankan `git rm --cached -r env db.sqlite3` sebelum `add`, `commit`, `push` lagi.

- Kalau struktur sudah yakin lengkap tapi tetap gagal, pastikan kamu push ke PWS menggunakan _branch_`master`.


**Tidak Menyimpan Credentials**

Kalau kamu lupa menyimpan _credentials_ saat membuat proyek PWS, kamu bisa me- _regenerate_-nya lewat tab **Settings** di proyek tersebut.

![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-regenerate-credential.png)

Regenerate credential di tab Settings

Ikuti langkah-langkah pada tab tersebut, atau alternatifnya buat proyek baru.

**Mengganti Remote URL PWS pada Repositori Lokal**

Kalau kamu membuat proyek baru di PWS untuk mengatasi masalah proyek sebelumnya, ganti _remote_ URL di repositori lokalmu supaya `git push pws master` mengarah ke proyek yang baru, bukan yang lama:

```
git remote set-url pws <link-proyek-baru>
```

**Error 502 (Bad Gateway) pada Web**

Saat _deployment_ pertama kali, kamu mungkin melihat error 502 (Bad Gateway) di _browser_. Ini normal - PWS sedang menjalankan migrasi database sebelum _server_ aplikasi (gunicorn) siap menerima _request_.

![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-502-error.png)

Error 502 Bad Gateway

Kamu bisa cek progresnya di tab **Logs** pada dashboard proyek PWS. Tunggu sampai muncul log `Listening at` (biasanya 15-20 detik) - _refresh_ halaman _log_ kalau perlu, karena tidak update secara _streaming_.

![](https://pbp.cs.ui.ac.id/img/tutorial-1/pws-logs.png)

Tab Logs pada dashboard PWS

## Pengumpulan [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#pengumpulan)

Tutorial ini tidak punya slot submisi terpisah di SCELE dan tidak dinilai secara langsung - tapi karena statusnya sebagai prasyarat wajib Individual Assignment 1, pastikan seluruh perubahan tutorial ini sudah di- _commit_ dan di- _push_ ke repositori GitHub kamu **paling lambat Rabu, 2 September 2026**. Commit yang baru di- _push_ setelah tenggat waktu itu dianggap Tutorial 01 belum selesai, sehingga Individual Assignment 1 tidak akan dinilai. Pastikan juga repositori GitHub kamu bersifat **publik**, supaya asisten dosen bisa mengaksesnya.

## Referensi Tambahan [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html\#referensi-tambahan)

- [MDN - HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
- [MDN - CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout)
- [Django - Templates](https://docs.djangoproject.com/en/4.2/topics/templates/)