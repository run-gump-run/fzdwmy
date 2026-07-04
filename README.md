# 🏓 樊振东 & 王曼昱 球迷致敬网站

两位国乒世界冠军的个人致敬页面，展示他们的职业生涯时间线、荣誉数据和精彩瞬间。

## 📁 项目结构

```
fzdwmy/
├── fanzhendong.html       # 樊振东主页
├── wangmanyu.html          # 王曼昱主页
├── build.py               # 轮播自动生成脚本
├── images/
│   ├── fanzhendong/       # 樊振东照片（7 张）
│   └── wangmanyu/         # 王曼昱照片（3 张）
└── LICENSE
```

## ✨ 功能特性

- **球员切换** — 页面左上角固定切换标签，一键在樊振东和王曼昱之间跳转
- **图片轮播** — Hero 区域背景图片自动轮播，5 秒渐变切换
- **职业生涯时间线** — 从入选国家队到登顶世界之巅的完整历程
- **荣誉数据** — 奥运金牌、世乒赛、世界杯等关键赛事成绩
- **大满贯/全满贯展示** — 樊振东超级全满贯 & 王曼昱亚洲全满贯成就
- **响应式设计** — 适配桌面端和移动端
- **滚动动画** — IntersectionObserver 驱动的计数器动画和渐入效果

## 🚀 快速开始

直接用浏览器打开 `fanzhendong.html` 或 `wangmanyu.html` 即可查看。

## 🖼️ 添加/更新图片

1. 将要展示的图片放入对应的文件夹：
   - 樊振东 → `images/fanzhendong/`
   - 王曼昱 → `images/wangmanyu/`

2. 运行构建脚本自动更新轮播：

```bash
python build.py
```

图片按文件名字母排序，第一张默认为初始显示图片。

## 🛠️ 技术栈

- 纯 HTML / CSS / JavaScript，零依赖
- CSS 自定义属性（`:root` 变量）统一主题配色
- IntersectionObserver API 实现滚动动画
- Python 构建脚本自动扫描图片并更新 HTML 轮播
- 支持 `.jpg` `.jpeg` `.png` `.webp` `.gif` 格式

## 📄 许可

[MIT License](LICENSE)
