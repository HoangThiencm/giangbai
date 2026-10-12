# Hướng dẫn tạo đề thi từ Ma trận và Bản đặc tả

Dùng cho lựa chọn 12 của Menu Cấp 2 "Tạo bài tập". Đây là Master Prompt khi giáo viên đưa khung ma trận và bản đặc tả dạng Word `.docx`.

## 1. Nạp file

Ưu tiên đường dẫn giáo viên dán trong chat (thư mục hoặc một tệp `.docx`). Đường dẫn tương đối, có khoảng trắng hoặc tiếng Việt đều được. Chuẩn hóa bằng `pathlib.Path.resolve()`, rồi kiểm tra `is_dir()` hoặc `is_file()`.

Không có đường dẫn thì quét đệ quy:

`TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/`

Kể cả thư mục con theo ngày, ví dụ `Dau_vao/12.10/`. Bỏ tệp tạm Word bắt đầu bằng `~$`.

Đường dẫn không tồn tại: dừng, báo đúng đường dẫn đã nhận. Không tự chuyển sang thư mục khác.

Lệnh engine:

```text
python TROLYTHIEN/engine/doc_ma_tran_dac_ta.py --input-dir "TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/12.10"
python TROLYTHIEN/engine/doc_ma_tran_dac_ta.py --file "đường-dẫn-tệp.docx"
```

JSON trả về có chủ đề, đơn vị kiến thức, mức độ, yêu cầu cần đạt, dạng câu, số câu và số điểm. Sinh đề từ JSON này, không đọc lại bảng bằng mắt rồi bỏ sót dòng.

## 2. Khung ma trận

Giữ nguyên:

- Số câu và số điểm từng ô (trắc nghiệm, tự luận, đúng/sai, trả lời ngắn).
- Mức độ: nhận biết, thông hiểu, vận dụng, vận dụng cao. Cột ghi "Biết" là nhận biết, "Hiểu" là thông hiểu.
- Tỉ lệ điểm và tổng điểm (thường 10 điểm).
- Chủ đề hoặc chương và đơn vị kiến thức.

Đề Công văn 7991 giữ đúng ba phần nếu ma trận có nhiều lựa chọn, đúng/sai và trả lời ngắn. Đề kết hợp trắc nghiệm và tự luận thì giữ đúng tỉ lệ trong bảng. Không thêm câu ngoài ma trận. Không gộp hai ô thành một câu nếu bảng đang tách điểm.

## 3. Bản đặc tả

Mỗi dòng yêu cầu cần đạt sinh đúng nhóm câu mà dòng đó ghi (mã TN, TL, số câu, số điểm).

- Một yêu cầu cần đạt không bị tách sang chủ đề khác.
- Câu hỏi nằm trong đơn vị kiến thức của dòng đó.
- Mức độ của câu đúng mức độ của dòng (không nâng vận dụng cao khi dòng chỉ là nhận biết).
- Thiếu mã câu ở một dòng: vẫn phủ yêu cầu cần đạt đó, và ghi chú trong phần đối chiếu.

## 4. Biên soạn theo GDPT 2018

- Đúng môn, khối lớp và mạch kiến thức trong bảng. Lớp 6, 7, 8 không dùng kiến thức lớp trên. Toán THCS không dùng định lý sin, côsin, công thức lượng giác cấp THPT.
- Không dùng dấu tương đương $\Leftrightarrow$. Không kết luận tập nghiệm $S = \{...\}$. Viết "Ta có", "Suy ra" ($\Rightarrow$), "hoặc", rồi nêu từng nghiệm.
- Công thức soạn bằng LaTeX trong `$...$` hoặc `$$...$$` lúc thảo đề. Khi ghi Word thì chuyển hết sang Word Equation.
- Số liệu trong đề phải giải được trong thời gian của kỳ thi. Không đưa bài olympic ngoài yêu cầu cần đạt.
- Ngôn ngữ đề rõ, một ý hỏi một việc. Phương án nhiễu cùng dạng với đáp án đúng.

## 5. Xuất Word

Dùng `latex_to_omml` trong `TROLYTHIEN/2_TAO_BAI_TAP/QUY_CHUAN_TRON_DE.md`: LaTeX $\rightarrow$ MathML (`latex2mathml`) $\rightarrow$ OMML (`MML2OMML.XSL`) $\rightarrow$ chèn `m:oMath` bằng `python-docx`.

Cấm để trần `$x^2$` trong file Word. Cấm chèn ảnh chụp công thức. Giáo viên phải sửa được công thức trong Word.

Thể thức đề:

- Khổ A4. Phông Times New Roman.
- Đầu đề trường THCS Trần Phú: Cộng hòa xã hội chủ nghĩa Việt Nam, tiêu ngữ, tên trường, môn, khối, thời gian, năm học.
- Khung thông tin học sinh: họ và tên, lớp, trường, điểm.
- Bảng đóng khung đủ bốn cạnh. Điểm từng phần ghi đúng ma trận.

## 6. Ba phần trong một file

1. **Đề kiểm tra.** Đủ câu, đủ phương án hoặc chỗ trình bày tự luận, ghi điểm từng phần.
2. **Ma trận đối chiếu và bảng đáp án.** Mỗi câu một dòng: mã câu, chủ đề, mức độ, yêu cầu cần đạt, dạng câu, đáp án, điểm.
3. **Hướng dẫn chấm.** Từng câu tự luận có các bước và điểm từng bước. Câu trắc nghiệm ghi đáp án và điểm. Câu đúng/sai chấm theo barem của ma trận; nếu ma trận không nói khác và đề theo Công văn 7991 thì: 1 ý đúng 0,1 điểm; 2 ý đúng 0,25 điểm; 3 ý đúng 0,5 điểm; 4 ý đúng 1,0 điểm.

## 7. Nơi lưu

Mặc định:

`TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/De_Kiem_Tra_[Mon]_[Lop]_[KyThi].docx`

Ví dụ: `De_Kiem_Tra_Toan_8_Giua_HK1.docx`.

Giáo viên chỉ định thư mục kết quả thì ghi vào thư mục đó, giữ cùng kiểu tên file.

Chat chỉ cần: đã tạo đề, đường dẫn file, số câu và tổng điểm đã bóc từ ma trận.
