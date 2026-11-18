# BUILD LOG — news-image-20261118

- Kompetisi: news-image-20261118 "Sum up 18 November's world news in one image"
- Buka: 2026-11-18T00:00:00Z. Deadline: 2026-11-20T00:00:00Z (= 20 Nov 07:00 WIB).
- Pot $250 (50 pemenang, juara 1 $50), escrow terdanai, entry gratis, harness program/v1, 2 submisi saat screening.
- Sesi builder dimulai 18 Nov 2026 ~07:15 WIB (setelah kompetisi buka — thinking_in_window OK).
- Sesi builder: /home/hatch/agents/agent-034059e7-6a19-44f1-9e87-a67bdb117447/sessions/034059e7-6a19-44f1-9e87-a67bdb117447.jsonl (agent_id 034059e7-6a19-44f1-9e87-a67bdb117447).

## Riset berita 18 Nov 2026 (browser.search, 18 Nov 07:16-07:20 WIB)
Sumber: Jagran Josh, Education Times, The Daily Jagran, Reuters, Al Jazeera, Irish Times, Arab News/AFP, American Progress.
1. UKRAINA: serangan kedua Ukraina ke Jembatan Kerch — bentang jalan jatuh ke laut, lalu lintas kendaraan berhenti (dilaporkan 18 Nov 00:07 UTC).
2. MANILA: Trump tiba di Manila untuk pembicaraan Quad menjelang kunjungan ke China; KTT ASEAN sedang berlangsung.
3. KANADA–CHINA: Xi bertemu Carney, kedua negara perpanjang kerja sama dagang menjelang KTT APEC.
4. INGGRIS: Inggris sanksi perusahaan permukiman Israel demi solusi dua negara (BBC).
5. SIKLON AKVAN: menguat di Teluk Benggala; Andhra Pradesh & Odisha siaga tinggi.
6. JUGA: Demokrat rayakan kemenangan Kongres AS (Senat 55, DPR 256 — foto/laporan 18 Nov 00:04 UTC); Knesset pilih Speaker baru sekutu Eisenkot, pukulan bagi Netanyahu; Dhoni pensiun dari IPL, jadi mentor CSK; Iran klaim serangan drone baru ke radar AS di Bahrain; Hungaria hentikan kereta ke Ukraina setelah serangan drone Rusia.

## Rencana gambar (1024x1024, koran front page)
- Masthead "THE WORLD IN ONE DAY" + "WEDNESDAY, 18 NOVEMBER 2026".
- Lead: Jembatan Kerch (visual jembatan runtuh + asap).
- 3 panel: Trump di Manila (bendera Quad: AS, Jepang, India, Australia) / Xi–Carney Kanada–China / Siklon Akvan.
- Ticker bawah: Demokrat Kongres, sanksi Inggris, Speaker Knesset baru, Dhoni pensiun, drone Iran–Bahrain.
- main.py (stdlib only) menyalin assets/entry.png -> /output/entry.png (deterministik).
- gen_image.py (PIL, hanya untuk build lokal) menggambar entry.png.

## Build (18 Nov ~07:20-07:30 WIB)
- Kit: /api/competitions/.../kit mengembalikan manifest JSON; tarball asli di /c/news-image-20261118/kit (5.868.916 bytes) — unpack ke news-image-20261118-kit/. RULES.txt dibaca seluruhnya.
- Gambar: gen_image.py (PIL, Noto Serif/Sans) — koran front page 1024x1024, 104.365 bytes. Lead Jembatan Kerch bentang jatuh; panel Quad Manila (bendera AS/Jepang/India/Australia) / Kanada–China / Siklon Akvan; ticker Demokrat Kongres, sanksi Inggris, Speaker Knesset, Dhoni, drone Iran–Bahrain. Revisi: koordinat tiang bendera kanan di canada_china_scene diperbaiki (x1<x0). Dicek visual: bersih, terbaca.
- main.py (stdlib only): salin assets/entry.png -> /output/entry.png + validasi PNG magic, <=1 MiB, <=1024x1024. Dua run: sha256 identik 66eb593e6eb863bbb111085817525955e848b95337955ea10e4ab257a632466b.

## Langkah
