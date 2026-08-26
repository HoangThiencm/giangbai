const assert = require("assert");
const { extractTextbookSubsections, getPromptTemplate } = require("../js/khbd-prompts.js");
const { assertPhasePedagogyOutput } = require("../js/khbd-app.js");

function testExtractSubsections() {
  console.log("-> 1. Kiểm tra extractTextbookSubsections với các dạng nội dung SGK...");

  // Test 1: 1 mục
  const input1 = `
2. **Khung kiến thức trọng tâm:**
- Mục 1: Khái niệm góc và các yếu tố của góc
`;
  const res1 = extractTextbookSubsections(input1);
  assert.strictEqual(res1.length, 1, "Phải trích xuất được đúng 1 tiểu mục");
  assert.strictEqual(res1[0].index, 1);
  assert.strictEqual(res1[0].title, "Khái niệm góc và các yếu tố của góc");

  // Test 2: 2 mục với định dạng Mục 1, Mục 2
  const input2 = `
1. **Tổng quan bài học:** Bài 3: Hai đường thẳng song song
2. **Khung kiến thức trọng tâm (Bóc tách rõ ràng theo từng tiểu mục SGK để ánh xạ 1-1 sang hoạt động dạy học):**
   - Mục 1: Dấu hiệu nhận biết hai đường thẳng song song
   - Mục 2: Tiên đề Euclid về đường thẳng song song
3. **Chuỗi hoạt động khám phá trong SGK:**
   - HĐ 1: Vẽ hai đường thẳng
   - HĐ 2: Đo góc so le trong
4. **Hệ thống bài tập cuối bài:**
   - Bài 1: Cho hình vẽ...
`;
  const res2 = extractTextbookSubsections(input2);
  assert.strictEqual(res2.length, 2, "Phải trích xuất được đúng 2 tiểu mục");
  assert.strictEqual(res2[0].index, 1);
  assert.strictEqual(res2[0].title, "Dấu hiệu nhận biết hai đường thẳng song song");
  assert.strictEqual(res2[1].index, 2);
  assert.strictEqual(res2[1].title, "Tiên đề Euclid về đường thẳng song song");

  // Test 3: 3 mục với định dạng Hoạt động khám phá
  const input3 = `
Hoạt động khám phá 1: Phép cộng hai số nguyên cùng dấu
Hoạt động khám phá 2: Phép cộng hai số nguyên khác dấu
Hoạt động khám phá 3: Tính chất của phép cộng các số nguyên
`;
  const res3 = extractTextbookSubsections(input3);
  assert.strictEqual(res3.length, 3, "Phải trích xuất được đúng 3 tiểu mục từ Hoạt động khám phá");
  assert.strictEqual(res3[0].index, 1);
  assert.strictEqual(res3[0].title, "Phép cộng hai số nguyên cùng dấu");
  assert.strictEqual(res3[1].index, 2);
  assert.strictEqual(res3[1].title, "Phép cộng hai số nguyên khác dấu");
  assert.strictEqual(res3[2].index, 3);
  assert.strictEqual(res3[2].title, "Tính chất của phép cộng các số nguyên");

  // Test 4: 4 mục với định dạng số thứ tự 1., 2., 3., 4.
  const input4 = `
2. **Khung kiến thức trọng tâm:**
### 1. Khái niệm hình chữ nhật
- Định nghĩa hình chữ nhật
### 2. Tính chất của hình chữ nhật
- Tính chất cạnh và góc
### 3. Dấu hiệu nhận biết hình chữ nhật
- 4 dấu hiệu nhận biết
### 4. Áp dụng vào tam giác vuông
- Định lý đường trung tuyến ứng với cạnh huyền
3. **Chuỗi hoạt động khám phá trong SGK:**
`;
  const res4 = extractTextbookSubsections(input4);
  assert.strictEqual(res4.length, 4, "Phải trích xuất được đúng 4 tiểu mục");
  assert.strictEqual(res4[0].index, 1);
  assert.strictEqual(res4[0].title, "Khái niệm hình chữ nhật");
  assert.strictEqual(res4[1].index, 2);
  assert.strictEqual(res4[1].title, "Tính chất của hình chữ nhật");
  assert.strictEqual(res4[2].index, 3);
  assert.strictEqual(res4[2].title, "Dấu hiệu nhận biết hình chữ nhật");
  assert.strictEqual(res4[3].index, 4);
  assert.strictEqual(res4[3].title, "Áp dụng vào tam giác vuông");

  // Test 5: Input rỗng / null
  assert.deepStrictEqual(extractTextbookSubsections(""), []);
  assert.deepStrictEqual(extractTextbookSubsections(null), []);

  console.log("  -> extractTextbookSubsections: PASS");
}

function testPromptTemplateActivityB() {
  console.log("-> 2. Kiểm tra getPromptTemplate('GENERATE_ACTIVITY_B')...");

  const stubContext = {
    subjectName: "Toán",
    gradeLevelName: "THCS",
    topic: "Tập hợp các số tự nhiên",
    duration: "2 tiết",
    objectives_content: "I. Mục tiêu bài học",
    textbook_content: `
2. **Khung kiến thức trọng tâm:**
- Mục 1: Khái niệm tập hợp
- Mục 2: Phần tử của tập hợp
- Mục 3: Cách viết tập hợp
`
  };

  const promptB = getPromptTemplate("GENERATE_ACTIVITY_B", stubContext);
  assert.ok(promptB.includes("NGUYÊN TẮC ÁNH XẠ 1-1 BẮT BUỘC THEO TIỂU MỤC SGK"), "Prompt B phải có nguyên tắc ánh xạ 1-1");
  assert.ok(promptB.includes("TUYỆT ĐỐI CẤM GỘP"), "Prompt B phải cấm gộp tiểu mục");
  assert.ok(promptB.includes("TUYỆT ĐỐI CẤM BỊA THÊM"), "Prompt B phải cấm bịa thêm hoạt động");
  assert.ok(promptB.includes("DANH SÁCH TIỂU MỤC SGK BẮT BUỘC ÁP DỤNG (ĐÚNG 3 HOẠT ĐỘNG NHÁNH)"), "Prompt B phải nhúng danh sách đúng 3 tiểu mục");
  assert.ok(promptB.includes("### 1. Hoạt động 2.1: Khái niệm tập hợp"), "Prompt B phải có chỉ định cho Hoạt động 2.1");
  assert.ok(promptB.includes("### 2. Hoạt động 2.2: Phần tử của tập hợp"), "Prompt B phải có chỉ định cho Hoạt động 2.2");
  assert.ok(promptB.includes("### 3. Hoạt động 2.3: Cách viết tập hợp"), "Prompt B phải có chỉ định cho Hoạt động 2.3");

  console.log("  -> getPromptTemplate Activity B: PASS");
}

function testAssertPhasePedagogyOutput() {
  console.log("-> 3. Kiểm tra assertPhasePedagogyOutput cho Pha B...");

  const validOutputB = `
## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI

### 1. Hoạt động 2.1: Khái niệm tập hợp
#### a) Mục tiêu:
- Nhận biết khái niệm tập hợp.
#### b) Nội dung:
- Học sinh làm việc cá nhân HĐ 1.
#### c) Sản phẩm:
- Kết quả HĐ 1: $A = \\{1, 2, 3\\}$.
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** Giao HĐ 1: "Quan sát các đồ vật trên bàn...". **HS:** Tiếp nhận nhiệm vụ.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Làm việc cá nhân (2 phút) ghi nháp -> Thảo luận cặp (3 phút). **GV:** Quan sát, phát hiện lỗi sai: nhầm lẫn ngoặc, hỗ trợ phân hóa.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện cặp trả lời. **GV:** Điều hành thảo luận.<br>+ Bước 4: Kết luận, nhận định: **GV:** Chốt khái niệm. **HS:** Ghi bài vào vở. | **1. Khái niệm tập hợp**<br>- Tập hợp gồm các phần tử. |

### 2. Hoạt động 2.2: Phần tử thuộc và không thuộc tập hợp
#### a) Mục tiêu:
- Sử dụng đúng ký hiệu thuộc và không thuộc.
#### b) Nội dung:
- Học sinh làm việc nhóm hoàn thành Phiếu học tập số 1.
#### c) Sản phẩm:
- Ký hiệu: $a \\in A, b \\notin A$.
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: **GV:** Phát phiếu học tập: "Điền ký hiệu thích hợp...". **HS:** Nhận phiếu.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Cá nhân làm bài -> Nhóm chấm chéo. **GV:** Quan sát, hướng dẫn HS lúng túng.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** 2 nhóm lên bảng điền kết quả. **GV:** Đặt câu hỏi phản biện.<br>+ Bước 4: Kết luận, nhận định: **GV:** Chốt quy tắc ký hiệu. **HS:** Chữa bài chuẩn xác vào vở. | **2. Phần tử của tập hợp**<br>- $x \\in A$: $x$ thuộc $A$.<br>- $y \\notin A$: $y$ không thuộc $A$. |
`;

  // 1. Output hợp lệ 2 nhánh -> PASS
  assert.doesNotThrow(() => assertPhasePedagogyOutput("B", validOutputB), "Valid multi-branch Activity B phải pass");

  // 2. Nhánh 2.2 thiếu bảng 2 cột mục d -> Ném lỗi
  const invalidMissingTable = validOutputB.replace(
    /\| Hoạt động của GV và HS \| Nội dung \|[\s\S]*?\|\s*\*\*2\. Phần tử của tập hợp\*\*[\s\S]*?\|/i,
    "GV yêu cầu HS làm bài tập."
  );
  assert.throws(
    () => assertPhasePedagogyOutput("B", invalidMissingTable),
    /chưa có bảng 2 cột ở mục d\)/i,
    "Nhánh thiếu bảng phải throw"
  );

  // 3. Nhánh 2.1 thiếu Bước 4 -> Ném lỗi
  const invalidMissingStep4 = validOutputB.replace(
    /\+ Bước 4: Kết luận, nhận định: \*\*GV:\*\* Chốt khái niệm\. \*\*HS:\*\* Ghi bài vào vở\./i,
    ""
  );
  assert.throws(
    () => assertPhasePedagogyOutput("B", invalidMissingStep4),
    /chưa có đủ 4 bước trong bảng tổ chức thực hiện/i,
    "Nhánh thiếu bước phải throw"
  );

  // 4. Nhánh 2.1 thiếu vai trò HS -> Ném lỗi
  const invalidMissingHs = validOutputB.replace(
    /\+ Bước 1: Chuyển giao nhiệm vụ: \*\*GV:\*\* Giao HĐ 1: "Quan sát các đồ vật trên bàn\.\.\."\. \*\*HS:\*\* Tiếp nhận nhiệm vụ\./i,
    '+ Bước 1: Chuyển giao nhiệm vụ: **GV:** Giao HĐ 1: "Quan sát các đồ vật trên bàn...".'
  ).replace(
    /\+ Bước 2: Thực hiện nhiệm vụ: \*\*HS:\*\* Làm việc cá nhân \(2 phút\) ghi nháp -> Thảo luận cặp \(3 phút\)\. \*\*GV:\*\* Quan sát, phát hiện lỗi sai: nhầm lẫn ngoặc, hỗ trợ phân hóa\./i,
    "+ Bước 2: Thực hiện nhiệm vụ: **GV:** Quan sát, phát hiện lỗi sai: nhầm lẫn ngoặc, hỗ trợ phân hóa."
  ).replace(
    /\+ Bước 3: Báo cáo, thảo luận: \*\*HS:\*\* Đại diện cặp trả lời\. \*\*GV:\*\* Điều hành thảo luận\./i,
    "+ Bước 3: Báo cáo, thảo luận: **GV:** Điều hành thảo luận."
  ).replace(
    /\+ Bước 4: Kết luận, nhận định: \*\*GV:\*\* Chốt khái niệm\. \*\*HS:\*\* Ghi bài vào vở\./i,
    "+ Bước 4: Kết luận, nhận định: **GV:** Chốt khái niệm."
  );
  assert.throws(
    () => assertPhasePedagogyOutput("B", invalidMissingHs),
    /chưa phân định rõ ràng vai trò GV và HS/i,
    "Nhánh thiếu vai trò HS phải throw"
  );

  console.log("  -> assertPhasePedagogyOutput Activity B: PASS");
}

function main() {
  console.log("==================================================");
  console.log("BẮT ĐẦU KIỂM THỬ ÁNH XẠ 1-1 TIỂU MỤC SGK & HOẠT ĐỘNG B");
  console.log("==================================================");

  testExtractSubsections();
  testPromptTemplateActivityB();
  testAssertPhasePedagogyOutput();

  console.log("==================================================");
  console.log("TẤT CẢ TEST ÁNH XẠ 1-1 TIỂU MỤC HOẠT ĐỘNG B ĐỀU ĐẠT (PASS)!");
  console.log("==================================================");
}

main();
