# HƯỚNG DẪN THÊM BÀI VÀO KHO

## 1. Cấu trúc kho

```
Code_PTIT/
├── README.md
├── HUONG_DAN_THEM_BAI.md          ← file này
├── nhap/                          ← file nháp khi soạn bài (không bị commit)
├── tools/
│   ├── add_problem.py             ← script chèn bài tự động
│   └── mau_bai.md                 ← file mẫu để copy khi viết bài mới
└── <Tên môn>/                     ← 6 môn: Tin học cơ sở 2, C++, DSA, OOP, Python, Thuật toán nâng cao
    ├── README.md                  ← toàn bộ đề bài của môn nằm trong 1 file này
    └── img/                       ← ảnh minh họa của môn
```

Mỗi `README.md` có 3 cấp tiêu đề:

| Cấp | Dùng cho | Ví dụ |
|---|---|---|
| `#` | Tên môn (chỉ 1 dòng đầu file) | `# ĐỀ BÀI: NGÔN NGỮ LẬP TRÌNH C++` |
| `##` | Chương / chủ đề | `## VÒNG LẶP` |
| `###` | Một bài tập: `MÃ - TÊN BÀI` | `### C01001 - GẤP ĐÔI` |

Trong mỗi chương, các bài **được sắp theo mã bài tăng dần** (so sánh chuỗi: `C01001 < C02001 < CHELLO < PR-2022-001`).

## 2. Format chuẩn của một bài

````markdown
### C01002 - GẤP ĐÔI 2

Cho số tự nhiên N không quá 9 chữ số. Hãy in ra giá trị gấp đôi của N.

**Input**

Dòng đầu ghi số bộ test. Mỗi bộ test có duy nhất một số tự nhiên không quá 9 chữ số.

**Output**

Với mỗi bộ test, ghi ra kết quả trên một dòng.

**Ví dụ**

| **Input** | **Output** |
|---|---|
| 2<br>1<br>23 | 2<br>46 |
````

Quy tắc:

- Tiêu đề bài: `### MÃBÀI - TÊN BÀI`, tên bài **VIẾT HOA**, mã bài không có dấu cách.
- Các mục dùng chữ in đậm trên một dòng riêng: `**Input**`, `**Output**`, `**Ví dụ**` (thêm `**Giải thích test:**`, `**Ràng buộc:**`… nếu đề có).
- Ràng buộc nhiều ý thì dùng gạch đầu dòng `- ...`.
- Luôn có **một dòng trống** giữa các đoạn và trước tiêu đề bài tiếp theo.
- Ví dụ là bảng 2 cột. Mỗi test ví dụ là **một dòng** của bảng; xuống dòng bên trong ô dùng `<br>`.
- Lũy thừa / chỉ số: `10<sup>6</sup>`, `a<sub>i</sub>` (nếu gõ `106` sẽ bị hiểu nhầm thành một trăm lẻ sáu).
- Ký tự đặc biệt trong đề cần escape: `\*`, `\_`, `\[`, `\]`, `\|`; trong ô bảng dùng `&lt;` cho `<`.
- Ảnh: đặt file vào `img/` của môn, đặt tên `MÃBÀI.png` hoặc `MÃBÀI_1.png`, `MÃBÀI_2.png`…, rồi chèn `![Ảnh](./img/MÃBÀI_1.png)`.

## 3. Cách 1 — dùng script (khuyên dùng): 8 bước

Chỉ cần Python 3.8+, không cài thêm gì. Mọi lệnh gõ trong **terminal**: PowerShell, Command Prompt, Git Bash hoặc terminal của VS Code (`` Ctrl+` ``).

Ví dụ xuyên suốt: thêm bài **DSADQ01 — Đoạn con cân bằng dài nhất** vào môn DSA. Với bài khác, chỉ cần thay mã bài, tên môn (`-k`) và tên chương (`-c`).

### Bước 0. Mở terminal ở đúng thư mục

```bash
cd C:\Users\dell\Desktop\codeptit-Problemset\Code_PTIT
```

Mỗi lần mở terminal mới đều phải chạy lệnh này trước. Nếu gặp lỗi `can't open file '...\tools\add_problem.py'` thì terminal đang ở sai thư mục, hãy `cd` lại.

### Bước 1. Kiểm tra bài đã có trong kho chưa

```bash
python tools/add_problem.py find DSADQ01
```

- `Chưa có bài DSADQ01 trong kho.` → làm tiếp bước 2.
- Nếu in ra vị trí bài → bài đã có. Muốn sửa lại bài cũ thì vẫn làm các bước dưới, nhưng ở bước 5 và 6 thêm `--replace` (không cần `-c`).

Phải gõ **mã đầy đủ** (`DSA_P040`, không phải `P040`).

### Bước 2. Chọn chương

```bash
python tools/add_problem.py list -k dsa
```

Chọn chương hợp với nội dung bài. DSADQ01 dùng cửa sổ trượt với deque → chương **QUEUE**. Không cần quan tâm vị trí trong chương, script tự xếp theo mã bài.

Tên môn gõ tắt được: `thcs2` / `c`, `cpp` / `c++`, `dsa` / `ctdl`, `oop` / `java`, `py` / `python`, `tnc`, hoặc một phần tên không dấu như `"huong doi tuong"`. Tên chương cũng gõ không dấu được (`queue`, `"vong lap"`).

### Bước 3. Tạo file nháp từ file mẫu

```bash
mkdir nhap
```

```bash
copy tools\mau_bai.md nhap\DSADQ01.md
```

```bash
code nhap\DSADQ01.md
```

Lệnh `mkdir` chỉ cần ở lần đầu (báo lỗi "already exists" thì bỏ qua). Không dùng VS Code thì thay `code` bằng `notepad`. Thư mục `nhap/` đã nằm trong `.gitignore` nên file nháp không bị commit.

### Bước 4. Viết đề vào file nháp

1. **Dòng tiêu đề:** `### DSADQ01 - Đoạn con cân bằng dài nhất`. Bắt buộc có `### ` ở đầu và dấu cách hai bên `-`. Tên bài gõ thường cũng được, script tự viết hoa.
2. **Nội dung:** thay phần mẫu bằng đề bài, giữ các mục `**Input**`, `**Output**`, mỗi mục một dòng riêng và có dòng trống trước/sau.
3. **Ký hiệu toán:** khi copy từ web chỉ số và số mũ bị mất, phải gõ lại:

   | Trên web | Gõ trong nháp |
   |---|---|
   | a₁, a₂, …, aₙ | `a<sub>1</sub>, a<sub>2</sub>, ..., a<sub>n</sub>` |
   | aᵢ (mọi chỗ, kể cả trong ràng buộc) | `a<sub>i</sub>` |
   | 2 × 10⁹ | `2 × 10<sup>9</sup>` |
   | [l, r], A[i][j] | `\[l, r\]`, `A\[i\]\[j\]` |
   | \|aᵢ − aⱼ\| | `\|a<sub>i</sub> - a<sub>j</sub>\|` |

   Dấu `≤`, `≥`, `×`, `→` copy thẳng từ web là được.
4. **Ví dụ:** dán nguyên input vào khối ```` ```input ````, output vào khối ```` ```output ````, giữ nguyên xuống dòng. Có nhiều test ví dụ thì viết nhiều cặp liên tiếp. **Đề không có ví dụ thì xóa cả mục `**Ví dụ**` và hai khối mẫu.**

   ````markdown
   **Ví dụ**

   ```input
   2
   1
   23
   ```

   ```output
   2
   46
   ```
   ````

5. Đoạn comment `<!-- ... -->` ở đầu file để nguyên hay xóa đều được, script tự bỏ. Một file nháp có thể chứa nhiều bài, mỗi bài bắt đầu bằng một dòng `### MÃ - TÊN`.
6. Lưu file (`Ctrl+S`), rồi đọc lại một lượt để soát lỗi chính tả.

### Bước 5. Xem trước (chưa ghi gì vào kho)

```bash
python tools/add_problem.py add nhap/DSADQ01.md -k dsa -c queue --dry-run
```

Kiểm tra:

- Dòng đầu: `Thêm DSADQ01 - ĐOẠN CON CÂN BẰNG DÀI NHẤT -> Cấu trúc dữ liệu và giải thuật (DSA) / ## QUEUE (dòng ...)`, tức là đúng môn, đúng chương.
- Nội dung in giữa hai đường `-----` chính là phần sẽ được chèn. Có ví dụ thì phải thấy bảng `| **Input** | **Output** |`.
- Dòng cuối: `(dry-run: chưa ghi gì vào file)`.

Thấy sai thì sửa nháp, lưu lại rồi chạy lại bước này.

### Bước 6. Thêm thật vào kho

```bash
python tools/add_problem.py add nhap/DSADQ01.md -k dsa -c queue
```

Lệnh giống bước 5 nhưng bỏ `--dry-run`. Lỡ thêm rồi mới thấy sai thì sửa nháp và chạy lại kèm `--replace`:

```bash
python tools/add_problem.py add nhap/DSADQ01.md -k dsa --replace
```

### Bước 7. Kiểm tra lại

```bash
python tools/add_problem.py find DSADQ01
```

Kết quả phải ra đúng chương đã chọn: `...README.md:<số dòng>  ## QUEUE  ->  DSADQ01 - ĐOẠN CON CÂN BẰNG DÀI NHẤT`.

Muốn xem hiển thị thì mở `README.md` của môn trong VS Code, bấm `Ctrl+Shift+V` để xem preview, rồi `Ctrl+F` tìm mã bài.

### Bước 8. Lưu lại bằng git

```bash
git add -A
```

```bash
git commit -m "Thêm bài DSADQ01"
```

Muốn đưa lên GitHub thì xem mục 6 (cần trỏ `origin` sang repo của bạn trước khi `git push`).

### Gặp lỗi?

| Thông báo | Nguyên nhân / cách sửa |
|---|---|
| `can't open file '...add_problem.py'` | Terminal ở sai thư mục → làm lại bước 0 |
| `không có dòng tiêu đề dạng "### MÃBÀI - TÊN BÀI"` | Dòng tiêu đề sai: thiếu `### ` hoặc thiếu dấu cách quanh `-` |
| `khối ```input mở ... không có ``` đóng` | Quên dòng ```` ``` ```` đóng khối ví dụ |
| `... đã có ở dòng ...` | Mã bài đã tồn tại → thêm `--replace` nếu muốn ghi đè |
| `chưa có chương "..."` | Gõ sai tên chương → xem lại bước 2, hoặc thêm `--new-chapter` để tạo chương mới ở cuối file |
| `"..." khớp nhiều môn / nhiều chương` | Tên gõ quá ngắn → gõ dài hơn cho rõ |

### Script làm gì khi chèn bài

- Đổi các khối `input`/`output` thành bảng `| **Input** | **Output** |`, giữ đúng xuống dòng và dấu cách (bài in hình vẫn đúng).
- Viết hoa tên bài, dọn dòng trống thừa, bỏ các comment `<!-- -->`.
- Chèn bài vào đúng chương, **đúng vị trí theo thứ tự mã bài**.
- Copy ảnh `./img/...` nằm cạnh file nháp sang thư mục `img/` của môn.
- Giữ nguyên kiểu xuống dòng (CRLF/LF) của file README.
- Tự cập nhật mục lục (số bài, chương mới) nếu README đã có mục lục (xem mục 8).

## 4. Cách 2 — thêm bằng tay

1. Mở `README.md` của môn, tìm dòng `## TÊN CHƯƠNG`.
2. Tìm vị trí theo thứ tự mã bài trong chương đó.
3. Dán bài theo đúng format ở mục 2, nhớ có dòng trống trước và sau.
4. Mở preview Markdown (VS Code: `Ctrl+Shift+V`) để kiểm tra bảng ví dụ và ảnh hiển thị đúng.

## 5. Mẹo khi lấy đề từ code.ptit.edu.vn

- Copy phần chữ của đề, rồi tự gắn lại các mục `**Input**`, `**Output**`, `**Ví dụ**`.
- Test ví dụ: copy nguyên khối input/output dán vào khối ```` ```input ```` / ```` ```output ```` — không cần sửa gì.
- Số mũ trên web hay bị mất khi copy (`10^6` thành `106`): sửa lại thành `10<sup>6</sup>`. Chỉ số cũng vậy (`aᵢ` thành `ai`): dò lại **mọi** chỗ, nhất là trong phần ràng buộc.
- Chữ copy từ web có thể kèm dấu cách mảnh (thin space) ẩn quanh `≤`, `×`. Hiển thị vẫn bình thường, nhưng `Ctrl+F` tìm `1 ≤ n` sẽ không ra. Muốn sạch thì xóa đi gõ lại dấu cách thường.
- Ảnh/công thức dạng ảnh: chuột phải → lưu ảnh, đặt tên theo mã bài.

## 6. Lưu kho lên GitHub của bạn

Thư mục này được clone từ repo gốc `QuanNM-PTIT/Code_PTIT`, nên `origin` đang trỏ về đó và bạn không push lên đó được. Cần có một repo của riêng bạn.

### Lần đầu (chỉ làm một lần)

**Bước 1. Tạo repo trên GitHub**, chọn một trong hai cách:

| | Cách A: Fork (khuyên dùng) | Cách B: Repo mới |
|---|---|---|
| Làm thế nào | Mở https://github.com/QuanNM-PTIT/Code_PTIT → nút **Fork** → **Create fork** | Mở https://github.com/new → đặt tên `Code_PTIT` → **không** tick *Add a README*, *.gitignore*, *license* → **Create repository** |
| Ưu điểm | Giữ liên kết và ghi công repo gốc, dễ lấy bài mới từ repo gốc | Chọn được **Private** (chỉ mình bạn xem) |
| Lưu ý | Fork của repo công khai luôn là công khai | Repo phải trống, nếu không lần push đầu sẽ bị từ chối |

Địa chỉ repo của bạn sẽ có dạng `https://github.com/<tên-github-của-bạn>/Code_PTIT.git` (nút **Code** màu xanh trên trang repo → copy).

**Bước 2. Commit những gì đang có** (chạy trong thư mục `Code_PTIT`):

```bash
git add -A
```

```bash
git status
```

Kiểm tra danh sách: phải có các `README.md`, `HUONG_DAN_THEM_BAI.md`, `.gitignore`, `tools/...`, và **không** có `nhap/`. Các dòng cảnh báo `LF will be replaced by CRLF` là bình thường, bỏ qua.

```bash
git commit -m "Thêm bài DSADQ01, mục lục chương và công cụ thêm bài"
```

**Bước 3. Trỏ `origin` sang repo của bạn**, giữ repo gốc dưới tên `upstream`:

```bash
git remote rename origin upstream
```

```bash
git remote add origin https://github.com/<tên-github-của-bạn>/Code_PTIT.git
```

```bash
git remote -v
```

Kết quả đúng: `origin` là repo của bạn, `upstream` là `QuanNM-PTIT/Code_PTIT`.

**Bước 4. Push**:

```bash
git push -u origin main
```

Lần đầu, Windows hiện cửa sổ đăng nhập GitHub (Git Credential Manager) → chọn **Sign in with your browser** → đăng nhập và bấm cho phép trên trình duyệt. Những lần sau không phải đăng nhập lại.

Nếu bị từ chối với thông báo `rejected ... (fetch first)`, nghĩa là repo trên GitHub có commit mà máy bạn chưa có (thường do fork lấy cả commit mới của repo gốc). Lấy về rồi push lại:

```bash
git pull upstream main
```

**Bước 5. Kiểm tra**: mở trang repo của bạn trên GitHub, thấy commit vừa rồi và bài DSADQ01 trong README môn DSA là xong.

### Những lần sau (mỗi lần thêm bài)

```bash
git add -A
```

```bash
git commit -m "Thêm bài <MÃ BÀI>"
```

```bash
git push
```

### Lấy bài mới từ repo gốc

```bash
git pull upstream main
```

### Có cần đổi mục lục sang kiểu `github` trước khi push không?

**Không bắt buộc.** Push chỉ là sao lưu, nội dung đề bài hiển thị trên GitHub như nhau với cả hai kiểu. Khác biệt duy nhất là link trong mục lục / thanh điều hướng:

- **Đọc bài chủ yếu bằng Obsidian** → giữ `obsidian`. Trên GitHub muốn nhảy chương thì dùng nút **Outline** (☰) ở góc trên khung file.
- **Đọc bài chủ yếu trên GitHub** (điện thoại, gửi link cho bạn bè...) → đổi sang `github`, rồi commit và push:

  ```bash
  python tools/add_problem.py toc --style github
  ```

Không nên đổi qua đổi lại trước mỗi lần push, vì mỗi lần đổi là một commit sửa toàn bộ mục lục.

## 7. Lưu ý về dữ liệu cũ

Dữ liệu sẵn có được chuyển tự động từ web nên có vài chỗ lệch format, không ảnh hưởng tới việc thêm bài mới:

- Test ví dụ nhiều dòng bị gộp thành một dòng, ngăn cách bằng 2 dấu cách (`| 2  1  23 | 2  46 |`). Bài mới nên dùng `<br>` như trên.
- Nhãn chưa thống nhất: `**Input**` / `**Input:**` / `Input:` / `**Dữ liệu vào**`, vài chỗ gõ nhầm `**Ouput**`.
- `Tin học cơ sở 2/README.md` đang có tiêu đề `# ĐỀ BÀI: CẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT` (chép nhầm từ môn DSA).

## 8. Di chuyển nhanh giữa các chương

### Mục lục và thanh điều hướng (đã có sẵn trong 6 README)

- **Đầu mỗi README** có bảng **MỤC LỤC**: tên chương kèm số bài. Bấm vào tên chương để nhảy tới chương đó.
- **Dưới tiêu đề mỗi chương** có một dòng điều hướng:

  `⬆ Mục lục · ⬅ chương trước · chương sau ➡`

**Mỗi trình xem hiểu link theo một kiểu riêng, không có kiểu nào dùng chung được**, nên phải chọn một:

| Kiểu (`--style`) | Link trông như | Bấm được ở |
|---|---|---|
| `obsidian` (**đang dùng**) | `[VÒNG LẶP](#VÒNG%20LẶP)` (đúng chữ của tiêu đề) | Obsidian |
| `github` | `[VÒNG LẶP](#vòng-lặp)` (chữ thường, nối bằng `-`) | GitHub, preview của VS Code |

Đổi kiểu cho cả 6 README bằng một lệnh, đổi qua đổi lại thoải mái:

```bash
python tools/add_problem.py toc --style obsidian
```

```bash
python tools/add_problem.py toc --style github
```

Dùng nhầm kiểu thì Obsidian báo `Unable to find "..." in README`, còn GitHub/VS Code bấm vào không nhảy đi đâu.

Mục lục do script sinh ra, nằm giữa hai dòng `<!-- MUCLUC:START style=... -->` và `<!-- MUCLUC:END -->`, **đừng sửa tay**. Khi thêm bài bằng lệnh `add`, mục lục tự cập nhật và giữ nguyên kiểu link đang dùng. Nếu sửa README bằng tay (đổi tên chương, thêm chương...) thì chạy lại lệnh dưới đây (không cần `--style`, kiểu cũ được giữ):

```bash
python tools/add_problem.py toc
```

Muốn gỡ mục lục và thanh điều hướng ra (file trở về như cũ):

```bash
python tools/add_problem.py toc --remove
```

### Các cách có sẵn, không cần sửa file

| Ở đâu | Cách dùng |
|---|---|
| Obsidian — Outline | `Ctrl+P` → gõ **Outline: Show outline**: cây chương / bài ở thanh bên phải, bấm để nhảy, thu gọn từng chương được (không thấy lệnh thì bật **Outline** trong Settings → Core plugins) |
| Obsidian — tìm trong file | `Ctrl+F` rồi gõ mã bài (vd. `DSADQ01`) |
| VS Code — Outline | Thanh bên trái → Explorer → mục **OUTLINE**: cây chương / bài, bấm để nhảy, thu gọn từng chương được |
| VS Code — nhảy tới tiêu đề | `Ctrl+Shift+O` rồi gõ tên chương hoặc mã bài (vd. `DSADQ01`) |
| VS Code — về đầu / cuối file | `Ctrl+Home` / `Ctrl+End` |
| GitHub | Nút **Outline** (biểu tượng ☰) ở góc trên bên phải khung file: danh sách mọi tiêu đề, có ô lọc |
| Mọi nơi | `Ctrl+F` tìm theo mã bài |
