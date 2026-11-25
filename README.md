# Nova Whisky Bar 新星威士忌酒館 官網

網址：https://nova-whisky-bar.github.io/

## 部署到 GitHub Pages（第一次）

1. 用 Nova 專用的新 GitHub 帳號，建立名稱為 `帳號名稱.github.io` 的 repository（Public）。
   例如帳號是 novawhiskybar，repository 就叫 `novawhiskybar.github.io`，網站會在根網址。
2. 把這個資料夾裡的所有檔案（含隱藏檔 `.nojekyll`）上傳到 repository 根目錄。
3. Settings → Pages → Source 選 `Deploy from a branch`，Branch 選 `main`、資料夾 `/ (root)`，儲存。
4. 約 1–2 分鐘後打開官網網址確認。

## 上線後一定要做

1. Google Search Console（https://search.google.com/search-console）新增資源（官網根網址），
   用 HTML 標記驗證，提交 `sitemap.xml`。
2. Bing Webmaster Tools（https://www.bing.com/webmasters）可直接從 Search Console 匯入，提交 sitemap。
   ChatGPT 搜尋大量使用 Bing 的索引，這步不要省。
3. Google 商家檔案的「網站」欄位填官網網址。
4. Instagram @novawhisky、@drunkenkuo 的個人簡介連結改成官網。
5. 用 https://search.google.com/test/rich-results 測試首頁與 /faq/，確認結構化資料無錯誤。

## 新增品飲紀錄文章

文章由 `_source/build.py` 的 `POSTS` 產生，四語各一頁並互相對應（hreflang）：
`journal/SLUG/`、`en/journal/SLUG/`、`ja/journal/SLUG/`、`ko/journal/SLUG/`。

1. 酒瓶照片（直式 1080×1350）轉成 `assets/SLUG-720.jpg／.webp` 與 `assets/SLUG-1080.jpg／.webp`。
2. 在 `POSTS` 最上方新增一筆：slug、日期、照片前綴，以及四語的標題、導言、描述、酒款資料、文案段落、品飲紀錄。
   欄位格式參考 `journal/_template/` 與既有文章；沒有資料的欄位就不要寫。
3. 執行 `python3 build.py`，把輸出的 `site/` 內容複製到 repository 根目錄。
   各語文章列表、首頁文章區塊、sitemap.xml、llms.txt 會一起更新。

## 之後若購買網域

改 `build.py` 第一行的 BASE 後重新產生，並在 repository 根目錄加上 `CNAME` 檔。
