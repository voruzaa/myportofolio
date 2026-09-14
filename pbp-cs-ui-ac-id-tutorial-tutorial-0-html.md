# Tutorial 0: Setup Git Repository, Django Installation

Pemrograman Berbasis Platform (CSGE602022) - diselenggarakan oleh Fakultas Ilmu Komputer Universitas Indonesia, Semester Gasal 2026/2027

**Kontributor:** MUH - Hafiz

* * *

### Tujuan Pembelajaran [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#tujuan-pembelajaran)

Setelah menyelesaikan tutorial ini, mahasiswa diharapkan untuk dapat:

- Mengerti perintah-perintah dasar Git yang perlu diketahui untuk mengerjakan proyek aplikasi.
- Membuat repositori Git lokal dan daring (GitHub), lalu menghubungkan keduanya.
- Memahami _branching_ pada Git dan mampu melakukan _pull request_/ _merge_.
- Menginstall Django dan membuat proyek Django pertamamu.

Tip

Tutorial ini adalah tutorial pertama dari proyek yang akan kamu bangun berkelanjutan sepanjang semester: sebuah **website portofolio pribadi**. Pastikan langkah-langkah di bawah selesai sebelum Tutorial 01 minggu depan, karena Tutorial 01 melanjutkan langsung dari proyek Django yang kamu buat di sini.

## Pembuatan Akun GitHub (Lewati Jika Sudah Ada) [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#pembuatan-akun-github-lewati-jika-sudah-ada)

### Pengenalan Git dan GitHub [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#pengenalan-git-dan-github)

Pengenalan awal ini akan membantumu memahami dasar-dasar Git dan platform _git hosting_ berbasis web yang dikenal sebagai GitHub.

**Git: Sistem Kontrol Versi untuk Codebase**

- **Git** adalah sistem kontrol versi yang membantumu melacak perubahan pada kode sumber proyek.
- Dengan Git, kamu dapat memantau semua revisi yang telah dilakukan pada proyekmu seiring waktu.

**GitHub: Platform Kolaborasi Menggunakan Git**

- **GitHub** adalah platform berbasis web yang memungkinkanmu menyimpan, mengelola, dan berkolaborasi pada proyek menggunakan Git.
- Ini memberikan wadah yang aman untuk meng- _host_ proyekmu dan berinteraksi dengan rekan tim melalui Git.

**Mengapa Penting?**

- Git dan GitHub memainkan peran penting dalam pengembangan perangkat lunak modern dan kolaborasi tim.
- Keduanya memungkinkan tim untuk melacak perubahan kode, menyimpan versi, dan bekerja bersama dalam proyek secara efisien.

### Langkah 1: Membuat Akun di GitHub [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-1-membuat-akun-di-github)

1. Buka [GitHub](https://github.com/) di peramban web.
2. Cari tombol **Sign up** di pojok kanan atas, lalu klik.
3. Isi formulir pendaftaran (nama pengguna, email, kata sandi).
4. Verifikasi akunmu lewat email yang dikirimkan GitHub.
5. Akun GitHub kamu siap digunakan.

![](https://pbp.cs.ui.ac.id/img/tutorial-0/github-account.png)

Contoh akun GitHub

Selamat, kamu telah membuat akun GitHub yang dapat digunakan untuk menyimpan proyek, berkolaborasi dengan orang lain, dan masih banyak lagi.

## Instalasi IDE [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#instalasi-ide)

_IDE_ ( _Integrated Development Environment_) adalah perangkat lunak yang membantu menulis, mengedit, dan mengelola kode.

### Langkah 1: Pilih Text Editor atau IDE [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-1-pilih-text-editor-atau-ide)

Beberapa pilihan populer:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Sublime Text](https://www.sublimetext.com/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Neovim](https://neovim.io/)

### Langkah 2: Proses Instalasi [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-2-proses-instalasi)

1. Buka situs resmi IDE pilihanmu.
2. Ikuti petunjuk yang diberikan untuk mengunduh _installer_-nya.
3. Jalankan _installer_ dan ikuti instruksi di layar untuk menyelesaikan proses instalasi.

### Langkah 3: Mulai Menggunakan IDE [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-3-mulai-menggunakan-ide)

1. Setelah instalasi selesai, buka IDE yang sudah terinstall.
2. Eksplorasi antarmuka dan fitur yang disediakan untuk membantumu dalam pengembangan proyek.

![](https://pbp.cs.ui.ac.id/img/tutorial-0/ide-installed.png)

Contoh tampilan IDE setelah terinstall

## Instalasi dan Konfigurasi Git [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#instalasi-dan-konfigurasi-git)

### Langkah 1: Instalasi Git [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-1-instalasi-git)

1. Buka [situs resmi Git](https://git-scm.com/downloads).
2. Pilih sistem operasimu (Windows, macOS, atau Linux), unduh _installer_-nya.
3. Jalankan _installer_ dan ikuti instruksi di layar. Untuk pengguna Windows, centang opsi “Git Credential Manager Core” supaya integrasi dengan GitHub lebih mudah.

### Langkah 2: Konfigurasi Nama Pengguna dan Email [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-2-konfigurasi-nama-pengguna-dan-email)

Sebelum mulai berkontribusi ke repositori, konfigurasikan nama pengguna dan alamat email agar terhubung dengan _commit_-mu. Atur _username_ dan _email_ yang akan diasosiasikan dengan pekerjaanmu, sesuaikan dengan akun [GitHub](https://github.com/) yang kamu pakai.

```
git config --global user.name "<NAMA>"
git config --global user.email "<EMAIL>"
```

Contoh:

```
git config --global user.name "Burhan"
git config --global user.email "burhan@example.com"
```

Perlu diketahui bahwa _flag_`--global` akan mengubah konfigurasi global untuk seluruh sistem. Yang dimaksud konfigurasi global adalah kamu sedang bilang ke Git: “Kalau aku pakai Git di komputer ini, anggap saja namaku dan emailku selalu ini.” Jadi, `--global` berlaku untuk semua proyek Git yang kamu buka di komputer itu.

Peringatan

Kalau kamu **hanya butuh konfigurasi internal** (khusus satu proyek saja), kamu cukup menjalankan perintah yang sama tanpa `--global`, di dalam folder proyek tersebut:

```
git config user.name "<NAMA>"
git config user.email "<EMAIL>"
```

Contoh:

```
git config user.name "Burhan"
git config user.email "burhan@example.com"
```

Konfigurasi internal (nama dan email yang kamu gunakan untuk _login_) hanya berlaku untuk proyek Git yang sedang kamu buka - jadi cuma untuk folder Git yang sedang aktif.

### Langkah 3: Konfigurasi Autentikasi [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-3-konfigurasi-autentikasi)

**Windows:**

```
git credential-manager configure
git config --global credential.credentialStore wincredman
```

**Unix (macOS, Linux):**

```
git credential-manager configure
git config --global credential.credentialStore keychain
```

Tip

Kalau perintah `git credential-manager` tidak dikenali, coba `git-credential-manager` atau `git-credential-manager-core`. Di macOS, kamu bisa install lewat Homebrew: `brew install git-credential-manager-core`.

### Langkah 4: Verifikasi Konfigurasi [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-4-verifikasi-konfigurasi)

```
git config --list
```

![](https://pbp.cs.ui.ac.id/img/tutorial-0/git-config-list.png)

Contoh output git config –list

## Menyiapkan Repository myportofolio [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#menyiapkan-repository-myportofolio)

**Repositori** adalah tempat penyimpanan untuk proyek perangkat lunak, yang mencakup semua revisi dan perubahan yang telah dilakukan pada kode. Untuk mengeksekusi perintah-perintah Git, kamu bisa melakukannya pada repositori di GitHub, platform kolaboratif untuk mengelola proyek menggunakan Git.

### Langkah 1: Inisiasi Repositori Lokal [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-1-inisiasi-repositori-lokal)

1. Buat folder proyek baru dan masuk ke dalamnya.





```
mkdir myportofolio && cd myportofolio
```

2. Inisiasi repositori Git.





```
git init
```

3. Buat berkas `README.md` berisi identitasmu.





```
Nama : Burhan

NPM : 2206000000

Kelas : PBP A
```

4. Cek status repositori, lalu tandai `README.md` sebagai berkas yang akan di- _commit_.





```
git status
git add README.md
```

5. Jalankan `git status` sekali lagi untuk memastikan `README.md` sudah ditandai untuk di- _commit_, lalu commit dengan pesan yang sesuai.





```
git status
git commit -m "Add README.md"
```


Catatan

Kebiasaan baik menulis pesan _commit_: jelaskan singkat apa yang kamu lakukan, biasanya dalam bahasa Inggris (mis. `Add README.md`), hindari pesan umum seperti `update file`.

### Langkah 2: Menghubungkan ke Repositori GitHub [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-2-menghubungkan-ke-repositori-github)

1. Buat _branch_ utama bernama `main`.





```
git branch -M main
```

2. Buka [GitHub](https://github.com/), klik tombol **+** di pojok kanan atas lalu pilih **New repository**. Isi `Repository name` dengan `myportofolio`, pilih visibilitas **Public**, biarkan opsi lain (README, .gitignore, license) tetap kosong/default, lalu klik **Create repository**.



![](https://pbp.cs.ui.ac.id/img/tutorial-0/github-create-repo.png)

Halaman pembuatan repositori baru di GitHub

3. Hubungkan repositori lokal ke repositori GitHub yang baru dibuat dengan perintah `git remote add <NAMA_REMOTE> <URL_REPO>`.





```
git remote add origin https://github.com/<username>/myportofolio.git
```





`<NAMA_REMOTE>` adalah nama yang akan kamu gunakan untuk mereferensikan repositori remote tersebut - secara konvensi, nama **origin** dipakai untuk repositori utama/primer. `<URL_REPO>` adalah URL HTTPS repositori yang kamu dapat dari halaman GitHub setelah repositorinya dibuat.










Tip








Beberapa perintah tambahan yang berguna seputar _remote_:



   - Melihat daftar remote yang sudah ditambahkan: `git remote -v`
   - Menghapus remote: `git remote remove <NAMA_REMOTE>`
   - Mengganti URL remote: `git remote set-url <NAMA_REMOTE> <URL_BARU>`

4. Push ke GitHub untuk pertama kalinya.





```
git push -u origin main
```





Perintah ini mengirimkan semua perubahan yang ada pada _branch_ saat ini (`main`) di repositori lokal ke _branch_`main` di repositori GitHub. Kalau ini pertama kalinya kamu push dari komputer ini, biasanya akan muncul jendela yang minta kamu _sign in_ ke GitHub lewat _browser_ \- ikuti saja instruksinya.

5. _Refresh_ halaman repositorimu di GitHub - `README.md` seharusnya sudah terlihat.


![](https://pbp.cs.ui.ac.id/img/tutorial-0/github-repo-created.png)

Repositori myportofolio di GitHub setelah push pertama

### Langkah 3: Melakukan Cloning terhadap Suatu Repositori [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-3-melakukan-cloning-terhadap-suatu-repositori)

**_Cloning_ repositori** adalah proses menduplikasi seluruh konten dari repositori yang ada di GitHub ke komputer lokal, supaya bisa dilihat, diedit, dan dijalankan secara _offline_.

1. Buka halaman repositori `myportofolio` yang sudah kamu buat di [GitHub](https://github.com/).

2. Klik tombol **Code** di pojok kanan atas halaman repositori, lalu pilih opsi HTTPS untuk salin URL _clone_-nya.

3. Buka terminal di direktori yang **berbeda** dari tempat repositori lokalmu sebelumnya, lalu jalankan:





```
git clone <URL_CLONE>
```


Setelah ini kamu punya tiga repositori: repositori asli di komputer lokal, repositori daring di GitHub, dan repositori baru hasil _cloning_ yang terhubung ke repositori GitHub yang sama. Ini memungkinkanmu bekerja dengan repositori yang sama dari beberapa tempat/komputer dengan mudah.

### Langkah 4: Latihan Branching dan Pull Request [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-4-latihan-branching-dan-pull-request)

Pada tahap ini kamu akan mempelajari penggunaan _branch_ di Git. Penggunaan _branch_ memungkinkanmu mengembangkan fitur atau memperbaiki _bug_ di lingkungan terpisah sebelum menggabungkannya kembali ke _branch_ utama.

**Apa Itu Branch di Git?**

- _Branch_ di Git adalah cabang terpisah dari _source code_ yang memungkinkan pengembangan independen dari fitur atau perubahan.
- Hal ini memungkinkan kamu untuk bekerja pada fitur atau perbaikan _bug_ tanpa mengganggu kode yang ada di _branch_ utama (`main`).

1. Buat dan pindah ke _branch_ baru dengan perintah `git checkout -b <NAMA_BRANCH>`.





```
git checkout -b latihan-branch
```














Tip








Kalau kamu ingin berpindah ke _branch_ yang **sudah ada** (bukan membuat baru), jalankan `git checkout <NAMA_BRANCH>` saja tanpa flag `-b`. Flag `-b` khusus dipakai untuk membuat _branch_ baru sekaligus langsung berpindah ke sana.

2. Ubah sedikit isi `README.md`, lalu simpan, `add`, `commit`, dan push _branch_ tersebut.





```
git add README.md
git commit -m "Update README.md"
git push -u origin latihan-branch
```

3. Buka repositorimu di GitHub. Secara otomatis akan muncul _pop-up_ dengan tombol **Compare & pull request**. Kalau tidak muncul, alternatifnya tekan tombol **Pull Request**, lalu pilih **New pull request**. GitHub akan membandingkan perubahan di kedua _branch_ yang ingin digabungkan.

4. Apabila tidak ada konflik, klik **Merge pull request** untuk menggabungkan perubahan dari `latihan-branch` ke `main`.


Catatan

**Konflik** terjadi ketika perubahan pada satu _branch_ bertabrakan dengan perubahan di _branch_ lain - misalnya kalau dua bagian berbeda mengubah baris yang sama dalam waktu bersamaan, Git tidak bisa otomatis memutuskan perubahan mana yang harus dipakai. Kalau ini terjadi, GitHub akan minta kamu menentukan sendiri perubahan mana yang dipakai sebelum bisa merge - ini normal terjadi kalau kamu bekerja di banyak _branch_ sekaligus. Memahami konsep _branching_ ini penting karena memungkinkan pengembangan yang terorganisir dan terpisah, sebelum semua perubahan digabungkan kembali ke kode utama.

## Instalasi Django dan Inisiasi Proyek Django [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#instalasi-django-dan-inisiasi-proyek-django)

**Django** adalah kerangka kerja ( _framework_) yang populer untuk pengembangan aplikasi web dengan bahasa pemrograman Python. Di section ini kamu akan menginstall Django dan menginisiasi proyek portofoliomu.

### Langkah 1: Virtual Environment [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-1-virtual-environment)

Di dalam folder `myportofolio`, buat _virtual environment_.

**Windows:**

```
python -m venv env
```

**Unix (macOS, Linux):**

```
python3 -m venv env
```

_Virtual environment_ berguna untuk mengisolasi _package_ dan _dependencies_ aplikasi supaya tidak bertabrakan dengan versi lain di komputermu. Aktifkan dengan perintah berikut.

**Windows:**

```
env\Scripts\activate
```

**Unix (macOS, Linux):**

```
source env/bin/activate
```

Tip

Pengguna Windows yang mengalami error `PSSecurityException`, `UnauthorizedAccess`, atau “running scripts is disabled on this system” bisa mengatasinya dengan: buka PowerShell dengan akses _administrator_, jalankan `Set-ExecutionPolicy Unrestricted -Force`, lalu coba aktifkan _virtual environment_ lagi.

Kamu akan lihat `(env)` muncul di depan prompt terminal kalau berhasil.

### Langkah 2: Menyiapkan Dependencies dan Membuat Proyek Django [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-2-menyiapkan-dependencies-dan-membuat-proyek-django)

**Dependencies** adalah _library_/ _package_ yang dibutuhkan aplikasimu untuk berjalan. Buat berkas `requirements.txt` berisi daftar _dependencies_ berikut (tanpa perlu menentukan versi spesifik):

```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
python-dotenv
```

Install semua _dependencies_ tersebut:

```
pip install -r requirements.txt
```

Lalu buat proyek Django bernama `myportofolio`:

```
django-admin startproject myportofolio .
```

Penting

Pastikan karakter `.` tertulis di akhir perintah - ini membuat Django meletakkan `manage.py` langsung di folder `myportofolio`, bukan di dalam subfolder baru.

### Langkah 3: Konfigurasi Environment Variables [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-3-konfigurasi-environment-variables)

**Environment variables** adalah variabel yang disimpan di luar kode program, dipakai untuk menyimpan informasi konfigurasi (kredensial database, API key, dst) supaya kode yang sama bisa jalan di environment yang berbeda tanpa diubah.

1. Buat berkas `.env` di root proyek (sejajar dengan `manage.py`), isi dengan:


```
PRODUCTION=False
```

2. Buat juga berkas `.env.prod` di folder yang sama, untuk konfigurasi production nanti:


```
DB_NAME=<nama database>
DB_HOST=<host database>
DB_PORT=<port database>
DB_USER=<username database>
DB_PASSWORD=<password database>
SCHEMA=tutorial
PRODUCTION=True
```











Catatan








   - `.env`: dipakai untuk development lokal. Karena `PRODUCTION=False`, aplikasi memakai database SQLite yang sederhana untuk testing.
   - `.env.prod`: dipakai saat _deployment_ ke PWS di [Tutorial 01](https://pbp.cs.ui.ac.id/tutorial/tutorial-1.html). Karena `PRODUCTION=True`, aplikasi memakai database PostgreSQL dengan kredensial yang akan diberikan menyusul.
   - `SCHEMA`: nama schema database, disesuaikan lagi dengan kebutuhan tiap tutorial/tugas.

3. Tambahkan kode berikut di bagian atas `settings.py` (setelah import `Path`), lalu tambahkan konfigurasi `ALLOWED_HOSTS` dan `PRODUCTION`:





```
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
```









```
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
```









```
PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'
```

4. Cari bagian `DATABASES` di `settings.py`, ganti dengan konfigurasi yang otomatis memilih SQLite (development) atau PostgreSQL (production):





```
# Database configuration
if PRODUCTION:
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql',
               'NAME': os.getenv('DB_NAME'),
               'USER': os.getenv('DB_USER'),
               'PASSWORD': os.getenv('DB_PASSWORD'),
               'HOST': os.getenv('DB_HOST'),
               'PORT': os.getenv('DB_PORT'),
               'OPTIONS': {
                   'options': f"-c search_path={os.getenv('SCHEMA', 'public')}"
               }
           }
       }
else:
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.sqlite3',
               'NAME': BASE_DIR / 'db.sqlite3',
           }
       }
```


### Langkah 4: Menjalankan Server [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-4-menjalankan-server)

Jalankan migrasi database, lalu jalankan servernya.

```
python manage.py migrate
python manage.py runserver
```

Perintah `migrate` menerapkan migration bawaan Django untuk _app_ default (`admin`, `auth`, `contenttypes`, `sessions`). Buka `http://localhost:8000/` di browser - kamu akan melihat animasi roket bawaan Django sebagai tanda proyekmu berhasil dibuat.

![](https://pbp.cs.ui.ac.id/img/tutorial-0/django-rocket.png)

Halaman selamat datang Django (animasi roket)

### Langkah 5: Menghentikan Server dan Menonaktifkan Virtual Environment [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-5-menghentikan-server-dan-menonaktifkan-virtual-environment)

1. Untuk menghentikan server, tekan `Ctrl+C` (Windows/Linux) atau `Control+C` (Mac) di terminal.

2. Nonaktifkan _virtual environment_:





```
deactivate
```


Selamat, kamu sudah berhasil membuat aplikasi Django dari awal!

### Langkah 6: Simpan Perubahan ke GitHub [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#langkah-6-simpan-perubahan-ke-github)

Buat berkas `.gitignore` di root proyek (sejajar dengan `manage.py`) supaya `env/`, berkas `.env`/`.env.prod`, `db.sqlite3`, dan berkas sementara lain tidak ikut ter- _commit_:

```
# Django
*.log
*.pot
*.pyc
__pycache__/
db.sqlite3
media

# Backup files
*.bak

# If you are using PyCharm
.idea/**/workspace.xml
.idea/**/tasks.xml
.idea/**/usage.statistics.xml
.idea/**/dictionaries
.idea/**/shelf
.idea/**/aws.xml
.idea/**/contentModel.xml
.idea/**/dataSources/
.idea/**/dataSources.ids
.idea/**/dataSources.local.xml
.idea/**/sqlDataSources.xml
.idea/**/dynamic.xml
.idea/**/uiDesigner.xml
.idea/**/dbnavigator.xml
.idea/**/gradle.xml
.idea/**/libraries
*.iws

# IntelliJ
out/

# JIRA plugin
atlassian-ide-plugin.xml

# Python
*.py[cod]
*$py.class
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
.pytest_cache/
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery
celerybeat-schedule.*

# SageMath parsed files
*.sage.py

# Environments
.env*
!.env.example*
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# mkdocs documentation
/site

# mypy
.mypy_cache/

# Sublime Text
*.tmlanguage.cache
*.tmPreferences.cache
*.stTheme.cache
*.sublime-workspace
*.sublime-project

# sftp configuration file
sftp-config.json

# Visual Studio Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
.history

# macOS
.DS_Store
```

Penting

Berkas `.env` dan `.env.prod` **tidak boleh** ikut ter- _push_ ke GitHub karena (nantinya) berisi kredensial - pastikan `.gitignore` di atas sudah dibuat SEBELUM kamu menjalankan `git add`.

Aktifkan lagi _virtual environment_ kalau perlu, lalu commit dan push proyek Django yang baru dibuat.

```
git add .
git commit -m "Initial Django project setup"
git push origin main
```

Penting

**Menghubungkan ke Proyek Kamu** \- repositori `myportofolio` yang baru kamu buat ini **adalah** website portofolio pribadimu untuk sepanjang semester, bukan latihan sekali pakai. Struktur, riwayat commit, dan branch yang kamu buat di sini akan terus berkembang di tutorial-tutorial berikutnya.

## Akhir Kata [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#akhir-kata)

Selamat! Kamu sudah menyiapkan akun GitHub, IDE, Git, dan proyek Django pertamamu. Di Tutorial 01 minggu depan, kamu akan melanjutkan langsung dari proyek Django ini untuk membangun halaman “About Me” pertama di portofoliomu.

## Referensi Tambahan [Anchor](https://pbp.cs.ui.ac.id/tutorial/tutorial-0.html\#referensi-tambahan)

- [About pull request merges](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges)
- [Resolving a merge conflict on GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-on-github)
- [Git - Getting Started](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [Django - Installation](https://docs.djangoproject.com/en/4.2/topics/install/)