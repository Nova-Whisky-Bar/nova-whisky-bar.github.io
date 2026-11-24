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

1. 複製 `journal/_template/` 資料夾，改名為酒款英文代稱，例如 `journal/smws-53-496/`。
2. 打開 `index.html`，把「酒款名稱」「YYYY-MM-DD」「SLUG」全部替換，貼上 IG 繁中文案。
3. 刪掉 `<meta name="robots" content="noindex">` 這一行。
4. 在 `journal/index.html` 的清單加上一筆連結，在 `sitemap.xml` 加上一筆網址。

## 之後若購買網域

改 `build.py` 第一行的 BASE 後重新產生，並在 repository 根目錄加上 `CNAME` 檔。
