#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động tổng hợp các chương truyện (.txt) thành một file HTML đọc truyện độc lập (offline-first).
Giao diện hiện đại, hỗ trợ Chế độ Sáng / Tối / Giấy Cũ (Sepia), tăng giảm cỡ chữ, mục lục trượt,
lưu vị trí đọc tự động vào trình duyệt.
"""

import os
import re
import sys
import html
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


def parse_novel_meta(novel_dir: Path):
    """Trích xuất thông tin truyện từ ho_so_dich_thuat.md nếu có."""
    meta = {
        "title": novel_dir.name.replace("_", " ").title(),
        "author": "Đang cập nhật",
        "genre": "Tiểu thuyết",
        "original_title": "",
        "translator": "Trợ lý Antigravity"
    }
    
    ho_so_file = novel_dir / "ho_so_dich_thuat.md"
    if ho_so_file.exists():
        try:
            content = ho_so_file.read_text(encoding="utf-8")
            # Tên tiếng Việt
            m = re.search(r"\*\*Tên tiếng Việt:\*\*\s*(.+)", content)
            if m:
                meta["title"] = m.group(1).strip()
            else:
                m_h1 = re.search(r"^#\s+HỒ SƠ DỊCH THUẬT:\s*(.+)", content, re.M)
                if m_h1:
                    meta["title"] = m_h1.group(1).strip()
            
            # Tên tiếng Trung
            m_cn = re.search(r"\*\*Tên tiếng Trung.*:\*\*\s*(.+)", content)
            if m_cn:
                meta["original_title"] = m_cn.group(1).strip()
                
            # Tác giả
            m_au = re.search(r"\*\*Tác giả:\*\*\s*(.+)", content)
            if m_au:
                meta["author"] = m_au.group(1).strip()
                
            # Thể loại
            m_gen = re.search(r"\*\*Thể loại:\*\*\s*(.+)", content)
            if m_gen:
                meta["genre"] = m_gen.group(1).strip()
        except Exception as e:
            print(f"[Cảnh báo] Không thể đọc chi tiết ho_so_dich_thuat.md: {e}")
            
    return meta


def parse_chapter_file(file_path: Path):
    """Đọc file txt chương và tách tiêu đề + các đoạn văn."""
    raw_text = file_path.read_text(encoding="utf-8", errors="replace").strip()
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    
    if not lines:
        return {"title": file_path.stem, "paragraphs": []}
    
    # Dòng đầu tiên thường là "Chương X: [Tên chương]"
    first_line = lines[0]
    if re.match(r"^chương\s+\d+", first_line, re.IGNORECASE):
        chapter_title = first_line
        body_lines = lines[1:]
    else:
        chapter_title = f"{file_path.stem} - {first_line}"
        body_lines = lines[1:]
        
    return {
        "title": chapter_title,
        "paragraphs": body_lines
    }


def generate_reader_html(novel_dir: Path, output_file: Path = None):
    """Biên tập toàn bộ chương trong chuong/ thành file HTML đọc truyện."""
    chuong_dir = novel_dir / "chuong"
    if not chuong_dir.exists():
        print(f"[Lỗi] Không tìm thấy thư mục: {chuong_dir}")
        return False
        
    txt_files = sorted(list(chuong_dir.glob("*.txt")), key=lambda p: natural_sort_key(p.name))
    if not txt_files:
        print(f"[Thông báo] Chưa có file .txt nào trong {chuong_dir}")
        return False
        
    meta = parse_novel_meta(novel_dir)
    if output_file is None:
        output_file = novel_dir / "doc_truyen.html"
        
    chapters = []
    for idx, f in enumerate(txt_files, start=1):
        parsed = parse_chapter_file(f)
        chapters.append({
            "id": f"chap_{idx}",
            "index": idx,
            "filename": f.name,
            "title": parsed["title"],
            "paragraphs": parsed["paragraphs"]
        })

    # Render HTML
    html_content = render_template(meta, chapters)
    output_file.write_text(html_content, encoding="utf-8")
    print(f"[Thành công] Đã biên tập {len(chapters)} chương vào: {output_file.resolve()}")
    return True


def render_template(meta, chapters):
    """Tạo chuỗi HTML hoàn chỉnh."""
    toc_items_html = []
    chapters_html = []
    
    total_chaps = len(chapters)
    
    for c in chapters:
        idx = c["index"]
        c_id = c["id"]
        c_title_escaped = html.escape(c["title"])
        
        # TOC link
        toc_items_html.append(f"""
            <a href="#{c_id}" class="toc-item" data-chap="{idx}" onclick="closeSidebarOnMobile()">
                <span class="toc-num">{idx}</span>
                <span class="toc-text">{c_title_escaped}</span>
            </a>
        """)
        
        # Paragraphs formatting & highlight [CẦN KIỂM TRA]
        p_elements = []
        for p in c["paragraphs"]:
            p_esc = html.escape(p)
            if "[CẦN KIỂM TRA]" in p_esc:
                p_esc = p_esc.replace("[CẦN KIỂM TRA]", '<span class="needs-check">[CẦN KIỂM TRA]</span>')
            p_elements.append(f"<p>{p_esc}</p>")
            
        body_p = "\n".join(p_elements)
        
        # Navigation buttons
        prev_btn = f'<a href="#chap_{idx-1}" class="btn-nav">← Chương trước</a>' if idx > 1 else '<span class="btn-nav disabled">← Chương trước</span>'
        next_btn = f'<a href="#chap_{idx+1}" class="btn-nav">Chương sau →</a>' if idx < total_chaps else '<span class="btn-nav disabled">Hết chương mới nhất</span>'
        
        chapters_html.append(f"""
        <article class="chapter-card" id="{c_id}" data-index="{idx}">
            <header class="chapter-header">
                <div class="chap-badge">Chương {idx} / {total_chaps}</div>
                <h2 class="chapter-title">{c_title_escaped}</h2>
                <div class="chapter-top-nav">
                    {prev_btn}
                    <button class="btn-nav" onclick="openSidebar()">☰ Mục lục</button>
                    {next_btn}
                </div>
            </header>
            <div class="chapter-body">
                {body_p}
            </div>
            <footer class="chapter-footer">
                <div class="chapter-bot-nav">
                    {prev_btn}
                    <a href="#top" class="btn-nav" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">↑ Đầu trang</a>
                    {next_btn}
                </div>
            </footer>
        </article>
        """)

    toc_str = "\n".join(toc_items_html)
    chapters_str = "\n".join(chapters_html)
    
    title_escaped = html.escape(meta["title"])
    author_escaped = html.escape(meta["author"])
    genre_escaped = html.escape(meta["genre"])
    orig_escaped = html.escape(meta.get("original_title", ""))

    return f"""<!DOCTYPE html>
<html lang="vi" data-theme="sepia" data-font="serif">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_escaped} - Đọc Truyện Bản Dịch</title>
    <style>
        :root {{
            --font-serif: "Merriweather", "Charter", "Georgia", "Times New Roman", serif;
            --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --base-font-size: 19px;
            --line-height: 1.85;
            --max-read-width: 780px;
        }}

        /* Theme: Sepia (Mặc định cho trải nghiệm đọc êm dịu) */
        html[data-theme="sepia"] {{
            --bg-color: #f7f3e9;
            --surface-color: #eee7d7;
            --card-bg: #fdfaf2;
            --text-color: #382f2d;
            --text-muted: #7b6f68;
            --border-color: #dfd5c3;
            --accent-color: #9c4221;
            --accent-hover: #b8522e;
            --highlight-bg: #fff0b3;
            --highlight-border: #d4a017;
        }}

        /* Theme: Sáng */
        html[data-theme="light"] {{
            --bg-color: #f9fafb;
            --surface-color: #f3f4f6;
            --card-bg: #ffffff;
            --text-color: #1f2937;
            --text-muted: #6b7280;
            --border-color: #e5e7eb;
            --accent-color: #1d4ed8;
            --accent-hover: #2563eb;
            --highlight-bg: #fef08a;
            --highlight-border: #ca8a04;
        }}

        /* Theme: Tối (Dark mode) */
        html[data-theme="dark"] {{
            --bg-color: #121417;
            --surface-color: #1c1f24;
            --card-bg: #181b20;
            --text-color: #d1d5db;
            --text-muted: #9ca3af;
            --border-color: #2e3440;
            --accent-color: #38bdf8;
            --accent-hover: #7dd3fc;
            --highlight-bg: #713f12;
            --highlight-border: #eab308;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: var(--font-serif);
            font-size: var(--base-font-size);
            line-height: var(--line-height);
            transition: background-color 0.25s ease, color 0.25s ease;
            -webkit-font-smoothing: antialiased;
        }}

        html[data-font="sans"] body {{
            font-family: var(--font-sans);
        }}

        /* Progress Bar */
        #read-progress {{
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: var(--accent-color);
            width: 0%;
            z-index: 9999;
            transition: width 0.1s linear;
        }}

        /* Header / Navbar */
        .reader-navbar {{
            position: sticky;
            top: 0;
            z-index: 1000;
            background: var(--surface-color);
            border-bottom: 1px solid var(--border-color);
            backdrop-filter: blur(10px);
            padding: 8px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .nav-left, .nav-right {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .btn-icon {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: all 0.2s;
        }}

        .btn-icon:hover {{
            background: var(--card-bg);
            border-color: var(--accent-color);
            color: var(--accent-color);
        }}

        .novel-mini-title {{
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 320px;
        }}

        /* Control Popover */
        .theme-select, .font-select {{
            padding: 5px 8px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            background: var(--card-bg);
            color: var(--text-color);
            font-size: 13px;
            cursor: pointer;
        }}

        /* Sidebar / TOC Drawer */
        .sidebar-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0,0,0,0.4);
            z-index: 2000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }}

        .sidebar-overlay.active {{
            opacity: 1;
            pointer-events: auto;
        }}

        .sidebar-drawer {{
            position: fixed;
            top: 0;
            left: 0;
            width: 340px;
            max-width: 85vw;
            height: 100vh;
            background: var(--surface-color);
            border-right: 1px solid var(--border-color);
            z-index: 2001;
            transform: translateX(-100%);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            box-shadow: 4px 0 20px rgba(0,0,0,0.15);
        }}

        .sidebar-drawer.active {{
            transform: translateX(0);
        }}

        .sidebar-header {{
            padding: 16px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .sidebar-header h3 {{
            font-size: 16px;
            font-family: var(--font-sans);
            font-weight: 700;
        }}

        .sidebar-search {{
            padding: 10px 16px;
            border-bottom: 1px solid var(--border-color);
        }}

        .sidebar-search input {{
            width: 100%;
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            background: var(--card-bg);
            color: var(--text-color);
            font-size: 13px;
        }}

        .sidebar-toc-list {{
            flex: 1;
            overflow-y: auto;
            padding: 8px 0;
        }}

        .toc-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 16px;
            text-decoration: none;
            color: var(--text-color);
            font-size: 14px;
            font-family: var(--font-sans);
            border-bottom: 1px solid rgba(0,0,0,0.03);
            transition: background 0.15s;
        }}

        .toc-item:hover, .toc-item.current {{
            background: var(--card-bg);
            color: var(--accent-color);
            font-weight: 600;
        }}

        .toc-num {{
            font-size: 12px;
            opacity: 0.6;
            min-width: 24px;
        }}

        /* Main Container */
        .container {{
            max-width: var(--max-read-width);
            margin: 0 auto;
            padding: 30px 20px 80px 20px;
        }}

        /* Hero / Novel Info Card */
        .novel-hero {{
            text-align: center;
            padding: 40px 20px 50px 20px;
            border-bottom: 2px dashed var(--border-color);
            margin-bottom: 40px;
        }}

        .novel-hero h1 {{
            font-size: 32px;
            font-weight: 800;
            color: var(--accent-color);
            margin-bottom: 8px;
            line-height: 1.3;
        }}

        .novel-hero .orig-title {{
            font-size: 16px;
            color: var(--text-muted);
            margin-bottom: 16px;
            font-style: italic;
        }}

        .novel-meta-tags {{
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 12px;
        }}

        .meta-tag {{
            font-size: 13px;
            font-family: var(--font-sans);
            padding: 4px 12px;
            border-radius: 999px;
            background: var(--surface-color);
            border: 1px solid var(--border-color);
        }}

        /* Chapter Card */
        .chapter-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 45px 36px;
            margin-bottom: 50px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }}

        @media (max-width: 640px) {{
            .chapter-card {{
                padding: 24px 16px;
                border-radius: 8px;
            }}
            .novel-hero h1 {{
                font-size: 24px;
            }}
            .novel-mini-title {{
                max-width: 140px;
            }}
        }}

        .chap-badge {{
            display: inline-block;
            font-size: 12px;
            font-family: var(--font-sans);
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }}

        .chapter-title {{
            font-size: 24px;
            font-weight: 700;
            line-height: 1.4;
            color: var(--accent-color);
            margin-bottom: 20px;
            text-align: center;
        }}

        .chapter-top-nav, .chapter-bot-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin: 20px 0 30px 0;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }}

        .chapter-bot-nav {{
            margin-top: 40px;
            margin-bottom: 0;
            border-bottom: none;
            padding-top: 24px;
            border-top: 1px solid var(--border-color);
        }}

        .btn-nav {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-family: var(--font-sans);
            font-size: 13px;
            padding: 8px 14px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            background: var(--surface-color);
            color: var(--text-color);
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .btn-nav:hover:not(.disabled) {{
            border-color: var(--accent-color);
            color: var(--accent-color);
        }}

        .btn-nav.disabled {{
            opacity: 0.4;
            cursor: not-allowed;
            pointer-events: none;
        }}

        /* Chapter Body Typography */
        .chapter-body p {{
            margin-bottom: 1.4em;
            text-indent: 1.6em;
            text-align: justify;
            text-justify: inter-word;
            word-break: break-word;
        }}

        .needs-check {{
            background: var(--highlight-bg);
            border-bottom: 2px dashed var(--highlight-border);
            padding: 0 4px;
            font-weight: 600;
            border-radius: 3px;
        }}
    </style>
</head>
<body id="top">

    <div id="read-progress"></div>

    <!-- Navigation Header -->
    <header class="reader-navbar">
        <div class="nav-left">
            <button class="btn-icon" onclick="openSidebar()" title="Mục lục chương">
                ☰ <span style="font-family: var(--font-sans);">Mục lục</span>
            </button>
            <span class="novel-mini-title" title="{title_escaped}">{title_escaped}</span>
        </div>
        <div class="nav-right">
            <!-- Font Style -->
            <select class="font-select" id="fontSelect" onchange="changeFont(this.value)" title="Kiểu phông">
                <option value="serif">Có chân (Serif)</option>
                <option value="sans">Không chân (Sans)</option>
            </select>
            <!-- Theme -->
            <select class="theme-select" id="themeSelect" onchange="changeTheme(this.value)" title="Chế độ màu">
                <option value="sepia">📖 Giấy Cũ</option>
                <option value="light">☀️ Sáng</option>
                <option value="dark">🌙 Tối</option>
            </select>
            <!-- Font size -->
            <button class="btn-icon" onclick="adjustFontSize(-1)" title="Giảm cỡ chữ">A-</button>
            <button class="btn-icon" onclick="adjustFontSize(1)" title="Tăng cỡ chữ">A+</button>
        </div>
    </header>

    <!-- Sidebar Overlay & Drawer -->
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="closeSidebar()"></div>
    <aside class="sidebar-drawer" id="sidebarDrawer">
        <div class="sidebar-header">
            <h3>Danh Sách Chương ({total_chaps})</h3>
            <button class="btn-icon" onclick="closeSidebar()">✕</button>
        </div>
        <div class="sidebar-search">
            <input type="text" id="searchInput" placeholder="Tìm theo tên hoặc số chương..." oninput="filterChapters(this.value)">
        </div>
        <div class="sidebar-toc-list" id="tocList">
            {toc_str}
        </div>
    </aside>

    <!-- Novel Main Content -->
    <main class="container">
        <!-- Novel Hero Section -->
        <section class="novel-hero">
            <h1>{title_escaped}</h1>
            {f'<div class="orig-title">Nguyên tác: {orig_escaped}</div>' if orig_escaped else ''}
            <div class="novel-meta-tags">
                <span class="meta-tag">✍️ Tác giả: <strong>{author_escaped}</strong></span>
                <span class="meta-tag">🏷️ Thể loại: <strong>{genre_escaped}</strong></span>
                <span class="meta-tag">📚 Tổng số: <strong>{total_chaps} chương đã dịch</strong></span>
            </div>
        </section>

        <!-- Chapter Contents -->
        <section class="chapters-container">
            {chapters_str}
        </section>
    </main>

    <script>
        // Reading Progress Bar
        window.addEventListener('scroll', () => {{
            const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById("read-progress").style.width = scrolled + "%";
            saveCurrentScroll();
        }});

        // Sidebar Drawer
        function openSidebar() {{
            document.getElementById('sidebarOverlay').classList.add('active');
            document.getElementById('sidebarDrawer').classList.add('active');
            document.getElementById('searchInput').focus();
        }}

        function closeSidebar() {{
            document.getElementById('sidebarOverlay').classList.remove('active');
            document.getElementById('sidebarDrawer').classList.remove('active');
        }}

        function closeSidebarOnMobile() {{
            if (window.innerWidth <= 768) {{
                closeSidebar();
            }}
        }}

        function filterChapters(query) {{
            const q = query.toLowerCase().trim();
            const items = document.querySelectorAll('.toc-item');
            items.forEach(item => {{
                const text = item.innerText.toLowerCase();
                item.style.display = text.includes(q) ? 'flex' : 'none';
            }});
        }}

        // Theme Switch
        function changeTheme(theme) {{
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('dich_truyen_theme', theme);
            document.getElementById('themeSelect').value = theme;
        }}

        // Font Switch
        function changeFont(font) {{
            document.documentElement.setAttribute('data-font', font);
            localStorage.setItem('dich_truyen_font', font);
            document.getElementById('fontSelect').value = font;
        }}

        // Font Size Adjust
        let currentFontSize = 19;
        function adjustFontSize(delta) {{
            currentFontSize = Math.min(28, Math.max(14, currentFontSize + delta));
            document.documentElement.style.setProperty('--base-font-size', currentFontSize + 'px');
            localStorage.setItem('dich_truyen_font_size', currentFontSize);
        }}

        // Save & Restore Settings
        (function initSettings() {{
            const savedTheme = localStorage.getItem('dich_truyen_theme') || 'sepia';
            changeTheme(savedTheme);

            const savedFont = localStorage.getItem('dich_truyen_font') || 'serif';
            changeFont(savedFont);

            const savedSize = localStorage.getItem('dich_truyen_font_size');
            if (savedSize) {{
                currentFontSize = parseInt(savedSize, 10);
                document.documentElement.style.setProperty('--base-font-size', currentFontSize + 'px');
            }}
        }})();

        // Memory of last read location
        function saveCurrentScroll() {{
            const chapters = document.querySelectorAll('.chapter-card');
            let currentId = null;
            chapters.forEach(c => {{
                const rect = c.getBoundingClientRect();
                if (rect.top <= 200 && rect.bottom >= 200) {{
                    currentId = c.id;
                }}
            }});
            if (currentId) {{
                localStorage.setItem('dich_truyen_last_chap', currentId);
            }}
        }}
    </script>
</body>
</html>
"""


def main():
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
        if target_dir.exists() and (target_dir / "chuong").exists():
            generate_reader_html(target_dir)
            return
        elif target_dir.exists() and target_dir.name == "chuong":
            generate_reader_html(target_dir.parent)
            return
            
    # Tự động quét các thư mục con trong dich_truyen
    base_dir = Path(__file__).resolve().parent
    found = False
    for sub in base_dir.iterdir():
        if sub.is_dir() and (sub / "chuong").exists():
            print(f"[*] Đang biên tập truyện tại: {sub.name}")
            generate_reader_html(sub)
            found = True
            
    if not found:
        print("[*] Hướng dẫn: Đặt các file chương dạng .txt vào: dich_truyen/<ten_truyen>/chuong/")
        print("    Sau đó chạy: python dich_truyen/build_html.py dich_truyen/<ten_truyen>")


if __name__ == "__main__":
    main()
