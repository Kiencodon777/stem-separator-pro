"""
Stem Separator Pro - Studio Edition & YouTube Media Center
Features:
1. High-Precision 3-Way Stem Separation (Beat, Lead Vocals, Backing Vocals, Karaoke Mix)
2. Interactive Web Audio 4-Track Studio Mixer (Sync Playback, Volume, Mute, Solo, Waveform)
3. Direct YouTube / TikTok / SoundCloud URL Separation
4. One-Click Smart Presets
5. Dedicated Multi-format YouTube Downloader Tab (MP3 320k, WAV Lossless, MP4 1080p/720p/480p)
"""

import os
import shutil
import zipfile
import uuid
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from engine import StemSeparatorPro
from downloader import get_media_info, download_for_separation, download_media_format

app = FastAPI(title="Stem Separator Pro & Studio Media Center")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE = BASE_DIR / "workspace"
WORKSPACE.mkdir(exist_ok=True)

engine = StemSeparatorPro(work_dir=str(WORKSPACE))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stem Separator Pro - Studio Edition & YouTube Media Center</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: #080B11; color: #E2E8F0; }
        .glass { background: rgba(18, 23, 33, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .glow-cyan { box-shadow: 0 0 25px rgba(6, 182, 212, 0.25); }
        .glow-btn { background: linear-gradient(135deg, #06B6D4, #3B82F6); box-shadow: 0 4px 20px rgba(6, 182, 212, 0.35); }
        .glow-btn:hover { background: linear-gradient(135deg, #0891B2, #2563EB); box-shadow: 0 6px 25px rgba(6, 182, 212, 0.5); }
        .preset-active { border-color: #06B6D4 !important; background: rgba(6, 182, 212, 0.12) !important; }
        .channel-active { border-left: 4px solid #06B6D4; }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            height: 16px;
            width: 16px;
            border-radius: 50%;
            background: #06B6D4;
            cursor: pointer;
            box-shadow: 0 0 10px #06B6D4;
        }
        .anim-bar {
            animation: pulseHeight 1.2s ease-in-out infinite alternate;
        }
        @keyframes pulseHeight {
            0% { height: 15%; }
            100% { height: 95%; }
        }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between">
    <!-- Navbar with Tabs -->
    <nav class="border-b border-white/10 px-6 py-4 glass sticky top-0 z-50 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center font-black text-xl text-cyan-400">🎛️</div>
            <div>
                <span class="text-xl font-extrabold tracking-tight bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">Stem Separator Pro</span>
                <span class="text-xs ml-2 px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">Studio v2.5</span>
            </div>
        </div>

        <!-- Tab Switcher -->
        <div class="flex items-center bg-white/5 p-1 rounded-xl border border-white/10">
            <button onclick="switchTab('stems')" id="tabStemsBtn" class="px-5 py-2 rounded-lg text-sm font-bold transition flex items-center gap-2 bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                <span>🎛️ Tách Stems & Mixer</span>
            </button>
            <button onclick="switchTab('downloader')" id="tabDownloaderBtn" class="px-5 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 text-slate-400 hover:text-white">
                <span>📥 Tải YouTube Đa Năng</span>
            </button>
        </div>

        <div class="flex items-center space-x-2">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                GPU Acceleration Active
            </span>
        </div>
    </nav>

    <!-- TAB 1: STEM SEPARATOR & STUDIO MIXER -->
    <main id="tabStemsContent" class="flex-1 max-w-5xl w-full mx-auto p-6 md:p-8 space-y-8">
        <div class="text-center space-y-2">
            <h1 class="text-3xl md:text-5xl font-black tracking-tight">Tách Beat, Giọng Chính & Bè Chuyên Nghiệp</h1>
            <p class="text-slate-400 text-sm md:text-base max-w-2xl mx-auto">
                Sử dụng thuật toán AI BS-RoFormer & UVR-BVE 4B cao cấp nhất để bóc tách 3 luồng âm thanh độc lập và tinh chỉnh trực tiếp trên Bàn Mixer 4 kênh.
            </p>
        </div>

        <!-- Step 1: Input Selection (Upload or URL) -->
        <div class="glass rounded-2xl p-6 md:p-8 space-y-6 glow-cyan">
            <div class="flex items-center justify-between border-b border-white/10 pb-4">
                <span class="text-base font-bold text-slate-200 flex items-center gap-2">
                    <span class="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-sm font-black">1</span>
                    Chọn Nguồn Nhạc Cần Tách
                </span>
                <div class="flex gap-2">
                    <button type="button" onclick="setInputMode('file')" id="modeFileBtn" class="px-3.5 py-1.5 rounded-lg text-xs font-bold transition bg-cyan-500 text-slate-900">
                        📁 Tải File Lên
                    </button>
                    <button type="button" onclick="setInputMode('url')" id="modeUrlBtn" class="px-3.5 py-1.5 rounded-lg text-xs font-bold transition bg-white/5 text-slate-400 hover:text-white border border-white/10">
                        🔗 Dán Link (YouTube/TikTok)
                    </button>
                </div>
            </div>

            <!-- Upload File Box -->
            <div id="fileUploadContainer" class="space-y-4">
                <div id="dropZone" class="border-2 border-dashed border-white/15 rounded-2xl p-8 text-center hover:border-cyan-500/50 transition cursor-pointer bg-white/[0.02]" onclick="document.getElementById('audioInput').click()">
                    <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-cyan-500/10 flex items-center justify-center text-3xl">🎵</div>
                    <p class="text-base font-semibold text-slate-200">Kéo & thả file bài hát vào đây, hoặc click để chọn file</p>
                    <p class="text-xs text-slate-400 mt-1">Hỗ trợ định dạng MP3, WAV, FLAC, M4A, OGG... (Chất lượng càng cao tách càng sạch)</p>
                    <input type="file" id="audioInput" accept="audio/*" class="hidden" onchange="handleFileSelect(event)">
                </div>
                <div id="fileInfoBox" class="hidden items-center justify-between p-3.5 bg-cyan-500/10 border border-cyan-500/30 rounded-xl">
                    <div class="flex items-center space-x-3 overflow-hidden">
                        <span class="text-2xl">🎧</span>
                        <div class="truncate">
                            <p id="fileName" class="text-sm font-bold text-cyan-300 truncate">track.mp3</p>
                            <p id="fileSize" class="text-xs text-slate-400">12.5 MB</p>
                        </div>
                    </div>
                    <button onclick="clearSelectedFile()" class="text-xs text-red-400 hover:text-red-300 font-bold px-3 py-1">Xóa</button>
                </div>
            </div>

            <!-- URL Input Box -->
            <div id="urlInputContainer" class="hidden space-y-4">
                <div class="relative">
                    <input type="text" id="streamUrlInput" placeholder="Dán link bài hát từ YouTube, TikTok hoặc SoundCloud..." class="w-full bg-[#131720] border border-white/10 rounded-xl px-4 py-3.5 pl-11 text-sm focus:outline-none focus:border-cyan-500 text-slate-200">
                    <span class="absolute left-4 top-3.5 text-slate-500 text-lg">🔗</span>
                </div>
                <p class="text-xs text-slate-400">Hệ thống sẽ tự động trích xuất luồng âm thanh gốc độ phân giải cao và tiến hành tách Stems ngay lập tức.</p>
            </div>

            <!-- Step 2: One-Click Presets -->
            <div class="space-y-3 pt-2">
                <label class="block text-sm font-bold text-slate-200 flex items-center gap-2">
                    <span class="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-sm font-black">2</span>
                    Chọn Preset Mục Đích Sử Dụng (One-Click)
                </label>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
                    <!-- Preset 1 -->
                    <div onclick="selectPreset('karaoke')" id="preset_karaoke" class="preset-card preset-active glass p-4 rounded-xl cursor-pointer border border-white/10 hover:border-cyan-500/40 transition">
                        <div class="text-2xl mb-1.5">🎤</div>
                        <h4 class="text-sm font-bold text-white">Karaoke Chuyên Nghiệp</h4>
                        <p class="text-xs text-slate-400 mt-1">Beat sạch 100% + Dàn bè đệm hòa âm chuẩn sân khấu.</p>
                    </div>
                    <!-- Preset 2 -->
                    <div onclick="selectPreset('remix')" id="preset_remix" class="preset-card glass p-4 rounded-xl cursor-pointer border border-white/10 hover:border-cyan-500/40 transition">
                        <div class="text-2xl mb-1.5">🎧</div>
                        <h4 class="text-sm font-bold text-white">Làm Nhạc Remix / Acapella</h4>
                        <p class="text-xs text-slate-400 mt-1">Lấy giọng ca mộc sạch bóng, lọc sạch tiếng trống & bass.</p>
                    </div>
                    <!-- Preset 3 -->
                    <div onclick="selectPreset('backing')" id="preset_backing" class="preset-card glass p-4 rounded-xl cursor-pointer border border-white/10 hover:border-cyan-500/40 transition">
                        <div class="text-2xl mb-1.5">🎼</div>
                        <h4 class="text-sm font-bold text-white">Bóc Giọng Bè Luyện Thanh</h4>
                        <p class="text-xs text-slate-400 mt-1">Tách riêng bè cao, bè trầm để phân tích hòa âm và tập hát.</p>
                    </div>
                    <!-- Preset 4 -->
                    <div onclick="selectPreset('fast')" id="preset_fast" class="preset-card glass p-4 rounded-xl cursor-pointer border border-white/10 hover:border-cyan-500/40 transition">
                        <div class="text-2xl mb-1.5">⚡</div>
                        <h4 class="text-sm font-bold text-white">Siêu Tốc (Fast Mode)</h4>
                        <p class="text-xs text-slate-400 mt-1">Chạy nhanh trong 15-20s bằng MDX-Net nhẹ nhàng.</p>
                    </div>
                </div>
            </div>

            <!-- Hidden Advanced Model Inputs (Auto set by Preset) -->
            <input type="hidden" id="vocalModel" value="model_bs_roformer_ep_317_sdr_12.9755.ckpt">
            <input type="hidden" id="backingModel" value="UVR-BVE-4B_SN-44100-2.pth">

            <!-- Submit Button -->
            <button onclick="startSeparation()" id="submitBtn" class="w-full glow-btn py-4 rounded-xl font-bold text-base text-slate-900 transition flex items-center justify-center space-x-2">
                <span>⚡ Bắt Đầu Tách 3 Đường Tiếng</span>
            </button>
        </div>

        <!-- Progress Box -->
        <div id="progressBox" class="glass rounded-2xl p-6 hidden space-y-4">
            <div class="flex items-center justify-between">
                <span id="statusText" class="text-sm font-semibold text-cyan-300">Đang khởi chạy cỗ máy AI...</span>
                <span id="percentText" class="text-xs font-extrabold text-cyan-400 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 animate-pulse">ĐANG XỬ LÝ</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-3 overflow-hidden">
                <div id="progressBar" class="bg-gradient-to-r from-cyan-400 to-blue-500 h-3 rounded-full w-1/4 transition-all duration-500"></div>
            </div>
            <p class="text-xs text-slate-400 text-center">Giai đoạn 1: Tách Beat bằng BS-RoFormer ➔ Giai đoạn 2: Tách Bè bằng UVR-BVE ➔ Giai đoạn 3: Phối Karaoke Mix</p>
        </div>

        <!-- STUDIO 4-TRACK MULTI-TRACK MIXER -->
        <div id="mixerBox" class="glass rounded-2xl p-6 md:p-8 hidden space-y-6">
            <div class="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 pb-5">
                <div>
                    <h3 class="text-xl font-black text-white flex items-center gap-2">
                        <span>🎚️</span> Bàn Mix Âm Thanh 4 Kênh (Studio Multi-track Player)
                    </h3>
                    <p class="text-xs text-slate-400 mt-1">Cả 4 track phát đồng bộ thời gian thực. Chỉnh volume, Mute hoặc Solo từng kênh để thưởng thức.</p>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="downloadAllZip()" class="px-4 py-2 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/20 text-white transition flex items-center gap-1.5 border border-white/10">
                        <span>📦</span> Tải Trọn Bộ 4 Stems (WAV)
                    </button>
                    <button onclick="resetApp()" class="px-3.5 py-2 rounded-xl text-xs font-bold text-slate-400 hover:text-white transition">
                        Tách Bài Khác
                    </button>
                </div>
            </div>

            <!-- Master Transport Controls -->
            <div class="p-4 bg-black/40 rounded-xl border border-white/10 flex flex-wrap items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                    <button onclick="toggleMasterPlay()" id="masterPlayBtn" class="w-12 h-12 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-black text-xl flex items-center justify-center transition shadow-lg">
                        ▶
                    </button>
                    <button onclick="stopMasterPlay()" class="w-10 h-10 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold flex items-center justify-center transition">
                        ⏹
                    </button>
                    <span id="timeDisplay" class="text-sm font-mono font-bold text-cyan-300 ml-2">00:00 / 00:00</span>
                </div>

                <!-- Global Timeline Scrubber -->
                <div class="flex-1 min-w-[200px] flex items-center gap-3">
                    <input type="range" id="masterTimeline" min="0" max="100" value="0" step="0.1" oninput="seekMaster(this.value)" class="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer">
                </div>
            </div>

            <!-- 4 Channels Strips -->
            <div class="space-y-3.5">
                <!-- Channel 1: Beat / Instrumental -->
                <div class="channel-active p-4 bg-white/[0.02] rounded-xl border border-white/10 flex flex-wrap items-center justify-between gap-4">
                    <div class="flex items-center space-x-3 w-48">
                        <span class="text-2xl">🎵</span>
                        <div>
                            <h4 class="text-sm font-bold text-white">Beat Sạch</h4>
                            <span class="text-[10px] text-cyan-400 uppercase font-bold tracking-wider">Instrumental</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="toggleMute(0)" id="muteBtn_0" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 transition">MUTE</button>
                        <button onclick="toggleSolo(0)" id="soloBtn_0" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-white/5 hover:bg-white/10 text-yellow-400 border border-white/10 transition">SOLO</button>
                    </div>
                    <div class="flex items-center gap-3 flex-1 min-w-[150px]">
                        <span class="text-xs text-slate-400">Vol</span>
                        <input type="range" min="0" max="1" step="0.01" value="1" oninput="setChannelVolume(0, this.value)" class="w-full h-1.5 bg-white/20 rounded-lg appearance-none cursor-pointer">
                    </div>
                    <a id="download_0" href="#" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 transition">
                        ⬇ Tải WAV
                    </a>
                </div>

                <!-- Channel 2: Lead Vocals -->
                <div class="channel-active p-4 bg-white/[0.02] rounded-xl border border-white/10 flex flex-wrap items-center justify-between gap-4">
                    <div class="flex items-center space-x-3 w-48">
                        <span class="text-2xl">🎤</span>
                        <div>
                            <h4 class="text-sm font-bold text-white">Giọng Ca Chính</h4>
                            <span class="text-[10px] text-emerald-400 uppercase font-bold tracking-wider">Lead Vocals</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="toggleMute(1)" id="muteBtn_1" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 transition">MUTE</button>
                        <button onclick="toggleSolo(1)" id="soloBtn_1" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-white/5 hover:bg-white/10 text-yellow-400 border border-white/10 transition">SOLO</button>
                    </div>
                    <div class="flex items-center gap-3 flex-1 min-w-[150px]">
                        <span class="text-xs text-slate-400">Vol</span>
                        <input type="range" min="0" max="1" step="0.01" value="1" oninput="setChannelVolume(1, this.value)" class="w-full h-1.5 bg-white/20 rounded-lg appearance-none cursor-pointer">
                    </div>
                    <a id="download_1" href="#" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 transition">
                        ⬇ Tải WAV
                    </a>
                </div>

                <!-- Channel 3: Backing Vocals -->
                <div class="channel-active p-4 bg-white/[0.02] rounded-xl border border-white/10 flex flex-wrap items-center justify-between gap-4">
                    <div class="flex items-center space-x-3 w-48">
                        <span class="text-2xl">🎶</span>
                        <div>
                            <h4 class="text-sm font-bold text-white">Giọng Bè & Hòa Âm</h4>
                            <span class="text-[10px] text-purple-400 uppercase font-bold tracking-wider">Backing Vocals</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="toggleMute(2)" id="muteBtn_2" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 transition">MUTE</button>
                        <button onclick="toggleSolo(2)" id="soloBtn_2" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-white/5 hover:bg-white/10 text-yellow-400 border border-white/10 transition">SOLO</button>
                    </div>
                    <div class="flex items-center gap-3 flex-1 min-w-[150px]">
                        <span class="text-xs text-slate-400">Vol</span>
                        <input type="range" min="0" max="1" step="0.01" value="1" oninput="setChannelVolume(2, this.value)" class="w-full h-1.5 bg-white/20 rounded-lg appearance-none cursor-pointer">
                    </div>
                    <a id="download_2" href="#" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 border border-purple-500/30 transition">
                        ⬇ Tải WAV
                    </a>
                </div>

                <!-- Channel 4: Karaoke Mix -->
                <div class="channel-active p-4 bg-white/[0.02] rounded-xl border border-white/10 flex flex-wrap items-center justify-between gap-4">
                    <div class="flex items-center space-x-3 w-48">
                        <span class="text-2xl">🌟</span>
                        <div>
                            <h4 class="text-sm font-bold text-white">Karaoke Mix</h4>
                            <span class="text-[10px] text-yellow-400 uppercase font-bold tracking-wider">Beat + Bè Đệm</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="toggleMute(3)" id="muteBtn_3" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 transition">MUTE</button>
                        <button onclick="toggleSolo(3)" id="soloBtn_3" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-white/5 hover:bg-white/10 text-yellow-400 border border-white/10 transition">SOLO</button>
                    </div>
                    <div class="flex items-center gap-3 flex-1 min-w-[150px]">
                        <span class="text-xs text-slate-400">Vol</span>
                        <input type="range" min="0" max="1" step="0.01" value="0" oninput="setChannelVolume(3, this.value)" class="w-full h-1.5 bg-white/20 rounded-lg appearance-none cursor-pointer">
                    </div>
                    <a id="download_3" href="#" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-yellow-500/10 hover:bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 transition">
                        ⬇ Tải WAV
                    </a>
                </div>
            </div>
        </div>
    </main>

    <!-- TAB 2: YOUTUBE / MEDIA DOWNLOADER TAB -->
    <main id="tabDownloaderContent" class="flex-1 max-w-4xl w-full mx-auto p-6 md:p-8 space-y-8 hidden">
        <div class="text-center space-y-2">
            <h1 class="text-3xl md:text-5xl font-black tracking-tight">Tải Nhạc & Video YouTube Đa Định Dạng</h1>
            <p class="text-slate-400 text-sm md:text-base max-w-xl mx-auto">
                Tải trực tiếp âm thanh Studio Lossless WAV, MP3 320kbps hoặc Video MP4 ở nhiều độ phân giải khác nhau (1080p, 720p, 480p).
            </p>
        </div>

        <div class="glass rounded-2xl p-6 md:p-8 space-y-6 glow-cyan">
            <div class="space-y-3">
                <label class="block text-sm font-bold text-slate-200">Dán Link Video YouTube / Shorts / Music</label>
                <div class="flex gap-2">
                    <input type="text" id="ytUrlInput" placeholder="https://www.youtube.com/watch?v=..." class="flex-1 bg-[#131720] border border-white/10 rounded-xl px-4 py-3.5 text-sm focus:outline-none focus:border-cyan-500 text-slate-200">
                    <button onclick="fetchYouTubeInfo()" id="btnFetchYt" class="glow-btn px-6 py-3.5 rounded-xl font-bold text-sm text-slate-900 transition flex items-center gap-2">
                        <span>🔍</span> Kiểm Tra
                    </button>
                </div>
            </div>

            <!-- Loading Spinner -->
            <div id="ytLoading" class="hidden text-center py-6">
                <div class="inline-block w-8 h-8 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
                <p class="text-xs text-slate-400 mt-2">Đang phân tích thông tin video...</p>
            </div>

            <!-- Video Preview Card -->
            <div id="ytInfoCard" class="hidden p-5 bg-white/[0.03] rounded-2xl border border-white/10 space-y-5">
                <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
                    <img id="ytThumb" src="" alt="Thumbnail" class="w-full sm:w-44 h-28 object-cover rounded-xl border border-white/10">
                    <div class="space-y-1.5 flex-1 overflow-hidden">
                        <h3 id="ytTitle" class="text-base font-bold text-white line-clamp-2">Title</h3>
                        <p id="ytUploader" class="text-xs text-slate-400">Uploader</p>
                        <span id="ytDuration" class="inline-block px-2.5 py-0.5 rounded text-[11px] font-bold bg-white/10 text-cyan-300">00:00</span>
                    </div>
                </div>

                <!-- Download Options Grid -->
                <div class="border-t border-white/10 pt-4 space-y-3">
                    <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider">Chọn Định Dạng Muốn Tải:</h4>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                        <!-- MP3 320k -->
                        <button onclick="downloadYtMedia('mp3', '320')" class="p-3.5 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 text-left transition flex items-center justify-between">
                            <div>
                                <p class="text-sm font-bold text-cyan-300">🎵 Audio MP3</p>
                                <p class="text-[11px] text-slate-400">320kbps High Quality</p>
                            </div>
                            <span class="text-lg">⬇</span>
                        </button>
                        <!-- WAV Lossless -->
                        <button onclick="downloadYtMedia('wav', '0')" class="p-3.5 rounded-xl bg-purple-500/10 hover:bg-purple-500/20 border border-purple-500/30 text-left transition flex items-center justify-between">
                            <div>
                                <p class="text-sm font-bold text-purple-300">🎵 Audio WAV</p>
                                <p class="text-[11px] text-slate-400">Studio Lossless 24-bit</p>
                            </div>
                            <span class="text-lg">⬇</span>
                        </button>
                        <!-- MP4 1080p -->
                        <button onclick="downloadYtMedia('mp4', '1080')" class="p-3.5 rounded-xl bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 text-left transition flex items-center justify-between">
                            <div>
                                <p class="text-sm font-bold text-blue-300">🎬 Video 1080p</p>
                                <p class="text-[11px] text-slate-400">Full HD Sắc Nét</p>
                            </div>
                            <span class="text-lg">⬇</span>
                        </button>
                        <!-- MP4 720p -->
                        <button onclick="downloadYtMedia('mp4', '720')" class="p-3.5 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 text-left transition flex items-center justify-between">
                            <div>
                                <p class="text-sm font-bold text-emerald-300">🎬 Video 720p</p>
                                <p class="text-[11px] text-slate-400">HD Chuẩn</p>
                            </div>
                            <span class="text-lg">⬇</span>
                        </button>
                        <!-- MP4 480p -->
                        <button onclick="downloadYtMedia('mp4', '480')" class="p-3.5 rounded-xl bg-yellow-500/10 hover:bg-yellow-500/20 border border-yellow-500/30 text-left transition flex items-center justify-between">
                            <div>
                                <p class="text-sm font-bold text-yellow-300">🎬 Video 480p</p>
                                <p class="text-[11px] text-slate-400">Tiết kiệm dung lượng</p>
                            </div>
                            <span class="text-lg">⬇</span>
                        </button>
                    </div>
                </div>

                <!-- Download Progress status -->
                <div id="ytDownloadStatus" class="hidden p-3 bg-cyan-500/10 border border-cyan-500/20 rounded-xl text-center text-xs text-cyan-300 animate-pulse">
                    Đang xử lý & tải tệp xuống máy... Vui lòng đợi trong giây lát!
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-white/5 py-4 text-center text-xs text-slate-500">
        Engineered with passion for LO • Powered by BS-RoFormer, UVR-BVE & yt-dlp
    </footer>

    <!-- Scripts -->
    <script>
        let selectedFile = null;
        let inputMode = 'file';
        let currentUrls = [];
        let audioTracks = [];
        let isPlaying = false;
        let soloIndex = -1;

        function switchTab(tab) {
            const stemsBtn = document.getElementById('tabStemsBtn');
            const dlBtn = document.getElementById('tabDownloaderBtn');
            const stemsContent = document.getElementById('tabStemsContent');
            const dlContent = document.getElementById('tabDownloaderContent');

            if (tab === 'stems') {
                stemsBtn.className = "px-5 py-2 rounded-lg text-sm font-bold transition flex items-center gap-2 bg-cyan-500/20 text-cyan-400 border border-cyan-500/30";
                dlBtn.className = "px-5 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 text-slate-400 hover:text-white";
                stemsContent.classList.remove('hidden');
                dlContent.classList.add('hidden');
            } else {
                dlBtn.className = "px-5 py-2 rounded-lg text-sm font-bold transition flex items-center gap-2 bg-cyan-500/20 text-cyan-400 border border-cyan-500/30";
                stemsBtn.className = "px-5 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 text-slate-400 hover:text-white";
                dlContent.classList.remove('hidden');
                stemsContent.classList.add('hidden');
            }
        }

        function setInputMode(mode) {
            inputMode = mode;
            const fileBtn = document.getElementById('modeFileBtn');
            const urlBtn = document.getElementById('modeUrlBtn');
            const fileBox = document.getElementById('fileUploadContainer');
            const urlBox = document.getElementById('urlInputContainer');

            if (mode === 'file') {
                fileBtn.className = "px-3.5 py-1.5 rounded-lg text-xs font-bold transition bg-cyan-500 text-slate-900";
                urlBtn.className = "px-3.5 py-1.5 rounded-lg text-xs font-bold transition bg-white/5 text-slate-400 hover:text-white border border-white/10";
                fileBox.classList.remove('hidden');
                urlBox.classList.add('hidden');
            } else {
                urlBtn.className = "px-3.5 py-1.5 rounded-lg text-xs font-bold transition bg-cyan-500 text-slate-900";
                fileBtn.className = "px-3.5 py-1.5 rounded-lg text-xs font-bold transition bg-white/5 text-slate-400 hover:text-white border border-white/10";
                urlBox.classList.remove('hidden');
                fileBox.classList.add('hidden');
            }
        }

        function selectPreset(preset) {
            document.querySelectorAll('.preset-card').forEach(c => c.classList.remove('preset-active'));
            const card = document.getElementById('preset_' + preset);
            if (card) card.classList.add('preset-active');

            const vModel = document.getElementById('vocalModel');
            const bModel = document.getElementById('backingModel');

            if (preset === 'karaoke') {
                vModel.value = "model_bs_roformer_ep_317_sdr_12.9755.ckpt";
                bModel.value = "UVR-BVE-4B_SN-44100-2.pth";
            } else if (preset === 'remix') {
                vModel.value = "model_bs_roformer_ep_317_sdr_12.9755.ckpt";
                bModel.value = "UVR-MDX-NET-Voc_FT.onnx";
            } else if (preset === 'backing') {
                vModel.value = "UVR-BVE-4B_SN-44100-2.pth";
                bModel.value = "UVR-BVE-4B_SN-44100-2.pth";
            } else if (preset === 'fast') {
                vModel.value = "UVR-MDX-NET-Voc_FT.onnx";
                bModel.value = "UVR-MDX-NET-Voc_FT.onnx";
            }
        }

        function handleFileSelect(e) {
            if (e.target.files.length > 0) {
                selectedFile = e.target.files[0];
                document.getElementById('fileName').innerText = selectedFile.name;
                document.getElementById('fileSize').innerText = (selectedFile.size / (1024 * 1024)).toFixed(2) + " MB";
                document.getElementById('dropZone').classList.add('hidden');
                document.getElementById('fileInfoBox').classList.remove('hidden');
                document.getElementById('fileInfoBox').classList.add('flex');
            }
        }

        function clearSelectedFile() {
            selectedFile = null;
            document.getElementById('audioInput').value = "";
            document.getElementById('dropZone').classList.remove('hidden');
            document.getElementById('fileInfoBox').classList.add('hidden');
            document.getElementById('fileInfoBox').classList.remove('flex');
        }

        async function startSeparation() {
            if (inputMode === 'file' && !selectedFile) {
                alert("Vui lòng chọn hoặc kéo thả 1 file bài hát trước!");
                return;
            }
            if (inputMode === 'url' && !document.getElementById('streamUrlInput').value.trim()) {
                alert("Vui lòng dán đường link bài hát!");
                return;
            }

            const btn = document.getElementById('submitBtn');
            const progress = document.getElementById('progressBox');
            const mixer = document.getElementById('mixerBox');
            const status = document.getElementById('statusText');
            const bar = document.getElementById('progressBar');

            btn.disabled = true;
            btn.innerHTML = `<span class="inline-block animate-spin mr-2">⏳</span> Đang bóc tách âm thanh...`;
            progress.classList.remove('hidden');
            mixer.classList.add('hidden');

            bar.style.width = "20%";
            status.innerText = inputMode === 'url' ? "Đang tải âm thanh từ link..." : "Đang tải file bài hát lên máy chủ...";

            try {
                let resp;
                if (inputMode === 'file') {
                    const formData = new FormData();
                    formData.append("file", selectedFile);
                    formData.append("vocal_model", document.getElementById('vocalModel').value);
                    formData.append("backing_model", document.getElementById('backingModel').value);

                    bar.style.width = "40%";
                    status.innerText = "Đang tách Beat & Vocal bằng BS-RoFormer...";

                    resp = await fetch('/api/separate', { method: 'POST', body: formData });
                } else {
                    const formData = new FormData();
                    formData.append("url", document.getElementById('streamUrlInput').value.trim());
                    formData.append("vocal_model", document.getElementById('vocalModel').value);
                    formData.append("backing_model", document.getElementById('backingModel').value);

                    bar.style.width = "30%";
                    status.innerText = "Đang trích xuất audio và chạy model tách nhạc...";

                    resp = await fetch('/api/separate-url', { method: 'POST', body: formData });
                }

                bar.style.width = "85%";
                status.innerText = "Đang phân tách Bè và hoàn tất Karaoke Mix...";

                const data = await resp.json();
                if (data.success) {
                    bar.style.width = "100%";
                    status.innerText = "Hoàn tất! Đang khởi động bàn Mixer...";
                    setTimeout(() => {
                        progress.classList.add('hidden');
                        initMixer(data);
                    }, 800);
                } else {
                    alert("Lỗi xử lý: " + (data.error || "Không thể tách bài hát này."));
                    progress.classList.add('hidden');
                }
            } catch (err) {
                alert("Lỗi kết nối máy chủ: " + err.message);
                progress.classList.add('hidden');
            } finally {
                btn.disabled = false;
                btn.innerHTML = `<span>⚡ Bắt Đầu Tách 3 Đường Tiếng</span>`;
            }
        }

        function initMixer(data) {
            currentUrls = [
                data.instrumental_url,
                data.lead_url,
                data.backing_url,
                data.karaoke_mix_url
            ];

            // Set download links
            for (let i = 0; i < 4; i++) {
                document.getElementById('download_' + i).href = currentUrls[i];
            }

            // Create Audio objects
            stopMasterPlay();
            audioTracks = currentUrls.map((url, idx) => {
                const a = new Audio(url);
                a.volume = idx === 3 ? 0 : 1; // Default Karaoke mix is silent unless desired
                return a;
            });

            audioTracks[0].ontimeupdate = () => {
                const curr = audioTracks[0].currentTime;
                const dur = audioTracks[0].duration || 1;
                document.getElementById('masterTimeline').value = (curr / dur) * 100;
                document.getElementById('timeDisplay').innerText = formatSeconds(curr) + " / " + formatSeconds(dur);
            };

            document.getElementById('mixerBox').classList.remove('hidden');
            document.getElementById('mixerBox').scrollIntoView({ behavior: 'smooth' });
        }

        function toggleMasterPlay() {
            if (!audioTracks.length) return;
            const btn = document.getElementById('masterPlayBtn');
            if (isPlaying) {
                audioTracks.forEach(a => a.pause());
                btn.innerText = "▶";
                isPlaying = false;
            } else {
                audioTracks.forEach(a => a.play());
                btn.innerText = "⏸";
                isPlaying = true;
            }
        }

        function stopMasterPlay() {
            audioTracks.forEach(a => {
                a.pause();
                a.currentTime = 0;
            });
            const btn = document.getElementById('masterPlayBtn');
            if (btn) btn.innerText = "▶";
            isPlaying = false;
        }

        function seekMaster(val) {
            if (!audioTracks.length) return;
            const dur = audioTracks[0].duration;
            if (dur) {
                const targetTime = (val / 100) * dur;
                audioTracks.forEach(a => a.currentTime = targetTime);
            }
        }

        function setChannelVolume(idx, vol) {
            if (audioTracks[idx]) {
                audioTracks[idx].volume = parseFloat(vol);
            }
        }

        function toggleMute(idx) {
            if (!audioTracks[idx]) return;
            const a = audioTracks[idx];
            const btn = document.getElementById('muteBtn_' + idx);
            a.muted = !a.muted;
            if (a.muted) {
                btn.classList.add('bg-red-500/20', 'text-red-400', 'border-red-500/30');
            } else {
                btn.classList.remove('bg-red-500/20', 'text-red-400', 'border-red-500/30');
            }
        }

        function toggleSolo(idx) {
            if (!audioTracks.length) return;
            const btn = document.getElementById('soloBtn_' + idx);
            if (soloIndex === idx) {
                // Turn off solo
                soloIndex = -1;
                audioTracks.forEach(a => a.muted = false);
                document.querySelectorAll('[id^="soloBtn_"]').forEach(b => b.classList.remove('bg-yellow-500', 'text-black'));
            } else {
                // Enable solo
                soloIndex = idx;
                audioTracks.forEach((a, i) => a.muted = (i !== idx));
                document.querySelectorAll('[id^="soloBtn_"]').forEach(b => b.classList.remove('bg-yellow-500', 'text-black'));
                btn.classList.add('bg-yellow-500', 'text-black');
            }
        }

        function formatSeconds(sec) {
            if (!sec || isNaN(sec)) return "00:00";
            const m = Math.floor(sec / 60);
            const s = Math.floor(sec % 60);
            return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
        }

        function downloadAllZip() {
            if (!currentUrls.length) return;
            const filenames = currentUrls.map(u => u.split('/').pop()).join(',');
            window.location.href = `/api/download-zip?stems=${encodeURIComponent(filenames)}`;
        }

        function resetApp() {
            stopMasterPlay();
            document.getElementById('mixerBox').classList.add('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // TAB 2: YOUTUBE DOWNLOADER
        let currentYtUrl = "";

        async function fetchYouTubeInfo() {
            const url = document.getElementById('ytUrlInput').value.trim();
            if (!url) {
                alert("Vui lòng dán link video YouTube!");
                return;
            }

            const loading = document.getElementById('ytLoading');
            const card = document.getElementById('ytInfoCard');
            loading.classList.remove('hidden');
            card.classList.add('hidden');

            try {
                const res = await fetch(`/api/yt-info?url=${encodeURIComponent(url)}`);
                const data = await res.json();
                if (data.success) {
                    currentYtUrl = url;
                    document.getElementById('ytThumb').src = data.thumbnail;
                    document.getElementById('ytTitle').innerText = data.title;
                    document.getElementById('ytUploader').innerText = "Kênh: " + data.uploader;
                    document.getElementById('ytDuration').innerText = "Thời lượng: " + data.duration;
                    card.classList.remove('hidden');
                } else {
                    alert("Không thể lấy thông tin video: " + (data.error || "Link không hợp lệ"));
                }
            } catch (err) {
                alert("Lỗi kết nối: " + err.message);
            } finally {
                loading.classList.add('hidden');
            }
        }

        function downloadYtMedia(format, quality) {
            if (!currentYtUrl) return;
            const status = document.getElementById('ytDownloadStatus');
            status.classList.remove('hidden');
            status.innerText = `Đang chuyển đổi và tải định dạng ${format.toUpperCase()} (${quality})...`;

            const downloadUrl = `/api/yt-download?url=${encodeURIComponent(currentYtUrl)}&format_type=${format}&quality=${quality}`;
            window.location.href = downloadUrl;

            setTimeout(() => {
                status.innerText = "Tệp đã được gửi đến trình duyệt của bạn!";
                setTimeout(() => status.classList.add('hidden'), 4000);
            }, 3000);
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_TEMPLATE

@app.post("/api/separate")
async def separate_audio_file(
    file: UploadFile = File(...),
    vocal_model: str = Form("model_bs_roformer_ep_317_sdr_12.9755.ckpt"),
    backing_model: str = Form("UVR-BVE-4B_SN-44100-2.pth")
):
    input_path = WORKSPACE / file.filename
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    results = engine.separate_3way(
        str(input_path),
        vocal_model=vocal_model,
        backing_model=backing_model
    )

    return {
        "success": True,
        "instrumental_url": f"/files/{Path(results['instrumental']).name}",
        "lead_url": f"/files/{Path(results['lead_vocals']).name}",
        "backing_url": f"/files/{Path(results['backing_vocals']).name}",
        "karaoke_mix_url": f"/files/{Path(results['karaoke_mix']).name}"
    }

@app.post("/api/separate-url")
async def separate_audio_url(
    url: str = Form(...),
    vocal_model: str = Form("model_bs_roformer_ep_317_sdr_12.9755.ckpt"),
    backing_model: str = Form("UVR-BVE-4B_SN-44100-2.pth")
):
    try:
        # Download audio stream as WAV
        wav_path = download_for_separation(url, WORKSPACE)
        results = engine.separate_3way(
            str(wav_path),
            vocal_model=vocal_model,
            backing_model=backing_model
        )
        return {
            "success": True,
            "instrumental_url": f"/files/{Path(results['instrumental']).name}",
            "lead_url": f"/files/{Path(results['lead_vocals']).name}",
            "backing_url": f"/files/{Path(results['backing_vocals']).name}",
            "karaoke_mix_url": f"/files/{Path(results['karaoke_mix']).name}"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.get("/api/yt-info")
async def yt_info(url: str = Query(...)):
    try:
        info = get_media_info(url)
        return {"success": True, **info}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

@app.get("/api/yt-download")
async def yt_download(
    url: str = Query(...),
    format_type: str = Query("mp3"),
    quality: str = Query("320")
):
    try:
        media_path = download_media_format(
            url,
            WORKSPACE,
            format_type=format_type,
            quality=quality
        )
        return FileResponse(media_path, filename=media_path.name)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/download-zip")
async def download_zip(stems: str = Query(...)):
    """
    Packages selected stem files into a single ZIP file for one-click studio download.
    """
    file_list = [f.strip() for f in stems.split(",") if f.strip()]
    zip_id = uuid.uuid4().hex[:6]
    zip_path = WORKSPACE / f"Stems_Pack_{zip_id}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for fname in file_list:
            fpath = WORKSPACE / fname
            if fpath.exists():
                zipf.write(fpath, arcname=fname)

    return FileResponse(zip_path, filename=f"Stems_Pack_{zip_id}.zip")

@app.get("/files/{filename}")
async def download_stem(filename: str):
    file_path = WORKSPACE / filename
    if file_path.exists():
        return FileResponse(file_path, filename=filename)
    return JSONResponse(status_code=404, content={"error": "File not found"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)
