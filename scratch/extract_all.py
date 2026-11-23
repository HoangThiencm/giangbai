import docx, os, json

def inspect_doc(path, out_txt):
    doc = docx.Document(path)
    lines = []
    lines.append(f"TOTAL PARAGRAPHS: {len(doc.paragraphs)}")
    lines.append(f"TOTAL TABLES: {len(doc.tables)}")
    
    # Extract images
    img_dir = out_txt + "_images"
    os.makedirs(img_dir, exist_ok=True)
    img_idx = 0
    for rel_id, rel in doc.part.rels.items():
        if "image" in rel.target_ref:
            img_data = rel.target_part.blob
            ext = rel.target_ref.split('.')[-1]
            img_path = os.path.join(img_dir, f"img_{img_idx}.{ext}")
            with open(img_path, "wb") as f_img:
                f_img.write(img_data)
            lines.append(f"Extracted image {img_idx}: {img_path} ({len(img_data)} bytes)")
            img_idx += 1

    lines.append("\n=== PARAGRAPHS ===")
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if t:
            lines.append(f"[{i}] {t}")
            
    lines.append("\n=== TABLES ===")
    for t_idx, tbl in enumerate(doc.tables):
        lines.append(f"\n--- TABLE {t_idx} ({len(tbl.rows)} rows, {len(tbl.columns)} cols) ---")
        for r_idx, r in enumerate(tbl.rows):
            row_cells = [c.text.strip().replace('\n', ' // ') for c in r.cells]
            lines.append(f"  Row {r_idx}: " + " | ".join(row_cells))
            
    with open(out_txt + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Written: {out_txt}.txt")

base = r"C:/Users/HoangThien/.gemini/antigravity/brain/80ce0a13-e50b-482d-9d30-b6dde4de8f42"
inspect_doc(os.path.join(base, ".user_uploaded/media_1795398554470_cf010f7c.docx"), "TROLYTHIEN/TEMP/tin6_dump")
inspect_doc(os.path.join(base, ".user_uploaded/media_1795398496828_3ac10fe1.docx"), "TROLYTHIEN/TEMP/toan6_de_dump")
inspect_doc(os.path.join(base, ".user_uploaded/media_1795398496827_9ff99f2e.docx"), "TROLYTHIEN/TEMP/toan6_da_dump")
inspect_doc(os.path.join(base, ".user_uploaded/media_1795398543453_c54767b9.docx"), "TROLYTHIEN/TEMP/toan9_de_dump")
inspect_doc(os.path.join(base, "toan9_da.docx"), "TROLYTHIEN/TEMP/toan9_da_dump")
