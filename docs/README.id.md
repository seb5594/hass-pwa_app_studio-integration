# Memasang, memasangkan, dan memperbarui aplikasi web

## Kirim dasbor ke seseorang yang Anda kenal

Contoh. Sebastian membuat aplikasi web yang menunjukkan keberangkatan kereta. Pamannya sudah menggunakan Aplikasi Pendamping Home Assistant resmi dan memiliki akses ke dasbor. Sebastian mengirimkan link browser melalui WhatsApp.

1. Di PWA Web-App Studio, buka aplikasi, buka Access, aktifkan masuk melalui Aplikasi Pendamping, dan simpan. Kedua aplikasi harus menjangkau server Home Assistant yang sama melalui HTTPS.

2. Tamu Anda membuka tautan WhatsApp di browser mereka dan memilih Masuk melalui Aplikasi Pendamping. Aplikasi web menampilkan kode perangkat. Tamu dapat menyalinnya jika diperlukan.

3. Ketuk Buka Home Assistant. Konfirmasikan bahwa aplikasi, akun, dan kode cocok. Jika halaman penyandingan meminta kode, tempel atau masukkan kode yang ditampilkan di aplikasi web. Kemudian setujui masuk.

4. Beralih kembali ke tab browser asli. Itu masuk secara otomatis. Jika perlu, ketuk Periksa persetujuan. Kode ini valid selama lima menit dan untuk satu kali masuk.

5. Di iPhone atau iPad, untuk masuk ke salinan yang diinstal, pertama-tama tambahkan halaman ke Layar Utama di Safari. Buka ikon Layar Beranda dan mulai proses persetujuan yang sama di sana.

## Temukan Studionya

Gunakan perlengkapan integrasi, lalu buka Studio melalui dialog Home Assistant. Jika Anda sering mengerjakan aplikasi, aktifkan entitas pengalih Panel Sidebar di pengaturan integrasi dan aktifkan agar pintasan tetap terlihat.

Untuk dasbor pemeliharaan, tambahkan kartu tombol yang menavigasi ke /pwa-app-studio. Entitas tombol Open PWA Designer opsional juga dapat membukanya di sesi administrator aktif Anda. Aktifkan entitas tersebut terlebih dahulu; Home Assistant menonaktifkannya secara default.

## Rancang dan perbarui dasbor tamu

Misalnya, buat dasbor untuk pengunjung dengan kartu informasi Wi-Fi dan lampu teras. Di bawah Konten, pilih masing-masing kartu dan pilih preset atau impor kartu yang ada. Tetapkan judul, entitas, atau Markdown menggunakan editor visual dan periksa pratinjau ponsel.

Pada langkah Aplikasi, atur versi Aplikasi ke 1.1 dan simpan. Tamu yang aplikasinya masih terbuka akan melihat spanduk pembaruan saat aplikasi mendeteksi revisi baru. Mengetuk Perbarui aplikasi akan memuat ulang tampilan dan mempertahankan ikon layar beranda dan sesi browser. Aplikasi yang dibuka kemudian memuat versi saat ini saat terhubung.

## Bagikan dari Android

Gunakan Berbagi tautan di Studio. Dialog asli terbuka ketika aplikasi atau browser menyediakannya. Jika Aplikasi Pendamping tidak menawarkan API berbagi, buka halaman berbagi di browser. Anda juga dapat menyalin tautannya.

[English README](../README.md) · [Deutsch](../README.de.md)
