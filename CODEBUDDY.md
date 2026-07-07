# CODEBUDDY.md This file provides guidance to CodeBuddy when working with code in this repository.

## 常用命令

### 本地预览
项目为零依赖纯静态页面，直接用浏览器打开 `index.html`、`fanzhendong.html` 或 `wangmanyu.html` 即可预览，无需构建或安装任何工具。

### 更新图片轮播
向 `images/fanzhendong/` 或 `images/wangmanyu/` 添加/删除图片后，运行以下命令自动更新 HTML 中的轮播幻灯片：
```bash
python build.py
```
脚本按文件名排序扫描文件夹，在 `<!-- HERO_SLIDES_START -->` 和 `<!-- HERO_SLIDES_END -->` 标记之间生成轮播 HTML，第一张图片默认设为当前显示页。

### Git 提交与推送
```bash
git add -A
git commit -m "描述信息"
git push
```

## 架构概述

### 总体设计
这是一个纯静态的双球员粉丝致敬网站，包含两个结构完全相同但内容不同的球员页面。项目零依赖、零构建步骤：CSS 和 JS 均内联在 HTML 中，`build.py` 仅用于管理轮播图片。

### 入口与导航
- `index.html`：EdgeOne Pages 部署的入口点，通过 `<meta http-equiv="refresh">` 和 JS `location.href` 双重跳转到 `fanzhendong.html`
- `fanzhendong.html` 和 `wangmanyu.html`：各自左上角的固定毛玻璃导航标签通过普通 `<a>` 链接互相跳转，当前页面的标签标记 `class="tab active"`

### 页面结构（每个球员页面完全相同）
两个 HTML 文件共享相同的 CSS（`:root` 变量 → 组件样式 → 响应式断点）和 JS（粒子背景 → IntersectionObserver 计数器 → 时间线滚动显现 → 轮播定时器）。它们仅在 body 内的具体文本数据（姓名、成就标签、统计数字、时间线条目、大满贯/全满贯卡片、页脚文案）和激活的导航标签不同。

页面按以下顺序组织 sections：
1. **player-tabs** — 固定定位左上角，`backdrop-filter: blur` 毛玻璃效果
2. **hero** — 全屏区域，三个 z-index 层：轮播背景层（z-index: 0）、半透明渐变遮罩层（z-index: 1，`::before` 伪元素）、文字内容层（z-index: 2），文字使用 `@keyframes fadeUp` 逐项延迟出现
3. **stats** — 数据统计卡片网格，数字通过 IntersectionObserver 触发 `setInterval` 计数器动画（从 0 递增到 `data-target` 值），非重复触发
4. **timeline** — 桌面端为左右交替的垂直时间线（`::before` 中线 + `.tl-item:nth-child(odd/even)` 定位），移动端统一左对齐，卡片进入视口时添加 `.visible` 类触发 CSS 过渡
5. **grand-slam** — 暗色背景区，网格展示各项荣誉，每个 `.gs-item` 悬停时上浮并高亮边框
6. **legend**（仅王曼昱页面）— 与 grand-slam 结构相同的额外成就展示区
7. **footer** — 暗色底栏

### 图片轮播机制
轮播系统由两部分协作：
- **HTML 标记区**：`<!-- HERO_SLIDES_START -->` 和 `<!-- HERO_SLIDES_END -->` 之间的 `<div class="hero-slides">` 包含所有 `.hero-slide`，第一张带 `class="active"`
- **CSS**：所有 `.hero-slide` 默认 `opacity: 0; transition: opacity 1.5s ease-in-out`，带 `.active` 的幻灯 `opacity: 1`
- **JS**：`setInterval` 每 5000ms 移除当前 active 再给下一个添加 active，循环索引
- **build.py**：扫描对应图片文件夹，按文件名排序生成轮播 HTML，使用正则 `(<!-- HERO_SLIDES_START -->)\r?\n.*?\r?\n(\s*<!-- HERO_SLIDES_END -->)` 替换标记间内容

**修改轮播行为时，必须同步修改两个 HTML 文件**，因为 CSS 和 JS 在两个文件中完全重复。build.py 中的 `IMAGE_FOLDERS` 字典维护了 HTML 文件名到图片文件夹的映射。

### CSS 架构
- `:root` 自定义属性定义调色板（红/金/深蓝/米色）和阴影，两页面变量值完全相同
- 所有样式在 `<style>` 标签内按 section 分块：PLAYER TABS → HERO → STATS → SECTION TITLE → TIMELINE → GRAND SLAM → FOOTER → RESPONSIVE
- 响应式通过 `@media (max-width: 768px)` 处理：时间线从双列变单列、统计网格从 4 列变 2 列、标签缩小
- 动画模式有三种：CSS `@keyframes`（fadeUp/bounce/particles）、CSS transition（轮播 opacity、卡片 hover scale、时间线显隐）、JS 定时器（计数器数字递增）

### JS 架构
每个页面的 `<script>` 块包含四个独立模块，均使用原生 DOM API：
1. **粒子生成**：循环 30 次创建绝对定位 div，随机 left/animationDuration/animationDelay/size
2. **计数器动画**：IntersectionObserver（threshold: 0.5）监听 `.stat-num`，触发仅一次（触发后 unobserved），30 步 `setInterval` 递增
3. **时间线显现**：IntersectionObserver（threshold: 0.15）监听 `.tl-item`，进入视口添加 `visible` 类
4. **轮播定时器**：5 秒 `setInterval` 循环切换 `.hero-slide` 的 `active` 类

### 数据准确性注意事项
时间线、统计数据、成就标签等均为手动整理的真实数据。修改任何球员的赛事数据前，应通过搜索确认信息准确（如确认冠军年份、对手、搭档姓名等）。之前发现并修正过的典型错误包括：青奥会项目名称（混合团体而非混双）、世界杯单打冠军归属确认、亚洲三大赛夺金时间线。两个页面的数据完全独立，修改一个不会影响另一个。

### 部署
项目直接部署到 EdgeOne Pages，通过 GitHub 仓库导入。`index.html` 为必要入口文件，缺失会导致 404。build.py 生成的内容直接写入 HTML 文件，提交到 git 后部署自动更新。
