# Quy chuẩn vẽ hình mẫu tức thì

Dùng khi hình thuộc mẫu sách giáo khoa. Hình lạ, ảnh đề, hoặc phối cảnh đặc thù vẫn vẽ bằng phân tích tự do, theo `HUONG_DAN_VE_HINH.md`.

Ứng dụng desktop dựng cùng quy tắc trong `app_trolythien/core/geometry_engine.py`. Không gọi AI cho các mẫu dưới đây.

## Mẫu có sẵn

- Chóp \(S.ABC\): đáy đều, đáy vuông tại \(A\), \(SA \perp (ABC)\), đáy thường.
- Chóp \(S.ABCD\): đáy chữ nhật, đáy bình hành, \(SA \perp (ABCD)\), chóp đều.
- Hình hộp chữ nhật và lập phương \(ABCD.A'B'C'D'\).
- Lăng trụ tam giác đứng \(ABC.A'B'C'\).
- Hình nón, hình trụ, mặt cầu.
- Tam giác phẳng: vuông, cân, đều, đường cao \(AH\), trung tuyến \(AM\).
- Đường tròn ngoại tiếp hoặc nội tiếp tam giác.

## Phép chiếu xiên

Trục \(x\) sang phải, \(y\) lùi xa người xem và đi lên trang, \(z\) thẳng đứng. Góc nhìn sách giáo khoa khoảng \(42^\circ\), hệ số sâu \(0{,}5\).

```python
import math

def chieu(x, y, z, goc=42, sau=0.52, goc_goc=(250, 320), don_vi=78):
    rad = math.radians(goc)
    return (
        goc_goc[0] + don_vi * (x + y * sau * math.cos(rad)),
        goc_goc[1] - don_vi * (z + y * sau * math.sin(rad)),
    )
```

Cạnh nhìn thấy là nét liền. Cạnh khuất dùng `stroke-dasharray="4,4"`. Với hộp và chóp nhìn từ phía trước, các cạnh qua đỉnh khuất \(D\) hoặc cạnh đáy sau là nét đứt.

Góc vuông là hình vuông nhỏ nằm trong góc, trên mặt phẳng màn hình, không ghi chữ "vuông".

Nhãn đỉnh là chữ nghiêng Times New Roman, đặt lệch ra ngoài hình:

```xml
<text font-family="Times New Roman" font-style="italic" font-size="18">A</text>
```

Khung hình chỉ có nét, cung và nhãn. Không tiêu đề, không chú thích, không lời giải.

## Chóp \(S.ABC\) đáy vuông, \(SA\) là đường cao

\(A(0,0,0)\), \(B(2{,}3,0,0)\), \(C(0,1{,}7,0)\), \(S(0,0,2{,}15)\). Nét liền: \(AB\), \(AC\), \(SA\), \(SB\). Nét đứt: \(BC\), \(SC\). Dấu vuông tại \(A\).

Đổi tên đỉnh thì chỉ đổi nhãn, không đổi tọa độ. Đổi góc nhìn thì chỉ đổi tham số `goc` trong phép chiếu.
