#!/usr/bin/env python3
"""
A4 recruitment flyers (Kansai/Kanto). Unified policy:
- Common participation conditions (union of both sites)
- 5,000 JPY/hr + transport, up to 3hr/visit
- Pre-meeting with treating psychiatrist required
"""
import os
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.utils import ImageReader

pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
FONT = "HeiseiKakuGo-W5"

# Twin Streams palette
INK = (0x10 / 255, 0x23 / 255, 0x2a / 255)
INK_SOFT = (0x54 / 255, 0x69 / 255, 0x70 / 255)
ACCENT = (0x2f / 255, 0x6f / 255, 0x73 / 255)
ACCENT_DEEP = (0x16 / 255, 0x4b / 255, 0x53 / 255)
ACCENT_SOFT = (0xb8 / 255, 0xd8 / 255, 0xd4 / 255)
IRIS = (0x73 / 255, 0x7b / 255, 0x9f / 255)
BG = (0xee / 255, 0xf5 / 255, 0xf3 / 255)


def wrap(text, font, size, max_w):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if stringWidth(cur + ch, font, size) > max_w:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def make(site, out_path):
    W, H = A4
    c = canvas.Canvas(out_path, pagesize=A4)

    # backdrop
    c.setFillColorRGB(*BG); c.rect(0, 0, W, H, fill=1, stroke=0)

    # ---- header band ----
    band_h = 92
    c.setFillColorRGB(*ACCENT_DEEP); c.rect(0, H - band_h, W, band_h, fill=1, stroke=0)

    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
    if os.path.exists(logo_path):
        c.drawImage(ImageReader(logo_path), 24, H - band_h + 14, width=100, height=46, mask="auto")

    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT, 18)
    c.drawString(146, H - 30, "脳機能計測実験に")
    c.drawString(146, H - 52, "ご興味をお持ちの方へ")
    c.setFont(FONT, 10)
    c.drawString(146, H - 70, "ブレインサイエンス研究室（京都工芸繊維大学）")

    # site badge
    badge = "関西サイト" if site == "kansai" else "関東サイト"
    c.setFillColorRGB(*ACCENT_SOFT)
    c.roundRect(W - 130, H - 46, 106, 22, 11, fill=1, stroke=0)
    c.setFillColorRGB(*ACCENT_DEEP); c.setFont(FONT, 11)
    c.drawCentredString(W - 77, H - 32, badge)

    # ---- body layout ----
    margin = 24
    label_w = 56
    content_x = margin + label_w + 10
    content_w = W - content_x - margin
    y = H - band_h - 18
    bottom_limit = 60  # footer space

    def section(label, body_lines, bg=None, padding=10, font=FONT, size=9.5, line_h=13):
        nonlocal y
        # Compose actual lines (lists or simple)
        flat = []
        for entry in body_lines:
            if isinstance(entry, tuple):
                kind, text = entry
                if kind == "para":
                    for para in text.split("\n"):
                        flat.extend(("p", l) for l in wrap(para, font, size, content_w - padding * 2))
                elif kind == "bullet":
                    for item in text:
                        wrapped = wrap(item, font, size, content_w - padding * 2 - 14)
                        for i, l in enumerate(wrapped):
                            flat.append(("b" if i == 0 else "bc", l))
            else:
                for para in entry.split("\n"):
                    flat.extend(("p", l) for l in wrap(para, font, size, content_w - padding * 2))
        body_h = len(flat) * line_h + padding * 2
        # if doesn't fit, allow it to overflow — caller should monitor
        # draw body bg
        if bg is not None:
            c.saveState()
            c.setFillColorRGB(*bg); c.setFillAlpha(0.18)
            c.roundRect(content_x, y - body_h, content_w, body_h, 6, fill=1, stroke=0)
            c.restoreState()
        else:
            c.setFillColorRGB(1, 1, 1)
            c.setFillAlpha(0.55)
            c.saveState()
            c.setFillColorRGB(1, 1, 1); c.setFillAlpha(0.55)
            c.roundRect(content_x, y - body_h, content_w, body_h, 6, fill=1, stroke=0)
            c.restoreState()
        # body text
        c.setFillColorRGB(*INK); c.setFont(font, size)
        cy = y - padding
        for kind, text in flat:
            if kind == "b":
                c.setFillColorRGB(*ACCENT)
                c.circle(content_x + padding + 3, cy - 4, 2, fill=1, stroke=0)
                c.setFillColorRGB(*INK)
                c.drawString(content_x + padding + 14, cy - line_h + 4, text)
            elif kind == "bc":
                c.drawString(content_x + padding + 14, cy - line_h + 4, text)
            else:
                c.drawString(content_x + padding, cy - line_h + 4, text)
            cy -= line_h
        # label box (full body height, accent fill, label centered vertically)
        c.setFillColorRGB(*ACCENT)
        c.roundRect(margin, y - body_h, label_w, body_h, 6, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1); c.setFont(FONT, 12)
        chars = list(label)
        # Auto-size vertical char step so label fits inside box
        char_step = min(15, max(11, (body_h - 14) / max(len(chars), 1)))
        total = char_step * (len(chars) - 1)
        start = y - body_h / 2 + total / 2 - char_step / 2 + 4
        for i, ch in enumerate(chars):
            c.drawCentredString(margin + label_w / 2, start - i * char_step, ch)
        y -= body_h + 8

    # ===== sections =====

    # 実験場所
    if site == "kansai":
        place = "京都大学附属病院 西構内\n公共交通機関でお越しください。最寄駅は京阪 神宮丸太町駅です。\n詳細は実験参加時にお伝えします。"
    else:
        place = "東京大学 本郷キャンパス\n公共交通機関でお越しください。最寄駅は都営大江戸線 本郷三丁目駅です。\n詳細は実験参加時にお伝えします。"
    section("実験場所", [place])

    # 実験内容
    intro = "（1）何もしていない状態，（2）人格が交代する際の脳機能，（3）簡単な課題を行っている際の脳機能を，MRI を用いて複数回計測します（①②は全員，③は可能な方のみ）。"
    items = [
        "① 安静時：MRI 内の十字マークを見ながらじっとしている状態の脳機能を 10 分程度計測します。",
        "② 人格交代時：MRI 内で人格交代を行っていただき，その際の脳機能を計測します。",
        "③ 課題時：人格間で差のあるもの（好き嫌い／読み書き能力 等）に関する写真・映像を MRI 内でご覧いただき，各人格状態で 10 分程度計測します。",
    ]
    section("実験内容", [("para", intro), ("bullet", items)])

    # 募集対象
    crit = [
        "高い解離傾向があり，一つの人格状態から別の状態へのコントロールが大きな苦痛を伴わずに可能な方",
        "現在の医療機関で 1 年以上にわたって治療を継続中の方",
        "MRI 撮像が実施可能な方",
        "閉所恐怖症でない方",
        "体内・体表に金属がない方（タトゥー等を含む）",
        "検査時に髪を派手な色に染めていない方",
    ]
    section("募集対象", [("bullet", crit)])

    # 事前連絡 (担当医との事前ミーティング、ラベルは短く)
    coord = (
        "ご応募から実験までの間に，研究者（梶村）から担当の精神科医の先生にご連絡し，研究参加についてご相談・ご了承を得たうえで，改めて参加のご案内をさせていただきます。研究と日常の治療がお互いに干渉しないようにし，ご本人の安全を最優先するための手順です。"
    )
    section("事前連絡", [coord], bg=IRIS)

    # 謝礼
    fee = "5,000 円／時間（実験時間：1 回あたり最大 3 時間，無理のない範囲で）\n交通費は別途お支払いします。何度でも繰り返しご参加いただけます。"
    section("謝　　礼", [fee])

    # 参加方法 (与えるURL + QRは別配置)
    apply_text = (
        "下記の公式サイトをご覧いただき，応募フォーム（準備中）または下記メールにてご連絡ください。"
        "\nhttps://shogokajimura.github.io/did-research/"
    )
    section("参加方法", [apply_text])

    # 実験担当
    pi = (
        "梶村 昇吾　京都工芸繊維大学 情報工学・人間科学系 准教授（ブレインサイエンス研究室）\n"
        "Email: kajimura@kit.ac.jp　／　researchmap: https://researchmap.jp/Shogo_KAJIMURA"
    )
    section("実験担当", [pi], size=9, line_h=12)

    # ---- QR code in lower-right corner (overlays the layout) ----
    qr = qrcode.make("https://shogokajimura.github.io/did-research/")
    qr_path = "/tmp/did_research_qr.png"
    qr.save(qr_path)
    qr_size = 72
    qr_x = W - qr_size - margin
    qr_y = bottom_limit + 6
    # Drop a white card behind the QR for contrast
    c.setFillColorRGB(1, 1, 1)
    c.roundRect(qr_x - 6, qr_y - 6, qr_size + 12, qr_size + 22, 6, fill=1, stroke=0)
    c.drawImage(ImageReader(qr_path), qr_x, qr_y + 6, width=qr_size, height=qr_size, mask="auto")
    c.setFillColorRGB(*INK_SOFT); c.setFont(FONT, 7)
    c.drawCentredString(qr_x + qr_size / 2, qr_y - 1, "公式サイト QR")

    # ---- footer ----
    c.setFillColorRGB(*INK_SOFT); c.setFont(FONT, 8)
    c.drawString(margin, 28, "京都大学・京都工芸繊維大学・立正大学 共同研究チーム")
    c.drawString(margin, 16, "※ご相談は X の DM ではなく，公式サイト または kajimura@kit.ac.jp 宛のメールでお願いいたします。")

    c.showPage()
    c.save()


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    make("kansai", os.path.join(out_dir, "flyer_kansai.pdf"))
    make("kanto", os.path.join(out_dir, "flyer_kanto.pdf"))
    print("done")
