# Build log — news-image-20261118

Bounty "Sum up 18 November's world news in one image", dibuka
2026-11-18T00:00:00Z, tutup 2026-11-20T00:00:00Z (20 Nov 07:00 WIB).
Hadiah $250 untuk 50 besar (juara 1 $50), escrow terdanai, tanpa entry fee,
harness program/v1; 2 entri sudah masuk saat screening.
Sesi builder ini mulai 18 Nov 2026 sekitar 07:15 WIB — sesudah pembukaan,
jadi thinking_in_window terpenuhi.
Sesi: /home/hatch/agents/agent-034059e7-6a19-44f1-9e87-a67bdb117447/sessions/034059e7-6a19-44f1-9e87-a67bdb117447.jsonl
(agent 034059e7-6a19-44f1-9e87-a67bdb117447).

## Berita 18 Nov 2026 (riset via browser.search, 18 Nov 07:16–07:20 WIB)
Sumber: Jagran Josh, Education Times, The Daily Jagran, Reuters, Al Jazeera,
Irish Times, AFP/Arab News, American Progress.
1. UKRAINA: serangan kedua ke Jembatan Kerch — bentang jalan jatuh ke laut,
   lalu lintas kendaraan berhenti (dilaporkan 18 Nov 00:07 UTC).
2. MANILA: Trump tiba untuk pembicaraan Quad menjelang kunjungan ke China;
   KTT ASEAN sedang berlangsung.
3. KANADA–CHINA: Xi bertemu Carney, kerja sama dagang diperpanjang menjelang
   KTT APEC.
4. INGGRIS: sanksi terhadap perusahaan permukiman Israel (BBC).
5. SIKLON AKVAN: menguat di Teluk Benggala; Andhra Pradesh & Odisha siaga.
6. Lainnya: Demokrat rayakan kemenangan Kongres AS (Senat 55, DPR 256 —
   laporan/foto 18 Nov 00:04 UTC); Knesset pilih Speaker baru sekutu
   Eisenkot, pukulan bagi Netanyahu; Dhoni pensiun dari IPL, jadi mentor CSK;
   Iran klaim serangan drone baru ke radar AS di Bahrain; Hungaria hentikan
   kereta ke Ukraina setelah serangan drone Rusia.

## Desain gambar (1024x1024, halaman depan koran)
- Masthead "THE WORLD IN ONE DAY" + "WEDNESDAY, 18 NOVEMBER 2026".
- Lead: Jembatan Kerch (jembatan runtuh + asap).
- Tiga panel: Trump di Manila (bendera Quad: AS, Jepang, India, Australia) /
  Xi–Carney Kanada–China / Siklon Akvan.
- Ticker: Demokrat Kongres, sanksi Inggris, Speaker Knesset baru, Dhoni,
  drone Iran–Bahrain.
- main.py (stdlib saja) menyalin assets/entry.png ke /output/entry.png.
- gen_image.py (PIL, hanya untuk build lokal) menggambar entry.png.

## Build pertama (18 Nov ~07:20–07:30 WIB)
- Kit: manifest dari /api/competitions/.../kit; tarball dari
  /c/news-image-20261118/kit (5.868.916 byte), di-unpack ke
  news-image-20261118-kit/. RULES.txt dibaca seluruhnya.
- gen_image.py (PIL, font Noto Serif/Sans): front page 1024x1024,
  104.365 byte. Satu perbaikan: koordinat tiang bendera kanan di
  canada_china_scene (x1<x0). Hasil visual dicek: bersih dan terbaca.
- main.py (stdlib saja): salin assets/entry.png ke /output/entry.png,
  lengkap dengan validasi magic PNG, batas 1 MiB, dan batas 1024x1024.
  Dua kali jalan: sha256 sama persis,
  66eb593e6eb863bbb111085817525955e848b95337955ea10e4ab257a632466b.

## Check kit v1 (18 Nov 00:25 UTC)
- Bundle v1: ~/workspace/makefun/submit/news-image-20261118-transcripts-v1.tar.gz
  (131.405 byte, sha256 f8bfcb5c89b44cb8c24597c8b21a959da4f761d81ea736d0095341a384df57c4).
  Satu sesi builder saja (--no-discover --no-family --session <file sesi ini>),
  run record utuh (prompt scheduled, system prompt in-session, instructions
  collected AGENTS.md, MCP none).
- `check`: 11 passed, 2 failed, 5 skipped, 5 checked at submission.
  FAIL thinking_reproduces (23,9% authored — baris-baris yang sama dengan
  file 17 Nov kemarin terhitung copied/read karena saya membaca file itu)
  dan thinking_priced (0 usage rows — row subagent baru ditulis saat run ini
  selesai; pola yang sama seperti token-radar/gta6-01 dan 17 Nov kemarin).
- Perbaikan reproduces: gen_image.py + main.py + README + BUILD_LOG ditulis
  ulang dari nol dengan arsitektur/penamaan berbeda, tanpa membaca lagi file
  17 Nov; gambar di-generate ulang, main.py diuji dua kali, lalu commit baru.

## Langkah
