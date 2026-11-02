"""Hậu xử lý ảnh PNG. Các mẫu hình đơn lẻ đã gỡ khỏi giao diện."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path


def _chunk(tag: bytes, data: bytes) -> bytes:
    body = tag + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def ensure_png_300dpi(path: Path, dpi: int = 300) -> None:
    """Gắn khối pHYs 300 DPI vào PNG nền trắng để chèn Word không vỡ hạt."""
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return
    ppm = int(round(dpi / 0.0254))
    phys = _chunk(b"pHYs", struct.pack(">IIB", ppm, ppm, 1))
    out = bytearray(data[:8])
    index = 8
    inserted = False
    while index + 8 <= len(data):
        length = struct.unpack(">I", data[index : index + 4])[0]
        tag = data[index + 4 : index + 8]
        end = index + 12 + length
        if end > len(data):
            return
        piece = data[index:end]
        index = end
        if tag == b"pHYs":
            continue
        if tag == b"IDAT" and not inserted:
            out.extend(phys)
            inserted = True
        out.extend(piece)
        if tag == b"IEND":
            break
    if not inserted:
        return
    path.write_bytes(bytes(out))
