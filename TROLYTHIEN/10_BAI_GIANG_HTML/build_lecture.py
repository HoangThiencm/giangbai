# -*- coding: utf-8 -*-
import os, sys

target_file = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\10_BAI_GIANG_HTML\Ket_qua\Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html"

# SVG definitions
SVG_H21 = '''<svg viewBox="0 0 280 280" style="max-width:240px;margin:10px auto;display:block;" preserveAspectRatio="xMidYMid meet">
  <!-- Khu vuon vuong 15m x 15m (canh 220px) -->
  <rect x="30" y="30" width="220" height="220" fill="#f8fafc" stroke="#1e293b" stroke-width="2.5" rx="4"/>
  <!-- Phan dat trong co 169m2 (canh 150px) -->
  <rect x="65" y="65" width="150" height="150" fill="#86efac" stroke="#166534" stroke-width="2" rx="2"/>
  <text x="140" y="145" text-anchor="middle" font-size="15" font-weight="700" fill="#14532d">169 m²</text>
  <text x="140" y="165" text-anchor="middle" font-size="12" fill="#15803d">(Đất cỏ)</text>
  <!-- Duong kich thuoc canh vuon 15m -->
  <line x1="30" y1="16" x2="250" y2="16" stroke="#0284c7" stroke-width="1.8"/>
  <polyline points="35,12 30,16 35,20" fill="none" stroke="#0284c7" stroke-width="1.8"/>
  <polyline points="245,12 250,16 245,20" fill="none" stroke="#0284c7" stroke-width="1.8"/>
  <text x="140" y="12" text-anchor="middle" font-size="14" font-weight="700" fill="#0369a1">15 m</text>
  <!-- Duong kich thuoc loi di x -->
  <line x1="215" y1="262" x2="250" y2="262" stroke="#d97706" stroke-width="1.8"/>
  <polyline points="219,258 215,262 219,266" fill="none" stroke="#d97706" stroke-width="1.8"/>
  <polyline points="246,258 250,262 246,266" fill="none" stroke="#d97706" stroke-width="1.8"/>
  <text x="232" y="277" text-anchor="middle" font-size="13" font-weight="700" fill="#b45309">x</text>
  <text x="140" y="275" text-anchor="middle" font-size="12" font-style="italic" fill="#475569">Hình 2.1: Sân vườn và lối đi</text>
</svg>'''

SVG_H22 = '''<svg viewBox="0 0 290 250" style="max-width:260px;margin:10px auto;display:block;" preserveAspectRatio="xMidYMid meet">
  <!-- Manh dat hinh chu nhat 14m x 12m (rong 224, cao 192) -->
  <rect x="25" y="25" width="224" height="192" fill="#bae6fd" stroke="#0284c7" stroke-width="2.5" rx="3"/>
  <text x="137" y="48" text-anchor="middle" font-size="14" font-weight="700" fill="#0369a1">Sân vườn</text>
  <!-- Nha hinh vuong 10m x 10m (160 x 160) -->
  <rect x="25" y="57" width="160" height="160" fill="#fef08a" stroke="#ca8a04" stroke-width="2" rx="2"/>
  <text x="105" y="135" text-anchor="middle" font-size="16" font-weight="800" fill="#854d0e">Nhà</text>
  <text x="105" y="155" text-anchor="middle" font-size="13" font-weight="600" fill="#a16207">100 m²</text>
  <!-- Kich thuoc dai 14m -->
  <line x1="25" y1="12" x2="249" y2="12" stroke="#0f172a" stroke-width="1.8"/>
  <polyline points="30,8 25,12 30,16" fill="none" stroke="#0f172a" stroke-width="1.8"/>
  <polyline points="244,8 249,12 244,16" fill="none" stroke="#0f172a" stroke-width="1.8"/>
  <text x="137" y="8" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">14 m</text>
  <!-- Kich thuoc rong 12m -->
  <line x1="262" y1="25" x2="262" y2="217" stroke="#0f172a" stroke-width="1.8"/>
  <polyline points="258,30 262,25 266,30" fill="none" stroke="#0f172a" stroke-width="1.8"/>
  <polyline points="258,212 262,217 266,212" fill="none" stroke="#0f172a" stroke-width="1.8"/>
  <text x="276" y="125" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">12 m</text>
  <!-- Dai san vuon tren x -->
  <line x1="12" y1="25" x2="12" y2="57" stroke="#b45309" stroke-width="1.5"/>
  <text x="5" y="45" font-size="12" font-weight="700" fill="#b45309">x</text>
  <!-- Dai san vuon phai x+2 -->
  <line x1="185" y1="230" x2="249" y2="230" stroke="#b45309" stroke-width="1.5"/>
  <polyline points="189,226 185,230 189,234" fill="none" stroke="#b45309" stroke-width="1.5"/>
  <polyline points="245,226 249,230 245,234" fill="none" stroke="#b45309" stroke-width="1.5"/>
  <text x="217" y="244" text-anchor="middle" font-size="12" font-weight="700" fill="#b45309">x + 2</text>
  <text x="137" y="244" text-anchor="middle" font-size="11" font-style="italic" fill="#475569">Hình 2.2: Mảnh đất và sân vườn</text>
</svg>'''

print("SVGs prepared successfully.")