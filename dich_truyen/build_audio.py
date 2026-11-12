#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động chuyển đổi các chương truyện dịch thành file Audio MP3 đọc truyện (Text-to-Speech)
Sử dụng Microsoft Edge Neural TTS chất lượng cao (giọng Nam / Nữ thuần Việt, truyền cảm)
Tự động ghép cứ mỗi 10 chương thành 1 file MP3 hoàn chỉnh bằng FFmpeg.
"""

import os
import re
import sys
import time
import shutil
import argparse
import subprocess
from pathlib import Path

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi mã hóa
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def natural_sort_key(s):
    """Sắp xếp chuỗi theo số tự nhiên (chuong_2 đứng trước chuong_10)."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]


def get_ffmpeg_exe():
    """Tìm binary ffmpeg từ imageio_ffmpeg hoặc trên PATH."""
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return exe
    except ImportError:
        pass
    
    # Kiểm tra trên PATH
    ffmpeg_on_path = shutil.which("ffmpeg")
    if ffmpeg_on_path:
        return ffmpeg_on_path
        
    return None


def clean_text_for_tts(text: str) -> str:
    """Làm sạch và tối ưu hóa văn bản để giọng đọc Neural ngắt nghỉ tự nhiên."""
    # Bỏ các ký hiệu markdown thừa
    text = re.sub(r'[*_#`~]', '', text)
    # Chuẩn hóa dấu ba chấm và dấu gạch đầu dòng
    text = re.sub(r'\.{3,}', '... ', text)
    text = re.sub(r'^[-\u2013\u2014]\s*', '', text, flags=re.M)
    # Đảm bảo dấu câu có khoảng trắng sau nó
    text = re.sub(r'([.,!?;:])([^\s\d])', r'\1 \2', text)
    # Xóa các dòng trống liên tiếp
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n\n'.join(lines)


def generate_single_chapter_audio(txt_path: Path, out_mp3: Path, voice: str = "vi-VN-NamMinhNeural", rate: str = "+0%"):
    """Tạo audio cho 1 chương truyện bằng edge-tts."""
    if out_mp3.exists() and out_mp3.stat().st_size > 1024:
        return True
        
    raw_text = txt_path.read_text(encoding="utf-8", errors="replace")
    cleaned_text = clean_text_for_tts(raw_text)
    
    # Ghi file tạm đã làm sạch
    temp_txt = out_mp3.parent / f"_temp_{txt_path.name}"
    temp_txt.write_text(cleaned_text, encoding="utf-8")
    
    try:
        cmd = [
            sys.executable, "-m", "edge_tts",
            "--file", str(temp_txt),
            "--voice", voice,
            "--rate", rate,
            "--write-media", str(out_mp3)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if res.returncode == 0 and out_mp3.exists() and out_mp3.stat().st_size > 1024:
            return True
        else:
            print(f"[Lỗi edge-tts] Chương {txt_path.name}: {res.stderr}")
            return False
    except Exception as e:
        print(f"[Ngoại lệ edge-tts] Chương {txt_path.name}: {e}")
        return False
    finally:
        if temp_txt.exists():
            try:
                temp_txt.unlink()
            except Exception:
                pass


def concat_mp3_files(mp3_files: list[Path], output_mp3: Path, ffmpeg_exe: str):
    """Ghép danh sách các file MP3 thành 1 file duy nhất bằng FFmpeg (lossless, nhanh tức thì)."""
    if not mp3_files:
        return False
        
    concat_list_file = output_mp3.parent / f"_concat_list_{output_mp3.stem}.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for mp3 in mp3_files:
            # Format chuẩn cho ffmpeg concat demuxer: file 'path'
            clean_path = str(mp3.resolve()).replace('\\', '/')
            f.write(f"file '{clean_path}'\n")
            
    try:
        cmd = [
            ffmpeg_exe, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_file),
            "-c", "copy",
            str(output_mp3)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if res.returncode == 0 and output_mp3.exists() and output_mp3.stat().st_size > 1024:
            return True
        else:
            print(f"[Lỗi FFmpeg Concat]: {res.stderr}")
            return False
    except Exception as e:
        print(f"[Ngoại lệ FFmpeg]: {e}")
        return False
    finally:
        if concat_list_file.exists():
            try:
                concat_list_file.unlink()
            except Exception:
                pass


def build_audio_batches(novel_dir: Path, group_size: int = 10, voice: str = "vi-VN-NamMinhNeural", 
                        rate: str = "+0%", target_batch: int = None, force: bool = False):
    """Xử lý tạo audio hàng loạt theo từng cụm 10 chương."""
    novel_dir = Path(novel_dir)
    chuong_dir = novel_dir / "chuong"
    if not chuong_dir.exists():
        print(f"[Lỗi] Không tìm thấy thư mục chương: {chuong_dir}")
        return
        
    audio_dir = novel_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    cache_dir = novel_dir / "temp_audio" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    ffmpeg_exe = get_ffmpeg_exe()
    if not ffmpeg_exe:
        print("[Lỗi] Không tìm thấy FFmpeg! Hãy cài đặt imageio-ffmpeg hoặc thêm ffmpeg vào PATH.")
        return
        
    # Lấy danh sách các chương txt theo thứ tự tự nhiên
    all_chapters = sorted([f for f in chuong_dir.glob("*.txt")], key=natural_sort_key)
    total_chapters = len(all_chapters)
    print(f"=== KHỞI ĐỘNG HỆ THỐNG AUDIO TTS TRUYỆN ===")
    print(f"Truyện: {novel_dir.name}")
    print(f"Tổng số chương đã dịch: {total_chapters}")
    print(f"Giọng đọc: {voice} (Tốc độ: {rate})")
    print(f"Quy cách ghép: {group_size} chương / 1 file MP3")
    print(f"Thư mục xuất audio: {audio_dir}")
    print("-" * 50)
    
    # Chia danh sách chương thành các nhóm group_size
    batches = []
    for i in range(0, total_chapters, group_size):
        chunk = all_chapters[i:i + group_size]
        batches.append(chunk)
        
    print(f"Tổng cộng có {len(batches)} cụm audio cần xử lý.")
    
    for b_idx, batch_chapters in enumerate(batches, start=1):
        if target_batch is not None and b_idx != target_batch:
            continue
            
        start_num = int(re.search(r'\d+', batch_chapters[0].name).group())
        end_num = int(re.search(r'\d+', batch_chapters[-1].name).group())
        
        batch_filename = f"audio_chuong_{start_num:03d}_{end_num:03d}.mp3"
        batch_output_file = audio_dir / batch_filename
        
        if batch_output_file.exists() and not force:
            print(f"[Đã có sẵn] Cụm {b_idx}: Chương {start_num} - {end_num} ({batch_filename}) -> Bỏ qua.")
            continue
            
        print(f"\n>>> ĐANG XỬ LÝ CỤM {b_idx}/{len(batches)}: Chương {start_num} đến Chương {end_num}...")
        t0 = time.time()
        
        batch_mp3_files = []
        success = True
        
        for c_idx, chap_file in enumerate(batch_chapters, start=1):
            chap_mp3 = cache_dir / f"{chap_file.stem}.mp3"
            print(f"  [{c_idx}/{len(batch_chapters)}] Đang đọc audio: {chap_file.name}...", end="", flush=True)
            t_chap = time.time()
            ok = generate_single_chapter_audio(chap_file, chap_mp3, voice=voice, rate=rate)
            if ok:
                size_mb = chap_mp3.stat().st_size / (1024 * 1024)
                print(f" Xong ({time.time() - t_chap:.1f}s, {size_mb:.2f} MB)")
                batch_mp3_files.append(chap_mp3)
            else:
                print(" THẤT BẠI!")
                success = False
                break
                
        if not success:
            print(f"[Cảnh báo] Cụm {b_idx} bị lỗi ở một số chương, không thể ghép file MP3 chung.")
            continue
            
        # Ghép thành 1 file MP3 chung cho 10 chương
        print(f"  -> Đang ghép {len(batch_mp3_files)} chương vào file tổng hợp: {batch_filename}...")
        if concat_mp3_files(batch_mp3_files, batch_output_file, ffmpeg_exe):
            total_size_mb = batch_output_file.stat().st_size / (1024 * 1024)
            print(f"  [THÀNH CÔNG] Đã tạo: {batch_output_file.name} ({total_size_mb:.2f} MB, {time.time() - t0:.1f}s)")
        else:
            print(f"  [THẤT BẠI] Lỗi ghép file cho cụm {b_idx}!")
            
    print("\n=== HOÀN TẤT XỬ LÝ AUDIO ===")


def main():
    parser = argparse.ArgumentParser(description="Tạo file Audio MP3 đọc truyện (10 chương / file) bằng Edge TTS")
    parser.add_argument("novel_dir", help="Thư mục truyện (ví dụ: dich_truyen/ta_ba_xa_la_minh_tinh)")
    parser.add_argument("--group", type=int, default=10, help="Số chương gộp vào 1 file audio (mặc định: 10)")
    parser.add_argument("--voice", default="vi-VN-NamMinhNeural", 
                        choices=["vi-VN-NamMinhNeural", "vi-VN-HoaiMyNeural"], 
                        help="Giọng đọc tiếng Việt (NamMinh: Nam, HoaiMy: Nữ)")
    parser.add_argument("--rate", default="+0%", help="Tốc độ đọc (ví dụ: +5%%, +10%%, -5%%)")
    parser.add_argument("--batch", type=int, default=None, help="Chỉ xử lý cụm số X (ví dụ: 1 cho chương 1-10)")
    parser.add_argument("--force", action="store_true", help="Ghi đè file audio cũ nếu đã tồn tại")
    
    args = parser.parse_args()
    build_audio_batches(
        novel_dir=Path(args.novel_dir),
        group_size=args.group,
        voice=args.voice,
        rate=args.rate,
        target_batch=args.batch,
        force=args.force
    )


if __name__ == "__main__":
    main()
