# 🎄 聖誕明信片祭

「陽光草地・明信片紀念」聖誕節特別版 — 將雪山夕照明信片加入聖誕氣氛的靜態網頁。

## 成品

| 檔案 | 說明 |
| --- | --- |
| `postcard_christmas.jpg` | 經典款：飄雪、聖誕燈串、裝飾球、金色邊框 |
| `image_with_qr_christmas.jpg` | QR 款：相同裝飾，左上角 QR code 完整保留可掃描 |
| `index.html` | 聖誕主題網頁（飄雪動畫、頂部燈串、卡片展示、祝福語） |

原始圖片為 `postcard.jpg` 與 `image_with_qr.jpg`。

## 聖誕元素

- 🎅 **圖片**：程式化加入飄雪（近景散景＋遠景細雪）、垂吊裝飾球、LED 燈串、四芒星光點、紅金雙線邊框與雪花角飾
- ❄️ **網頁**：CSS/JS 飄雪動畫、頂部閃爍燈串、金色獎章標題、懸浮卡片、聖誕紅綠漸層祝福區
- 📷 **QR 保護**：所有裝飾皆避開左上角 QR 安全區（200×200），掃描功能不受影響

## 本地開啟

直接用瀏覽器開啟 `index.html`，或啟動本地伺服器：

```bash
python -m http.server 8000
# 瀏覽器開啟 http://localhost:8000
```

## 重新產生裝飾圖片

```bash
pip install pillow
python decorate_christmas.py
```

## 技術

純 HTML / CSS / JavaScript，無任何外部依賴；圖片處理使用 Python + Pillow。
