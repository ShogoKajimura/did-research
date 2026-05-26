# did-research

DID（解離性同一症）の脳機能研究プロジェクトの公開サイト。
研究紹介と実験参加者募集のランディングページ。

## 公開URL（予定）
`https://shogokajimura.github.io/did-research/`

## デプロイ手順（GitHub Pages）

1. ローカルで GitHub リポジトリを作成して push:
   ```bash
   cd /Users/shogo/Documents/Ollama/projects/did-research
   git init
   git add .
   git commit -m "Initial site"
   gh repo create ShogoKajimura/did-research --public --source=. --remote=origin --push
   ```
2. GitHub の Settings → Pages で **Source: Deploy from a branch, Branch: main / (root)** を選択して Save。
3. 数分後に `https://shogokajimura.github.io/did-research/` で公開される。

## 応募フォームの差し替え

`app.js` の `FORM_URL` を Google Forms の公開URLに書き換えるだけで，応募ボタンがフォームを開くようになります。

```js
const FORM_URL = "https://docs.google.com/forms/d/e/XXXXXXXX/viewform";
```

Google Forms の推奨設計（IRB 提出文面に揃えること）:
- 必須項目: お名前（フリガナでも可） / 連絡先メール / 希望拠点（関西／関東／どちらでも） / 簡単な自己紹介（人格状態のコントロール可否など）
- 任意項目: 通院先（具体名は不要，関西は「1年以上の治療継続中ですか」のチェックボックスのみ）
- 末尾: 「個人情報の取り扱いに同意します」チェック
- センシティブ情報（病名・服薬・既往歴）は **書かないでください** とフォーム冒頭に明記

## TODO（公開前に埋めるもの）

- [ ] `app.js` の `FORM_URL` に Google Forms URL を貼る
- [ ] `index.html` 内の倫理委員会承認番号を実番号に差し替え（現状「応募後にご案内」表記）
- [ ] 共同研究者の所属・敬称が正確か共著者と確認（京大／立正大の担当者名）
- [ ] X プロフィール（bio + 固定ポスト）に本サイト URL を貼る
- [ ] OGP 画像 `assets/og.png` を追加（現状 favicon と同じロゴ）

## ディレクトリ構成

```
did-research/
├── index.html       ランディングページ本体
├── styles.css       did-case-explorer と統一したデザインシステム
├── app.js           フォームURL差し替えとスムーススクロール
├── assets/
│   ├── logo.png     BS研究室ロゴ
│   ├── flyer_kanto.pdf   関東サイトの募集チラシ
│   └── flyer_kansai.pdf  関西サイトの募集チラシ
└── README.md
```

## 設計思想

- **DM経由でのリクルートを禁止**: X DM は暗号化されておらず，ご本人確認も困難なため，応募はフォーム + メールに限定。
- **個人情報の最小取得**: フォーム送信時はメール住所と希望拠点のみ。詳細な医療情報は折り返しのメール or 事前面談で取得。
- **当事者コミュニティへの配慮**: 「人格」「対象」等の表現は当事者の自認に寄り添う表現を優先。「症例」「被験者」等の言葉は使わない。
- **二重関係の回避**: X のフォローと研究参加同意は無関係であることを明記。
- **デザイン共通化**: 既存の did-case-explorer と CSS 変数・フォントを揃え，将来 OCR/Explorer サービスへの相互リンクを自然に張れるようにしている。
