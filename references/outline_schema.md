# outline.json 格式說明

步驟 2 的產出，是步驟 3 逐頁生成的唯一依據。每個物件代表一頁投影片。

```json
{
  "meta": {
    "title": "簡報標題",
    "audience": "投資人",
    "duration_minutes": 15,
    "language": "zh-TW",
    "style_notes": "正式、簡潔、深色系配色"
  },
  "slides": [
    {
      "index": 1,
      "type": "title",
      "title": "2026 年度市場策略提案",
      "subtitle": "OO 部門 / 2026.07",
      "content_points": [],
      "data": [],
      "image_ref": null,
      "notes_for_designer": "開場頁，不要放太多資訊"
    },
    {
      "index": 2,
      "type": "agenda",
      "title": "本次報告大綱",
      "content_points": ["市場現況", "競爭分析", "策略建議", "執行時程"],
      "data": [],
      "image_ref": null
    },
    {
      "index": 3,
      "type": "content",
      "title": "市場現況：成長趨緩但區域分化明顯",
      "content_points": [
        "整體市場年成長率降至 3.5%（前年 8.2%）",
        "東南亞市場逆勢成長 12%"
      ],
      "data": [],
      "image_ref": null,
      "source_section": "市場現況"
    },
    {
      "index": 4,
      "type": "chart",
      "title": "近三年區域成長率比較",
      "content_points": [],
      "data": {
        "chart_type": "bar",
        "categories": ["2024", "2025", "2026"],
        "series": {"東南亞": [6, 9, 12], "整體市場": [8.2, 5.1, 3.5]}
      },
      "image_ref": null,
      "source_section": "市場現況"
    },
    {
      "index": 5,
      "type": "image_highlight",
      "title": "新產品線實機展示",
      "content_points": ["強調輕量化設計"],
      "data": [],
      "image_ref": "extracted_images/img_0003.png",
      "source_section": "產品介紹"
    },
    {
      "index": 6,
      "type": "section_divider",
      "title": "競爭分析",
      "content_points": [],
      "data": [],
      "image_ref": null
    },
    {
      "index": 7,
      "type": "closing",
      "title": "總結與下一步",
      "content_points": ["Q3 啟動東南亞市場試點", "Q4 檢視成效並決定擴大規模"],
      "data": [],
      "image_ref": null
    }
  ]
}
```

## 欄位說明

- `type`：頁面類型，決定步驟 3 該用哪種版面模板。常見值：
  `title`（標題頁）、`agenda`（議程頁）、`section_divider`（分節頁）、
  `content`（純文字重點頁）、`chart`（數據圖表頁）、
  `image_highlight`（圖片為主、文字為輔）、`comparison`（左右對比頁）、
  `closing`（總結/行動呼籲頁）。可依實際需求擴充，但同一份簡報內同類型頁面
  版面要一致。
- `content_points`：條列重點，建議 3-6 點以內，這裡放的是「濃縮後」的重點，
  不是原文照抄。
- `data`：如果是 `chart` 類型，放圖表所需的結構化數據，方便步驟 3 直接生成圖表。
- `image_ref`：對應步驟 2 內容清單裡整理出的圖片路徑；如果這頁需要圖但目前沒有
  現成圖片可用，先留 `null` 並在步驟 3 記錄進 `pending_visuals.md`。
- `source_section`：對應回文件的哪個章節，方便追溯與校對事實正確性。
