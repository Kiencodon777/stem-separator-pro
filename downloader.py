"""
YouTube / Web Media Downloader Module for Stem Separator Pro
Uses yt-dlp and FFmpeg to download and convert audio/video in various formats.
"""

import os
import sys
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
import yt_dlp

# Ensure FFmpeg is in PATH
FFMPEG_DIR = r"C:\Users\anhan\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
if os.path.exists(FFMPEG_DIR) and FFMPEG_DIR not in os.environ.get("PATH", ""):
    os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ["PATH"]


def get_media_info(url: str) -> Dict[str, Any]:
    """
    Extracts video metadata without downloading.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "ffmpeg_location": FFMPEG_DIR if os.path.exists(FFMPEG_DIR) else None
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        duration = info.get("duration", 0)
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        return {
            "title": info.get("title", "Unknown Title"),
            "uploader": info.get("uploader", "Unknown Artist"),
            "thumbnail": info.get("thumbnail", ""),
            "duration": f"{minutes:02d}:{seconds:02d}",
            "duration_sec": duration,
            "url": url
        }


def download_for_separation(url: str, output_dir: Path) -> Path:
    """
    Downloads media and converts to clean 44.1kHz 16-bit WAV for stem separation.
    """
    file_id = uuid.uuid4().hex[:8]
    output_template = str(output_dir / f"{file_id}.%(ext)s")
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
        "no_warnings": True,
        "ffmpeg_location": FFMPEG_DIR if os.path.exists(FFMPEG_DIR) else None,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "0",
        }]
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    wav_path = output_dir / f"{file_id}.wav"
    if not wav_path.exists():
        # Look for any file matching file_id
        matches = list(output_dir.glob(f"{file_id}*"))
        if matches:
            return matches[0]
        raise RuntimeError("Failed to download audio from URL.")
        
    return wav_path


def download_media_format(
    url: str,
    output_dir: Path,
    format_type: str = "mp3",
    quality: str = "320"
) -> Path:
    """
    Downloads video/audio in specific format:
    - format_type = 'mp3' (quality: 320, 256, 128)
    - format_type = 'wav' (studio quality)
    - format_type = 'mp4' (quality: 1080, 720, 480)
    """
    file_id = uuid.uuid4().hex[:8]
    
    if format_type in ["mp3", "wav"]:
        output_template = str(output_dir / f"download_{file_id}.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "ffmpeg_location": FFMPEG_DIR if os.path.exists(FFMPEG_DIR) else None,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": format_type,
                "preferredquality": quality if format_type == "mp3" else None,
            }]
        }
    else:  # MP4 video
        res = quality if quality in ["1080", "720", "480", "360"] else "720"
        output_template = str(output_dir / f"download_{file_id}.%(ext)s")
        ydl_opts = {
            "format": f"bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/best[height<={res}]/best",
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "ffmpeg_location": FFMPEG_DIR if os.path.exists(FFMPEG_DIR) else None,
            "merge_output_format": "mp4"
        }
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
    # Find generated file
    target_ext = "wav" if format_type == "wav" else ("mp3" if format_type == "mp3" else "mp4")
    expected_path = output_dir / f"download_{file_id}.{target_ext}"
    if expected_path.exists():
        return expected_path
        
    matches = list(output_dir.glob(f"download_{file_id}*"))
    if matches:
        return matches[0]
        
    return Path(filename)
