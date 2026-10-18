#!/usr/bin/env python3
"""Thêm bài tập vào README của từng môn, giữ đúng format sẵn có của kho.

Cách dùng nhanh:
    python tools/add_problem.py list                       # các môn + số bài
    python tools/add_problem.py list -k thcs2              # các chương của một môn
    python tools/add_problem.py find C01001                # mã bài đã có chưa, nằm ở đâu
    python tools/add_problem.py add bai_moi.md -k thcs2 -c "vòng lặp" --dry-run
    python tools/add_problem.py add bai_moi.md -k thcs2 -c "vòng lặp"
    python tools/add_problem.py toc --style obsidian       # tạo / cập nhật mục lục (obsidian | github)
    python tools/add_problem.py toc --remove               # gỡ mục lục

Xem HUONG_DAN_THEM_BAI.md ở thư mục gốc để biết format file nháp.
"""
import argparse
import html
import re
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PROBLEM_RE = re.compile(r'^### ([^*\s]\S*) - (.+?)\s*$')
CHAPTER_RE = re.compile(r'^## (.+?)\s*$')
FENCE_RE = re.compile(r'^\s*```\s*(input|output|in|out)\s*$', re.I)
CLOSE_RE = re.compile(r'^\s*```\s*$')
IMAGE_RE = re.compile(r'!\[[^\]]*\]\(\s*<?([^)\s>]+)>?')
COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
ATX_RE = re.compile(r'^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*$')
CODE_FENCE_RE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')

TOC_START = '<!-- MUCLUC:START style={} (tự sinh bởi "python tools/add_problem.py toc", đừng sửa tay) -->'
TOC_END = '<!-- MUCLUC:END -->'
NAV_MARK = '<!-- nav -->'
TOC_STYLES = ('obsidian', 'github')
# Obsidian coi các ký tự này như dấu cách khi so khớp link tới tiêu đề (stripHeading trong app)
OBSIDIAN_STRIP_RE = re.compile(r'[!"#$%&()*+,.:;<=>?@^`{|}~/\[\]\\\r\n]')

# Tên viết tắt -> tên thư mục môn học (so sánh không dấu, không phân biệt hoa thường)
ALIASES = {
    'c': 'Tin học cơ sở 2',
    'thcs2': 'Tin học cơ sở 2',
    'tin hoc co so': 'Tin học cơ sở 2',
    'cpp': 'Ngôn ngữ lập trình C++',
    'c++': 'Ngôn ngữ lập trình C++',
    'dsa': 'Cấu trúc dữ liệu và giải thuật (DSA)',
    'ctdl': 'Cấu trúc dữ liệu và giải thuật (DSA)',
    'ctdlgt': 'Cấu trúc dữ liệu và giải thuật (DSA)',
    'oop': 'Lập trình hướng đối tượng',
    'java': 'Lập trình hướng đối tượng',
    'lthdt': 'Lập trình hướng đối tượng',
    'py': 'Lập trình với Python',
    'python': 'Lập trình với Python',
    'tnc': 'Thuật toán nâng cao - 2024',
    'ttnc': 'Thuật toán nâng cao - 2024',
}


def fold(s):
    """Bỏ dấu, gộp khoảng trắng, chữ thường: 'Vòng  Lặp' -> 'vong lap'."""
    s = unicodedata.normalize('NFD', s.replace('đ', 'd').replace('Đ', 'D'))
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r'\s+', ' ', s).strip().lower()


def die(msg):
    print(f'Lỗi: {msg}', file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------- môn học

def courses():
    return sorted(d for d in ROOT.iterdir()
                  if d.is_dir() and not d.name.startswith('.') and (d / 'README.md').is_file())


def resolve_course(arg):
    all_courses = courses()
    key = fold(arg)
    target = ALIASES.get(key)
    if target:
        key = fold(target)
    exact = [d for d in all_courses if fold(d.name) == key]
    if exact:
        return exact[0]
    partial = [d for d in all_courses if key in fold(d.name)]
    if len(partial) == 1:
        return partial[0]
    names = '\n  '.join(d.name for d in all_courses)
    if partial:
        die(f'"{arg}" khớp nhiều môn, hãy ghi rõ hơn:\n  ' + '\n  '.join(d.name for d in partial))
    die(f'không tìm thấy môn "{arg}". Các môn hiện có:\n  {names}')


# ---------------------------------------------------------------- README

class Readme:
    def __init__(self, path):
        self.path = path
        raw = path.read_bytes().decode('utf-8')
        self.eol = '\r\n' if '\r\n' in raw else '\n'
        text = raw.replace('\r\n', '\n')
        self.trailing_newline = text.endswith('\n')
        self.lines = text.split('\n')
        if self.trailing_newline:
            self.lines.pop()

    def save(self):
        text = '\n'.join(self.lines) + ('\n' if self.trailing_newline else '')
        self.path.write_bytes(text.replace('\n', self.eol).encode('utf-8'))

    def chapters(self):
        """[(tên chương, dòng bắt đầu, dòng kết thúc (không gồm))]"""
        heads = [(i, m.group(1)) for i, line in enumerate(self.lines)
                 if (m := CHAPTER_RE.match(line))]
        return [(name, start, heads[k + 1][0] if k + 1 < len(heads) else len(self.lines))
                for k, (start, name) in enumerate(heads)]

    def problems(self, start=0, end=None):
        """[(mã, tên, dòng header)] trong khoảng [start, end)"""
        end = len(self.lines) if end is None else end
        return [(m.group(1), m.group(2), i) for i in range(start, end)
                if (m := PROBLEM_RE.match(self.lines[i]))]

    def block_end(self, header_idx):
        """Dòng kết thúc của bài bắt đầu ở header_idx (bài kế tiếp, chương kế tiếp hoặc hết file)."""
        for i in range(header_idx + 1, len(self.lines)):
            if PROBLEM_RE.match(self.lines[i]) or CHAPTER_RE.match(self.lines[i]):
                return i
        return len(self.lines)

    def find_code(self, code):
        for c, name, idx in self.problems():
            if c.upper() == code.upper():
                return idx, name
        return None

    def chapter_of(self, line_idx):
        for name, start, end in self.chapters():
            if start <= line_idx < end:
                return name
        return None

    def find_chapter(self, arg):
        key = fold(arg)
        chs = self.chapters()
        exact = [c for c in chs if fold(c[0]) == key]
        if exact:
            return exact[0]
        partial = [c for c in chs if key in fold(c[0])]
        if len(partial) == 1:
            return partial[0]
        return partial or None


# ---------------------------------------------------------------- mục lục

def gh_slug(text):
    """Anchor GitHub sinh cho một tiêu đề: '## VÒNG LẶP' -> 'vòng-lặp'."""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[\\]([!-/:-@\[-`{-~])', r'\1', text)  # bỏ dấu \ escape
    text = html.unescape(text).strip().lower()
    keep = ''.join(ch for ch in text
                   if ch in ' -' or unicodedata.category(ch)[0] in 'LM'
                   or unicodedata.category(ch) in ('Nd', 'Nl', 'Pc'))
    return keep.replace(' ', '-')


def heading_slugs(lines):
    """{chỉ số dòng: anchor} của mọi tiêu đề, đánh số trùng (-1, -2...) giống GitHub."""
    seen, slugs, fence = {}, {}, None
    for i, line in enumerate(lines):
        m = CODE_FENCE_RE.match(line)
        if m:
            tok, rest = m.group(1), m.group(2)
            if fence is None and not (tok[0] == '`' and '`' in rest):
                fence = tok
                continue
            if fence and tok[0] == fence[0] and len(tok) >= len(fence) and not rest.strip():
                fence = None
                continue
        if fence:
            continue
        m = ATX_RE.match(line)
        if not m:
            continue
        text = re.sub(r'(^|[ \t])#+[ \t]*$', '', m.group(2) or '')
        base = slug = gh_slug(text)
        while slug in seen:
            seen[base] += 1
            slug = f'{base}-{seen[base]}'
        seen[slug] = 0
        slugs[i] = slug
    return slugs


def strip_toc(lines):
    """Bỏ khối mục lục và các dòng điều hướng chương đã sinh trước đó."""
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('<!-- MUCLUC:START'):
            j = i
            while j < len(lines) and lines[j].strip() != TOC_END:
                j += 1
            if out and not out[-1].strip():
                out.pop()
            i = j + 1
            continue
        if line.rstrip().endswith(NAV_MARK):
            if out and not out[-1].strip():
                out.pop()
            i += 1
            continue
        out.append(line)
        i += 1
    return out


def toc_style(rd):
    """Kiểu link của mục lục đang có trong README, None nếu chưa có mục lục."""
    for line in rd.lines:
        if line.startswith('<!-- MUCLUC:START'):
            m = re.search(r'style=(\w+)', line)
            return m.group(1) if m else 'github'
    return None


def obsidian_fragment(heading):
    """Link Obsidian tới tiêu đề: '# ĐỀ BÀI: C++' -> 'ĐỀ%20BÀI%20C'."""
    text = re.sub(r'\s+', ' ', OBSIDIAN_STRIP_RE.sub(' ', heading)).strip()
    return text.replace(' ', '%20')


def build_toc(rd, style):
    """Chèn mục lục dưới tiêu đề '#' và dòng điều hướng dưới mỗi chương.

    style='github': anchor kiểu GitHub / VS Code (chữ thường, nối bằng '-').
    style='obsidian': link theo đúng chữ của tiêu đề, kiểu Obsidian hiểu.
    """
    rd.lines = strip_toc(rd.lines)
    slugs = heading_slugs(rd.lines)
    chapters = rd.chapters()
    h1 = next((i for i, l in enumerate(rd.lines) if l.startswith('# ')), None)

    def target(idx):
        if style == 'obsidian':
            text = re.sub(r'^#+\s+', '', rd.lines[idx]).strip()
            return '#' + obsidian_fragment(text)
        return '#' + slugs[idx]

    top = target(h1) if h1 is not None else '#'
    toc = [TOC_START.format(style), '',
           f'**MỤC LỤC** · {len(chapters)} chương · {len(rd.problems())} bài', '',
           '| # | Chương | Số bài |', '|---:|---|---:|']
    for k, (name, start, end) in enumerate(chapters, 1):
        toc.append(f'| {k} | [{name}]({target(start)}) | {len(rd.problems(start, end))} |')
    toc += ['', TOC_END]

    # chèn từ dưới lên để chỉ số dòng phía trên không bị lệch
    for k in range(len(chapters) - 1, -1, -1):
        name, start, _ = chapters[k]
        nav = [f'[⬆ Mục lục]({top})']
        if k > 0:
            nav.append(f'[⬅ {chapters[k - 1][0]}]({target(chapters[k - 1][1])})')
        if k + 1 < len(chapters):
            nav.append(f'[{chapters[k + 1][0]} ➡]({target(chapters[k + 1][1])})')
        block = ['', ' · '.join(nav) + ' ' + NAV_MARK]
        if start + 1 < len(rd.lines) and rd.lines[start + 1].strip():
            block.append('')
        rd.lines[start + 1:start + 1] = block
    at = h1 + 1 if h1 is not None else 0
    rd.lines[at:at] = [''] + toc if h1 is not None else toc + ['']


# ---------------------------------------------------------------- chuyển đổi file nháp

def escape_cell(line):
    """Escape một dòng input/output để đặt an toàn vào ô bảng Markdown."""
    line = line.rstrip()
    line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    line = re.sub(r'([\\`*_\[\]~|])', r'\\\1', line)
    # giữ khoảng trắng đầu dòng / nhiều dấu cách liền nhau (vd. bài in hình)
    line = re.sub(r'^ +', lambda m: '&nbsp;' * len(m.group()), line)
    line = re.sub(r' {2,}', lambda m: ' ' + '&nbsp;' * (len(m.group()) - 1), line)
    return line


def cell(lines):
    while lines and not lines[0].strip():
        lines = lines[1:]
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return '<br>'.join(escape_cell(l) for l in lines) or ' '


def convert_samples(lines):
    """Gom các khối ```input / ```output liên tiếp thành một bảng ví dụ."""
    out, samples, i = [], [], 0

    def flush():
        if not samples:
            return
        rows, pending = [], None
        for kind, body in samples:
            if kind == 'in':
                if pending is not None:
                    rows.append((pending, []))
                pending = body
            else:
                rows.append((pending or [], body))
                pending = None
        if pending is not None:
            rows.append((pending, []))
        out.extend(['| **Input** | **Output** |', '|---|---|'])
        out.extend(f'| {cell(a)} | {cell(b)} |' for a, b in rows)
        out.append('')
        samples.clear()

    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if m:
            kind = 'in' if m.group(1).lower().startswith('in') else 'out'
            j = i + 1
            while j < len(lines) and not CLOSE_RE.match(lines[j]):
                j += 1
            if j == len(lines):
                die(f'khối ```{m.group(1)} mở ở dòng nháp "{lines[i]}" nhưng không có ``` đóng')
            samples.append((kind, lines[i + 1:j]))
            i = j + 1
            continue
        if samples and not lines[i].strip():
            i += 1  # dòng trống giữa các khối ví dụ
            continue
        flush()
        out.append(lines[i])
        i += 1
    flush()
    return out


def parse_draft(path):
    text = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    text = COMMENT_RE.sub('', text)
    lines = text.split('\n')
    heads = [i for i, l in enumerate(lines) if PROBLEM_RE.match(l.strip())]
    if not heads:
        die(f'{path} không có dòng tiêu đề dạng "### MÃBÀI - TÊN BÀI"')
    problems = []
    for k, h in enumerate(heads):
        m = PROBLEM_RE.match(lines[h].strip())
        code, name = m.group(1).upper(), m.group(2).strip().upper()
        body = lines[h + 1:heads[k + 1] if k + 1 < len(heads) else len(lines)]
        body = convert_samples([l.rstrip() for l in body])
        # gộp nhiều dòng trống liên tiếp, bỏ dòng trống đầu/cuối
        cleaned = []
        for l in body:
            if not l.strip() and (not cleaned or not cleaned[-1].strip()):
                continue
            cleaned.append(l)
        while cleaned and not cleaned[-1].strip():
            cleaned.pop()
        problems.append((code, name, [f'### {code} - {name}', ''] + cleaned + ['']))
    return problems


def rel(path):
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def handle_images(block, course_dir, draft_dir, copy=True):
    """Ảnh tham chiếu ./img/... : nếu chưa có trong môn mà có cạnh file nháp thì copy sang."""
    for line in block:
        for ref in IMAGE_RE.findall(line):
            if re.match(r'^[a-z]+://', ref, re.I) or ref.startswith('data:'):
                continue
            dest = (course_dir / ref).resolve()
            if dest.exists():
                continue
            src = (draft_dir / ref).resolve()
            if not src.exists():
                src = (draft_dir / Path(ref).name).resolve()
            if src.exists():
                if copy:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dest)
                print(f'  + {"copy" if copy else "sẽ copy"} ảnh {rel(src)} -> {rel(dest)}')
            else:
                print(f'  ! Cảnh báo: không tìm thấy ảnh "{ref}" (cần đặt tại {rel(dest)})')


# ---------------------------------------------------------------- lệnh

def cmd_list(args):
    if args.course:
        d = resolve_course(args.course)
        rd = Readme(d / 'README.md')
        print(f'{d.name}:')
        for name, start, end in rd.chapters():
            print(f'  {len(rd.problems(start, end)):4d} bài  ## {name}')
        return
    for d in courses():
        rd = Readme(d / 'README.md')
        print(f'{len(rd.problems()):4d} bài  {len(rd.chapters()):3d} chương  {d.name}')


def cmd_find(args):
    found = False
    for d in courses():
        rd = Readme(d / 'README.md')
        hit = rd.find_code(args.code)
        if hit:
            idx, name = hit
            found = True
            print(f'{d.name}/README.md:{idx + 1}  ## {rd.chapter_of(idx)}  ->  {args.code.upper()} - {name}')
    if not found:
        print(f'Chưa có bài {args.code.upper()} trong kho.')


def cmd_add(args):
    draft = Path(args.draft).resolve()
    if not draft.is_file():
        die(f'không thấy file nháp {args.draft}')
    course_dir = resolve_course(args.course)
    rd = Readme(course_dir / 'README.md')
    added = []

    for code, name, block in parse_draft(draft):
        existing = rd.find_code(code)
        chapter_arg = args.chapter
        if existing:
            if not args.replace:
                die(f'{code} đã có ở dòng {existing[0] + 1} (chương "{rd.chapter_of(existing[0])}"). '
                    f'Dùng --replace nếu muốn ghi đè.')
            chapter_arg = chapter_arg or rd.chapter_of(existing[0])
        if not chapter_arg:
            die('thiếu -c/--chapter (xem danh sách bằng: list -k "<môn>")')

        found = rd.find_chapter(chapter_arg)
        if isinstance(found, list):
            die(f'"{chapter_arg}" khớp nhiều chương:\n  ' + '\n  '.join(c[0] for c in found))
        if found is None and not args.new_chapter:
            names = '\n  '.join(c[0] for c in rd.chapters())
            die(f'môn "{course_dir.name}" chưa có chương "{chapter_arg}". Các chương hiện có:\n  {names}\n'
                f'Thêm --new-chapter để tạo chương mới ở cuối file.')

        if existing:
            start = existing[0]
            del rd.lines[start:rd.block_end(start)]
            found = rd.find_chapter(chapter_arg)  # chỉ số dòng đã thay đổi

        if found is None:
            title = chapter_arg.strip().upper()
            if rd.lines and rd.lines[-1].strip():
                rd.lines.append('')
            rd.lines += [f'## {title}', '']
            found = (title, len(rd.lines) - 2, len(rd.lines))
            print(f'  + tạo chương mới "## {title}"')

        ch_name, ch_start, ch_end = found
        pos = ch_end
        for c, _, idx in rd.problems(ch_start, ch_end):
            if c.upper() > code:
                pos = idx
                break
        if pos > 0 and rd.lines[pos - 1].strip():
            block = [''] + block
        if pos == len(rd.lines):
            block = block[:-1]  # cuối file: không thêm dòng trống thừa
        rd.lines[pos:pos] = block

        action = 'Thay' if existing else 'Thêm'
        print(f'{action} {code} - {name}  ->  {course_dir.name} / ## {ch_name} (dòng {pos + 1})')
        if args.dry_run:
            print('-' * 60)
            print('\n'.join(block).strip('\n'))
            print('-' * 60)
        added.append(block)

    # chỉ đụng tới ảnh / file khi mọi bài trong nháp đều hợp lệ
    for block in added:
        handle_images(block, course_dir, draft.parent, copy=not args.dry_run)
    if args.dry_run:
        print('(dry-run: chưa ghi gì vào file)')
    else:
        style = toc_style(rd)
        if style:
            build_toc(rd, style)  # cập nhật số bài / chương mới trong mục lục, giữ kiểu link cũ
        rd.save()


def cmd_toc(args):
    for d in [resolve_course(args.course)] if args.course else courses():
        rd = Readme(d / 'README.md')
        before = list(rd.lines)
        if args.remove:
            rd.lines = strip_toc(rd.lines)
        else:
            build_toc(rd, args.style or toc_style(rd) or 'obsidian')
        if rd.lines == before:
            print(f'  (không đổi)  {d.name}')
            continue
        rd.save()
        print(f'{"Gỡ mục lục" if args.remove else "Cập nhật mục lục"}: {d.name} ({len(rd.chapters())} chương)')


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')  # console Windows mặc định không phải UTF-8

    p = argparse.ArgumentParser(description='Thêm bài tập vào kho Code_PTIT theo đúng format.')
    sub = p.add_subparsers(dest='cmd', required=True)

    pl = sub.add_parser('list', help='liệt kê môn / chương')
    pl.add_argument('-k', '--course', help='tên môn (vd. thcs2, cpp, dsa, oop, py, tnc)')
    pl.set_defaults(func=cmd_list)

    pf = sub.add_parser('find', help='tìm một mã bài trong toàn kho')
    pf.add_argument('code')
    pf.set_defaults(func=cmd_find)

    pa = sub.add_parser('add', help='thêm bài từ file nháp')
    pa.add_argument('draft', help='file .md chứa một hoặc nhiều bài')
    pa.add_argument('-k', '--course', required=True, help='tên môn (vd. thcs2, cpp, dsa, oop, py, tnc)')
    pa.add_argument('-c', '--chapter', help='tên chương (## ...), gõ không dấu cũng được')
    pa.add_argument('--new-chapter', action='store_true', help='tạo chương mới nếu chưa có')
    pa.add_argument('--replace', action='store_true', help='ghi đè nếu mã bài đã tồn tại')
    pa.add_argument('--dry-run', action='store_true', help='chỉ in ra kết quả, không ghi file')
    pa.set_defaults(func=cmd_add)

    pt = sub.add_parser('toc', help='tạo / cập nhật mục lục và thanh điều hướng giữa các chương')
    pt.add_argument('-k', '--course', help='chỉ làm cho một môn (mặc định: tất cả)')
    pt.add_argument('--style', choices=TOC_STYLES,
                    help='kiểu link: obsidian, hoặc github (GitHub + VS Code). Mặc định giữ kiểu đang dùng')
    pt.add_argument('--remove', action='store_true', help='gỡ mục lục ra khỏi README')
    pt.set_defaults(func=cmd_toc)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
