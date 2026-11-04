# 🎛️ Stem Separator Pro (Studio Edition & YouTube Media Center)

**Stem Separator Pro** là hệ thống tách nhạc, giọng hát & giọng bè chuyên nghiệp (3-Way / 4-Stems) kết hợp bàn mixer đa kênh thời gian thực và công cụ tải nhạc YouTube đa định dạng.

---

## 🌟 Tính Năng Nổi Bật

### 1. 🎚️ Bàn Mix Âm Thanh 4 Kênh Trực Tiếp (Multi-track Studio Mixer)
- Phát đồng bộ 4 track âm thanh cùng lúc:
  - 🎵 **Instrumental**: Beat sạch tách bằng model cao cấp `BS-RoFormer SDR 12.97dB`.
  - 🎤 **Lead Vocals**: Giọng hát chính của ca sĩ.
  - 🎶 **Backing Vocals**: Giọng bè & hòa âm tách bằng `UVR-BVE-4B`.
  - 🌟 **Karaoke Mix**: Bản phối Beat + Dàn bè đệm hòa âm chuẩn sân khấu.
- Điều khiển độc lập từng kênh:
  - Thanh chỉnh **Volume (Âm lượng)**
  - Nút **MUTE** (Tắt tiếng kênh)
  - Nút **SOLO** (Chỉ phát riêng kênh được chọn)
  - Nút **Tải Trọn Bộ 4 Stems (.ZIP)** tiện lợi.

### 2. 🔗 Dán Link Tách Nhạc Trực Tiếp (YouTube / TikTok / SoundCloud)
- Không cần tải file về máy tính trước. Chỉ cần dán đường link bài hát, cỗ máy tự động trích xuất luồng âm thanh gốc độ phân giải cao và tiến hành tách Stems.

### 3. 🎛️ 4 Preset "Một Chạm" Thông Minh
- 🎤 **Hát Karaoke Chuyên Nghiệp**: Beat sạch + Dàn bè đệm sân khấu (`BS-RoFormer` + `UVR-BVE-4B`).
- 🎧 **Làm Nhạc Remix / Acapella**: Lấy giọng ca mộc sạch bóng cho Producer (`BS-RoFormer` + `UVR-MDX-NET-Voc_FT`).
- 🎼 **Bóc Giọng Bè Luyện Thanh**: Tách riêng bè cao, bè trầm để luyện thanh, phân tích hòa âm.
- ⚡ **Siêu Tốc (Fast Mode)**: Tách cực nhanh 15-20s với `MDX-Net`.

### 4. 📥 Tải Nhạc & Video YouTube Đa Định Dạng
- 🎵 **Audio MP3 (320kbps)**: Âm thanh chất lượng cao.
- 🎵 **Audio WAV**: Studio Lossless Master 24-bit.
- 🎬 **Video MP4 1080p (Full HD)**, **720p (HD)**, **480p/360p** (Dung lượng nhẹ).

---

## 🚀 Cài Đặt & Khởi Chạy

### Yêu Cầu Hệ Thống:
- Python 3.10+
- FFmpeg (đã thêm vào PATH hệ thống)
- GPU NVIDIA (CUDA) khuyên dùng để tăng tốc tách nhạc

### Cài Đặt Thư Viện:
```bash
pip install fastapi uvicorn audio-separator yt-dlp python-multipart
```

### Khởi Chạy Server:
```bash
python server.py
```
Mở trình duyệt truy cập: **`http://localhost:8090`**

---

## 🛠️ Cấu Trúc Dự Án
```text
stem_separator_pro/
├── downloader.py     # Module tải nhạc YouTube, trích xuất audio WAV & đa định dạng
├── engine.py         # Cỗ máy xử lý tách âm thanh 3 giai đoạn (audio-separator)
├── server.py         # FastAPI Web Server & Giao diện Studio Mixer HTML5/TailwindCSS
├── pyproject.toml    # Cấu hình dự án
├── .gitignore        # Loại trừ file tạm, cache và dữ liệu âm thanh
└── README.md         # Hướng dẫn sử dụng
```

---
*Engineered with passion by LO & ENI.*
