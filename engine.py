"""
Stem Separator Pro Engine:
High-Precision 3-Way Audio Separation:
1. Instrumental (Beat sạch không giọng hát)
2. Lead Vocals (Giọng hát chính của ca sĩ)
3. Backing Vocals (Giọng bè, hòa âm phụ họa)
4. Karaoke Mix (Beat + Giọng bè)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

# Ensure FFmpeg is in PATH
FFMPEG_DIR = r"C:\Users\anhan\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
if os.path.exists(FFMPEG_DIR) and FFMPEG_DIR not in os.environ.get("PATH", ""):
    os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ["PATH"]


class StemSeparatorPro:
    def __init__(self, work_dir: str = "workspace"):
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def separate_3way(
        self,
        audio_file: str,
        vocal_model: str = "model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        backing_model: str = "UVR-BVE-4B_SN-44100-2.pth"
    ) -> Dict[str, str]:
        """
        Runs 2-stage professional separation:
        Stage 1: Separate Audio -> Instrumental + Total Vocals (using BS-RoFormer)
        Stage 2: Separate Total Vocals -> Lead Vocals + Backing Vocals (using UVR BVE MDX-Net)
        Stage 3: Merge Instrumental + Backing Vocals -> Karaoke Mix
        """
        from audio_separator.separator import Separator

        print(f"[Stage 1] Separating Instrumental and Vocals using {vocal_model}...")
        sep_stage1 = Separator(
            output_dir=str(self.work_dir),
            output_format="WAV",
            log_level=20
        )
        sep_stage1.load_model(model_filename=vocal_model)
        stage1_files = sep_stage1.separate(audio_file)

        inst_path = None
        total_vocals_path = None
        for f in stage1_files:
            p = str(self.work_dir / f)
            if "Instrumental" in f or "inst" in f.lower():
                inst_path = p
            elif "Vocals" in f or "vocal" in f.lower():
                total_vocals_path = p

        if not inst_path or not total_vocals_path:
            raise RuntimeError("Stage 1 separation failed to produce both instrumental and vocals.")

        print(f"[Stage 2] Separating Lead and Backing Vocals using {backing_model}...")
        sep_stage2 = Separator(
            output_dir=str(self.work_dir),
            output_format="WAV",
            log_level=20
        )
        sep_stage2.load_model(model_filename=backing_model)
        stage2_files = sep_stage2.separate(total_vocals_path)

        lead_path = None
        backing_path = None
        for f in stage2_files:
            p = str(self.work_dir / f)
            # In UVR_BVE_MDX_Net:
            # Stems are usually (Instrumental) -> Backing Vocals, (Vocals) -> Lead Vocals
            if "Instrumental" in f or "backing" in f.lower() or "bve" in f.lower():
                backing_path = p
            elif "Vocals" in f or "lead" in f.lower():
                lead_path = p

        # Robust Fallback if naming is unexpected
        if (not backing_path or not lead_path) and len(stage2_files) >= 2:
            if not backing_path:
                backing_path = str(self.work_dir / stage2_files[0])
            if not lead_path:
                lead_path = str(self.work_dir / stage2_files[1])
        elif len(stage2_files) == 1:
            lead_path = str(self.work_dir / stage2_files[0])
            backing_path = total_vocals_path

        print(f"[Stage 3] Merging Instrumental + Backing Vocals for Professional Karaoke...")
        stem_name = Path(audio_file).stem
        karaoke_mix_path = str(self.work_dir / f"{stem_name}_(Karaoke_Beat_Plus_Backing).wav")

        # Mix with FFmpeg (amix filter)
        cmd = [
            "ffmpeg",
            "-y",
            "-i", inst_path,
            "-i", backing_path,
            "-filter_complex", "amix=inputs=2:duration=first:dropout_transition=2",
            karaoke_mix_path
        ]
        subprocess.run(cmd, check=True)

        return {
            "instrumental": inst_path,
            "lead_vocals": lead_path,
            "backing_vocals": backing_path,
            "karaoke_mix": karaoke_mix_path
        }
