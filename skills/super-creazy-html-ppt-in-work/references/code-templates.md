# 代码模板库

## 完整 HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: {{PRIMARY}};
            --secondary: {{SECONDARY}};
            --accent: {{ACCENT}};
            --bg: {{BG}};
            --bgSecondary: {{BG_SECONDARY}};
            --text: {{TEXT}};
            --textMuted: {{TEXT_MUTED}};
            --glass: {{GLASS}};
            --glassBorder: {{GLASS_BORDER}};
            --cardBg: {{CARD_BG}};
            --shadow: {{SHADOW}};
            --radius: 16px;
            --radius-sm: 8px;
            --radius-full: 9999px;
            --font: 'Inter', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
            --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        html, body {
            width: 100%; height: 100%;
            font-family: var(--font);
            background: var(--bg);
            color: var(--text);
            overflow: hidden;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* ===== 背景层 ===== */
        .bg-layer {
            position: fixed; inset: 0; z-index: 0; pointer-events: none;
        }
        .bg-layer.gradient {
            background: linear-gradient(135deg, var(--bg) 0%, var(--bgSecondary) 50%, var(--bg) 100%);
        }
        .bg-layer .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.3;
        }
        .bg-layer .orb-1 {
            width: 600px; height: 600px;
            background: var(--primary);
            top: -200px; right: -100px;
        }
        .bg-layer .orb-2 {
            width: 400px; height: 400px;
            background: var(--secondary);
            bottom: -150px; left: -100px;
        }
        .bg-layer .orb-3 {
            width: 300px; height: 300px;
            background: var(--accent);
            top: 40%; left: 50%;
            transform: translate(-50%, -50%);
        }

        /* ===== 几何图案背景 ===== */
        .bg-pattern-dots {
            background-image: radial-gradient(circle, var(--textMuted) 1px, transparent 1px);
            background-size: 30px 30px;
            opacity: 0.06;
        }
        .bg-pattern-grid {
            background-image:
                linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 60px 60px;
        }
        .bg-pattern-waves {
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(255,255,255,0.01) 10px,
                rgba(255,255,255,0.01) 20px
            );
        }

        /* ===== 主容器 ===== */
        .presentation {
            position: relative; z-index: 1;
            width: 100%; height: 100%;
        }

        /* ===== 幻灯片 ===== */
        .slide {
            position: absolute; inset: 0;
            display: none;
            align-items: center; justify-content: center;
            padding: clamp(40px, 6vw, 80px);
            opacity: 0;
        }
        .slide.active {
            display: flex;
        }
        .slide.transitioning {
            display: flex;
        }

        .content-wrapper {
            width: 100%; max-width: 1400px;
        }
        .content-group > * {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        .slide.animate-in .content-group > * {
            opacity: 1;
            transform: translateY(0);
        }
        .slide.animate-in .content-group > *:nth-child(1) { transition-delay: 0.1s; }
        .slide.animate-in .content-group > *:nth-child(2) { transition-delay: 0.2s; }
        .slide.animate-in .content-group > *:nth-child(3) { transition-delay: 0.3s; }
        .slide.animate-in .content-group > *:nth-child(4) { transition-delay: 0.4s; }
        .slide.animate-in .content-group > *:nth-child(5) { transition-delay: 0.5s; }
        .slide.animate-in .content-group > *:nth-child(6) { transition-delay: 0.6s; }

        /* ===== 玻璃态卡片 ===== */
        .glass {
            background: var(--glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glassBorder);
            border-radius: var(--radius);
        }
        .glass-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glassBorder);
            border-radius: var(--radius);
            padding: clamp(1.5rem, 3vw, 2.5rem);
            transition: all var(--transition);
        }
        .glass-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255,255,255,0.25);
            box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        }

        /* ===== 排版 ===== */
        .text-xs { font-size: clamp(0.625rem, 0.8vw, 0.75rem); }
        .text-sm { font-size: clamp(0.75rem, 1vw, 0.875rem); }
        .text-base { font-size: clamp(0.875rem, 1.2vw, 1rem); }
        .text-lg { font-size: clamp(1rem, 1.5vw, 1.25rem); }
        .text-xl { font-size: clamp(1.25rem, 2vw, 1.5rem); }
        .text-2xl { font-size: clamp(1.5rem, 2.5vw, 2rem); }
        .text-3xl { font-size: clamp(2rem, 4vw, 3rem); }
        .text-4xl { font-size: clamp(3rem, 6vw, 5rem); }
        .text-muted { color: var(--textMuted); }
        .font-light { font-weight: 300; }
        .font-normal { font-weight: 400; }
        .font-medium { font-weight: 500; }
        .font-semibold { font-weight: 600; }
        .font-bold { font-weight: 700; }
        .font-extrabold { font-weight: 800; }

        /* ===== 标签/徽章 ===== */
        .badge {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 6px 16px;
            background: var(--glass);
            border: 1px solid var(--glassBorder);
            border-radius: var(--radius-full);
            font-size: clamp(0.7rem, 0.9vw, 0.8rem);
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--accent);
        }

        /* ===== 按钮 ===== */
        .btn {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 12px 28px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none; border-radius: var(--radius-full);
            color: white; font-weight: 600;
            font-size: clamp(0.875rem, 1.1vw, 1rem);
            cursor: pointer;
            transition: all var(--transition);
            text-decoration: none;
        }
        .btn:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        }

        /* ===== 渐变文字 ===== */
        .gradient-text {
            background: linear-gradient(135deg, var(--accent), var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* ===== SVG 图标 ===== */
        .icon { width: 24px; height: 24px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
        .icon-sm { width: 18px; height: 18px; }
        .icon-lg { width: 36px; height: 36px; }
        .icon-xl { width: 48px; height: 48px; }
        .icon-2xl { width: 64px; height: 64px; }
        .icon-circle {
            display: flex; align-items: center; justify-content: center;
            width: 56px; height: 56px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 50%;
            color: white;
        }

        /* ===== 导航 ===== */
        .nav-controls {
            position: fixed; bottom: 0; left: 0; right: 0; z-index: 100;
            padding: 24px 40px;
            display: flex; align-items: center; justify-content: space-between;
            pointer-events: none;
        }
        .nav-controls > * { pointer-events: auto; }
        .nav-arrows {
            display: flex; gap: 12px;
        }
        .nav-btn {
            width: 44px; height: 44px;
            display: flex; align-items: center; justify-content: center;
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glassBorder);
            border-radius: 50%;
            color: var(--text);
            cursor: pointer;
            transition: all var(--transition);
        }
        .nav-btn:hover:not(:disabled) {
            background: rgba(255,255,255,0.15);
            border-color: rgba(255,255,255,0.3);
        }
        .nav-btn:disabled {
            opacity: 0.3; cursor: not-allowed;
        }

        .nav-center {
            display: flex; align-items: center; gap: 16px;
        }
        .progress-bar {
            width: 120px; height: 3px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        .page-indicator {
            font-size: 0.8rem;
            font-weight: 500;
            color: var(--textMuted);
            min-width: 60px;
            text-align: center;
        }

        .dot-nav {
            display: flex; gap: 8px;
        }
        .dot {
            width: 8px; height: 8px;
            border-radius: 50%;
            background: rgba(255,255,255,0.25);
            cursor: pointer;
            transition: all var(--transition);
        }
        .dot.active {
            background: var(--accent);
            box-shadow: 0 0 10px var(--accent);
        }

        /* ===== CSS 动画关键帧 ===== */
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideDown { from { opacity: 0; transform: translateY(-40px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideLeft { from { opacity: 0; transform: translateX(40px); } to { opacity: 1; transform: translateX(0); } }
        @keyframes slideRight { from { opacity: 0; transform: translateX(-40px); } to { opacity: 1; transform: translateX(0); } }
        @keyframes scaleUp { from { opacity: 0; transform: scale(0.85); } to { opacity: 1; transform: scale(1); } }
        @keyframes zoomIn { from { opacity: 0; transform: scale(0.3); } to { opacity: 1; transform: scale(1); } }
        @keyframes bounce {
            0% { opacity: 0; transform: translateY(-80px); }
            60% { opacity: 1; transform: translateY(10px); }
            80% { transform: translateY(-5px); }
            100% { transform: translateY(0); }
        }
        @keyframes blurIn { from { opacity: 0; filter: blur(20px); } to { opacity: 1; filter: blur(0); } }
        @keyframes elastic {
            0% { transform: scaleX(0); opacity: 0; }
            60% { transform: scaleX(1.05); opacity: 1; }
            80% { transform: scaleX(0.95); }
            100% { transform: scaleX(1); }
        }

        /* ===== 粒子背景（Canvas） ===== */
        .particles-canvas {
            position: fixed; inset: 0; z-index: 0; pointer-events: none;
        }
    </style>
</head>
<body>
    <!-- ===== 背景层（每页必须不同！）=====
         不要所有页面共用同一个 bg-layer。
         方案1：每张 .slide 内嵌自己的背景层（position:absolute;inset:0;z-index:-1）
         方案2：为不同的 .slide 写不同的背景 class，通过 JS 切换全局背景
         方案3：直接使用 .slide 的 background 属性为每页设置不同背景 -->
    <!-- 以下为默认全局背景，通常仅用于 fallback -->
    <div class="bg-layer gradient">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
    </div>

    <!-- 主演示 -->
    <main class="presentation" id="presentation">
        <!-- 幻灯片 -->
    </main>

    <!-- 导航 -->
    <nav class="nav-controls">
        <div class="nav-arrows">
            <button class="nav-btn" id="prevBtn" aria-label="上一页">
                <svg class="icon" viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <button class="nav-btn" id="nextBtn" aria-label="下一页">
                <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
        </div>
        <div class="nav-center">
            <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
            <span class="page-indicator" id="pageIndicator">1 / 10</span>
        </div>
        <div class="dot-nav" id="dotNav"></div>
    </nav>

    <script>
    (function() {
        const slides = document.querySelectorAll('.slide');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const progressFill = document.getElementById('progressFill');
        const pageIndicator = document.getElementById('pageIndicator');
        const dotNav = document.getElementById('dotNav');

        let currentIndex = 0;
        let isTransitioning = false;

        // 创建圆点导航
        slides.forEach((_, i) => {
            const dot = document.createElement('div');
            dot.className = 'dot' + (i === 0 ? ' active' : '');
            dot.addEventListener('click', () => goTo(i));
            dotNav.appendChild(dot);
        });

        const dots = document.querySelectorAll('.dot');

        function goTo(index) {
            if (isTransitioning || index === currentIndex || index < 0 || index >= slides.length) return;
            isTransitioning = true;

            const currentSlide = slides[currentIndex];
            const nextSlide = slides[index];
            const direction = index > currentIndex ? 'next' : 'prev';

            // 移除旧状态
            currentSlide.classList.remove('animate-in');

            // 设置新幻灯片
            nextSlide.classList.add('active', 'transitioning');

            // 触发入场动画
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    nextSlide.classList.add('animate-in');
                    nextSlide.classList.remove('transitioning');
                });
            });

            // 隐藏旧幻灯片
            setTimeout(() => {
                currentSlide.classList.remove('active');
            }, 600);

            // 更新导航
            currentIndex = index;
            updateNav();
            setTimeout(() => { isTransitioning = false; }, 600);
        }

        function updateNav() {
            prevBtn.disabled = currentIndex === 0;
            nextBtn.disabled = currentIndex === slides.length - 1;
            progressFill.style.width = ((currentIndex + 1) / slides.length * 100) + '%';
            pageIndicator.textContent = (currentIndex + 1) + ' / ' + slides.length;
            dots.forEach((d, i) => d.classList.toggle('active', i === currentIndex));
        }

        // 键盘导航
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowRight': case 'ArrowDown': case ' ':
                    e.preventDefault();
                    if (currentIndex < slides.length - 1) goTo(currentIndex + 1);
                    break;
                case 'ArrowLeft': case 'ArrowUp':
                    e.preventDefault();
                    if (currentIndex > 0) goTo(currentIndex - 1);
                    break;
                case 'Home':
                    e.preventDefault(); goTo(0);
                    break;
                case 'End':
                    e.preventDefault(); goTo(slides.length - 1);
                    break;
                case 'f': case 'F':
                    if (document.fullscreenElement) {
                        document.exitFullscreen();
                    } else {
                        document.documentElement.requestFullscreen();
                    }
                    break;
            }
        });

        // 按钮导航
        prevBtn.addEventListener('click', () => { if (currentIndex > 0) goTo(currentIndex - 1); });
        nextBtn.addEventListener('click', () => { if (currentIndex < slides.length - 1) goTo(currentIndex + 1); });

        // 触摸导航
        let touchStartX = 0;
        document.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
        document.addEventListener('touchend', (e) => {
            const diff = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(diff) > 50) {
                if (diff > 0 && currentIndex < slides.length - 1) goTo(currentIndex + 1);
                else if (diff < 0 && currentIndex > 0) goTo(currentIndex - 1);
            }
        });

        // 初始化
        slides[0].classList.add('active');
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                slides[0].classList.add('animate-in');
            });
        });
        updateNav();
    })();
    </script>
</body>
</html>
```

---

## SVG 图标模板

### 常用图标 SVG

```html
<!-- arrow-right -->
<svg class="icon" viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>

<!-- arrow-left -->
<svg class="icon" viewBox="0 0 24 24"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>

<!-- check -->
<svg class="icon" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>

<!-- star -->
<svg class="icon" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>

<!-- zap -->
<svg class="icon" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>

<!-- shield -->
<svg class="icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>

<!-- trending-up -->
<svg class="icon" viewBox="0 0 24 24"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>

<!-- users -->
<svg class="icon" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>

<!-- heart -->
<svg class="icon" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>

<!-- globe -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>

<!-- settings -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>

<!-- mail -->
<svg class="icon" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>

<!-- clock -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>

<!-- map-pin -->
<svg class="icon" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>

<!-- lightbulb -->
<svg class="icon" viewBox="0 0 24 24"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>

<!-- target -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>

<!-- rocket -->
<svg class="icon" viewBox="0 0 24 24"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>

<!-- laptop -->
<svg class="icon" viewBox="0 0 24 24"><path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0l1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/></svg>

<!-- lock -->
<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>

<!-- search -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>

<!-- bar-chart -->
<svg class="icon" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>

<!-- pie-chart -->
<svg class="icon" viewBox="0 0 24 24"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>

<!-- activity -->
<svg class="icon" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>

<!-- award -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>

<!-- bookmark -->
<svg class="icon" viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>

<!-- calendar -->
<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>

<!-- camera -->
<svg class="icon" viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>

<!-- cloud -->
<svg class="icon" viewBox="0 0 24 24"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>

<!-- database -->
<svg class="icon" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>

<!-- code -->
<svg class="icon" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>

<!-- folder -->
<svg class="icon" viewBox="0 0 24 24"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>

<!-- image -->
<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>

<!-- music -->
<svg class="icon" viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>

<!-- play -->
<svg class="icon" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>

<!-- video -->
<svg class="icon" viewBox="0 0 24 24"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>

<!-- wifi -->
<svg class="icon" viewBox="0 0 24 24"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><circle cx="12" cy="20" r="1"/></svg>

<!-- bell -->
<svg class="icon" viewBox="0 0 24 24"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>

<!-- share -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>

<!-- file-text -->
<svg class="icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>

<!-- edit -->
<svg class="icon" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>

<!-- smile -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>

<!-- compass -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>

<!-- sun -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>

<!-- moon -->
<svg class="icon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>

<!-- leaf -->
<svg class="icon" viewBox="0 0 24 24"><path d="M17 8C8 10 5.9 16.17 3.82 21.34l1.89.66.95-2.3c.48.17.98.3 1.34.3C19 20 22 3 22 3c-1 2-8 2.25-13 3.25S2 11.5 2 13.5s1.75 3.75 1.75 3.75"/></svg>

<!-- mountain -->
<svg class="icon" viewBox="0 0 24 24"><path d="M17 10l-5 5-5-5"/><path d="M22 16.92L14.65 4.26a1.5 1.5 0 0 0-2.58 0L2 16.92A1.5 1.5 0 0 0 3.31 19h17.38a1.5 1.5 0 0 0 1.31-2.08z"/></svg>

<!-- flower -->
<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 12c0-3 1.5-5.5 3-7"/><path d="M12 12c0 3 1.5 5.5 3 7"/><path d="M12 12c-3 0-5.5-1.5-7-3"/><path d="M12 12c3 0 5.5 1.5 7 3"/></svg>

<!-- crown -->
<svg class="icon" viewBox="0 0 24 24"><path d="M2 4l3 12h14l3-12-6 5-4-7-4 7-6-5z"/><path d="M4 20h16"/></svg>

<!-- layers -->
<svg class="icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
```

---

## 粒子背景 JS

```javascript
// Canvas 粒子系统
(function() {
    const canvas = document.getElementById('particles');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w, h, particles = [];

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    const particleCount = 60;
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * w,
            y: Math.random() * h,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 2 + 0.5,
            opacity: Math.random() * 0.5 + 0.1
        });
    }

    function draw() {
        ctx.clearRect(0, 0, w, h);
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0) p.x = w;
            if (p.x > w) p.x = 0;
            if (p.y < 0) p.y = h;
            if (p.y > h) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255,255,255,${p.opacity})`;
            ctx.fill();
        });

        // 连线
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(255,255,255,${0.05 * (1 - dist / 120)})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(draw);
    }
    draw();
})();
```

---

## 布局模板

### Poster（海报封面）

```html
<section class="slide active" data-index="0">
    <div class="content-wrapper layout-poster">
        <div class="content-group" style="text-align:center; display:flex; flex-direction:column; align-items:center; gap:24px;">
            <div class="badge">
                <svg class="icon icon-sm" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                2025年度报告
            </div>
            <h1 class="text-4xl font-extrabold gradient-text" style="line-height:1.1;">
                创新引领未来
            </h1>
            <p class="text-xl text-muted font-light" style="max-width:700px;">
                重新定义智能科技体验，开启数字化新时代
            </p>
            <button class="btn" style="margin-top:16px;">
                立即探索
                <svg class="icon icon-sm" viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </button>
        </div>
    </div>
</section>
```

### Stats Dashboard（数据仪表盘）

```html
<section class="slide" data-index="1">
    <div class="content-wrapper layout-stats">
        <div class="content-group" style="display:flex; flex-direction:column; align-items:center; gap:48px;">
            <div class="badge">
                <svg class="icon icon-sm" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                核心数据
            </div>
            <div style="display:flex; gap:40px; flex-wrap:wrap; justify-content:center;">
                <div class="glass-card" style="text-align:center; min-width:200px;">
                    <div class="text-4xl font-extrabold gradient-text">99.9%</div>
                    <div class="text-sm text-muted" style="margin-top:8px;">服务稳定性</div>
                </div>
                <div class="glass-card" style="text-align:center; min-width:200px;">
                    <div class="text-4xl font-extrabold gradient-text">50ms</div>
                    <div class="text-sm text-muted" style="margin-top:8px;">平均响应时间</div>
                </div>
                <div class="glass-card" style="text-align:center; min-width:200px;">
                    <div class="text-4xl font-extrabold gradient-text">10M+</div>
                    <div class="text-sm text-muted" style="margin-top:8px;">全球活跃用户</div>
                </div>
            </div>
        </div>
    </div>
</section>
```

### Grid Cards（卡片网格）— 正确示范：图片为主 + SVG 图标为标识

```html
<!-- 卡片正确做法：每卡顶部有生成配图，SVG 图标仅作小标识 -->
<section class="slide" data-index="2">
    <div class="content-wrapper layout-cards">
        <div class="content-group" style="display:flex; flex-direction:column; align-items:center; gap:36px;">
            <div class="badge">
                <svg class="icon icon-sm" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/></svg>
                核心能力
            </div>
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:24px; width:100%;">
                <div class="glass-card" style="padding:0; overflow:hidden; text-align:left;">
                    <!-- 卡片顶部配图（必须用 generate_image 生成） -->
                    <img src="path/to/card-image-1.png" alt="极速引擎" style="width:100%; height:180px; object-fit:cover;">
                    <div style="padding:20px 24px 24px;">
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                            <svg class="icon" style="width:20px; height:20px; color:var(--accent);" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                            <h3 class="text-base font-semibold">极速引擎</h3>
                        </div>
                        <p class="text-sm text-muted" style="line-height:1.7;">搭载自研分布式计算架构，将复杂数据处理时间从分钟级缩短至毫秒级，提供业界领先的实时响应体验。</p>
                    </div>
                </div>
                <div class="glass-card" style="padding:0; overflow:hidden; text-align:left;">
                    <img src="path/to/card-image-2.png" alt="安全守护" style="width:100%; height:180px; object-fit:cover;">
                    <div style="padding:20px 24px 24px;">
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                            <svg class="icon" style="width:20px; height:20px; color:var(--accent);" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                            <h3 class="text-base font-semibold">安全守护</h3>
                        </div>
                        <p class="text-sm text-muted" style="line-height:1.7;">采用银行级数据加密与多层防火墙体系，通过 SOC2 合规认证，全方位保障用户数据与业务信息安全。</p>
                    </div>
                </div>
                <div class="glass-card" style="padding:0; overflow:hidden; text-align:left;">
                    <img src="path/to/card-image-3.png" alt="云端智能" style="width:100%; height:180px; object-fit:cover;">
                    <div style="padding:20px 24px 24px;">
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                            <svg class="icon" style="width:20px; height:20px; color:var(--accent);" viewBox="0 0 24 24"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>
                            <h3 class="text-base font-semibold">云端智能</h3>
                        </div>
                        <p class="text-sm text-muted" style="line-height:1.7;">基于大规模机器学习模型，自动分析业务数据并生成可执行的优化建议，帮助企业做出更精准的决策。</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
```

> **卡片配图铁律**：card-image 图片使用 `width:100%; height:180px; object-fit:cover;` 无边框、无圆角包裹。下方内容区使用 `padding:20px 24px 24px;`。SVG图标仅作标题旁 20px 小标识。

### Quote Spotlight（语录聚焦）

```html
<section class="slide" data-index="3">
    <div class="content-wrapper layout-quote">
        <div class="content-group" style="display:flex; flex-direction:column; align-items:center; gap:32px; text-align:center;">
            <svg class="icon icon-2xl" style="color:var(--accent); opacity:0.4;" viewBox="0 0 24 24">
                <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/>
                <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>
            </svg>
            <blockquote class="text-3xl font-light" style="max-width:800px; line-height:1.5; font-style:italic;">
                "创新不是改变一切，而是重塑可能。"
            </blockquote>
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="width:48px; height:48px; border-radius:50%; background:linear-gradient(135deg,var(--primary),var(--secondary)); display:flex; align-items:center; justify-content:center;">
                    <svg class="icon" viewBox="0 0 24 24" style="color:white;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                </div>
                <div style="text-align:left;">
                    <div class="text-base font-semibold">张伟</div>
                    <div class="text-xs text-muted">首席技术官</div>
                </div>
            </div>
        </div>
    </div>
</section>
```

### Timeline（时间线）

```html
<section class="slide" data-index="4">
    <div class="content-wrapper layout-timeline">
        <div class="content-group" style="display:flex; flex-direction:column; align-items:center; gap:48px;">
            <div class="badge">
                <svg class="icon icon-sm" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                发展历程
            </div>
            <div style="display:flex; gap:0; align-items:flex-start; position:relative; width:100%; max-width:1000px; justify-content:space-between;">
                <!-- 连接线 -->
                <div style="position:absolute; top:24px; left:40px; right:40px; height:2px; background:linear-gradient(90deg,var(--primary),var(--accent)); opacity:0.3;"></div>
                <!-- 节点 -->
                <div class="glass-card" style="text-align:center; min-width:150px; position:relative; z-index:1;">
                    <div class="text-2xl font-extrabold gradient-text">2019</div>
                    <div class="text-sm font-semibold" style="margin-top:8px;">创立启航</div>
                    <div class="text-xs text-muted" style="margin-top:4px;">梦想从这里开始</div>
                </div>
                <div class="glass-card" style="text-align:center; min-width:150px; position:relative; z-index:1;">
                    <div class="text-2xl font-extrabold gradient-text">2021</div>
                    <div class="text-sm font-semibold" style="margin-top:8px;">技术突破</div>
                    <div class="text-xs text-muted" style="margin-top:4px;">核心专利获批</div>
                </div>
                <div class="glass-card" style="text-align:center; min-width:150px; position:relative; z-index:1;">
                    <div class="text-2xl font-extrabold gradient-text">2023</div>
                    <div class="text-sm font-semibold" style="margin-top:8px;">全球化</div>
                    <div class="text-xs text-muted" style="margin-top:4px;">覆盖30+国家</div>
                </div>
                <div class="glass-card" style="text-align:center; min-width:150px; position:relative; z-index:1;">
                    <div class="text-2xl font-extrabold gradient-text">2025</div>
                    <div class="text-sm font-semibold" style="margin-top:8px;">行业领先</div>
                    <div class="text-xs text-muted" style="margin-top:4px;">市场份额第一</div>
                </div>
            </div>
        </div>
    </div>
</section>
```

### Comparison（对比展示）

```html
<section class="slide" data-index="5">
    <div class="content-wrapper layout-comparison">
        <div class="content-group" style="display:flex; flex-direction:column; align-items:center; gap:40px;">
            <div class="badge">
                <svg class="icon icon-sm" viewBox="0 0 24 24"><rect x="2" y="3" width="8" height="18" rx="1"/><rect x="14" y="8" width="8" height="13" rx="1"/></svg>
                方案对比
            </div>
            <div style="display:flex; gap:32px; width:100%; max-width:900px;">
                <div style="flex:1; padding:32px; border-radius:16px; background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.2);">
                    <div class="text-xl font-bold" style="margin-bottom:16px; color:#ef4444;">传统方案</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:12px;">
                        <li style="display:flex; align-items:center; gap:8px;">
                            <svg class="icon icon-sm" style="color:#ef4444;"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                            <span class="text-sm">人工处理，效率低</span>
                        </li>
                        <li style="display:flex; align-items:center; gap:8px;">
                            <svg class="icon icon-sm" style="color:#ef4444;"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                            <span class="text-sm">错误率高达 5%</span>
                        </li>
                        <li style="display:flex; align-items:center; gap:8px;">
                            <svg class="icon icon-sm" style="color:#ef4444;"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                            <span class="text-sm">成本高，不可扩展</span>
                        </li>
                    </ul>
                </div>
                <div style="flex:1; padding:32px; border-radius:16px; background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.2);">
                    <div class="text-xl font-bold" style="margin-bottom:16px; color:#22c55e;">我们的方案</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:12px;">
                        <li style="display:flex; align-items:center; gap:8px;">
                            <svg class="icon icon-sm" style="color:#22c55e;"><polyline points="20 6 9 17 4 12"/></svg>
                            <span class="text-sm">AI自动化，效率提升10x</span>
                        </li>
                        <li style="display:flex; align-items:center; gap:8px;">
                            <svg class="icon icon-sm" style="color:#22c55e;"><polyline points="20 6 9 17 4 12"/></svg>
                            <span class="text-sm">准确率 99.9%</span>
                        </li>
                        <li style="display:flex; align-items:center; gap:8px;">
                            <svg class="icon icon-sm" style="color:#22c55e;"><polyline points="20 6 9 17 4 12"/></svg>
                            <span class="text-sm">弹性扩展，按需付费</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
```

### Hero Split（左右分栏）

```html
<section class="slide" data-index="6">
    <div class="content-wrapper layout-hero-split">
        <div class="content-group" style="display:flex; align-items:center; gap:60px;">
            <div style="flex:1; display:flex; flex-direction:column; gap:20px;">
                <div class="badge" style="align-self:flex-start;">
                    <svg class="icon icon-sm" viewBox="0 0 24 24"><path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0l1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/></svg>
                    智能平台
                </div>
                <h2 class="text-3xl font-extrabold" style="line-height:1.2;">一站式<br><span class="gradient-text">数据分析平台</span></h2>
                <p class="text-base text-muted" style="max-width:450px; line-height:1.6;">整合多源数据，提供实时洞察与智能决策支持，助力企业数字化转型。</p>
                <div style="display:flex; gap:12px; margin-top:8px;">
                    <button class="btn">开始使用</button>
                    <button class="btn" style="background:transparent; border:1px solid var(--glassBorder);">了解更多</button>
                </div>
            </div>
            <!-- 右侧：生成配图（必须用 generate_image 工具生成真实图片） -->
            <div style="flex:1; display:flex; justify-content:center; align-items:center;">
                <img src="path/to/generated-image.png" alt="配图说明" style="width:100%; height:auto; max-height:70vh; object-fit:contain; border-radius:4px;">
            </div>
        </div>
    </div>
</section>
```
```

### Gallery（图文画廊）

```html
<section class="slide" data-index="7">
    <div class="content-wrapper layout-gallery">
        <div class="content-group" style="display:flex; flex-direction:column; align-items:center; gap:32px;">
            <div class="badge">
                <svg class="icon icon-sm" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                项目展示
            </div>
            <!-- 必须用 generate_image 工具为每张卡片生成对应配图 -->
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20px; width:100%; max-width:1100px;">
                <div style="position:relative; border-radius:4px; overflow:hidden; aspect-ratio:4/3; cursor:pointer; transition:all 0.3s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <img src="path/to/image-1.png" alt="项目 Alpha" style="width:100%; height:100%; object-fit:cover;">
                    <div style="position:absolute; bottom:0; left:0; right:0; padding:20px; background:linear-gradient(transparent,rgba(0,0,0,0.75));">
                        <div class="text-base font-semibold">项目 Alpha</div>
                        <div class="text-sm text-muted">品牌设计</div>
                    </div>
                </div>
                <div style="position:relative; border-radius:4px; overflow:hidden; aspect-ratio:4/3; cursor:pointer; transition:all 0.3s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <img src="path/to/image-2.png" alt="项目 Beta" style="width:100%; height:100%; object-fit:cover;">
                    <div style="position:absolute; bottom:0; left:0; right:0; padding:20px; background:linear-gradient(transparent,rgba(0,0,0,0.75));">
                        <div class="text-base font-semibold">项目 Beta</div>
                        <div class="text-sm text-muted">产品设计</div>
                    </div>
                </div>
                <div style="position:relative; border-radius:4px; overflow:hidden; aspect-ratio:4/3; cursor:pointer; transition:all 0.3s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <img src="path/to/image-3.png" alt="项目 Gamma" style="width:100%; height:100%; object-fit:cover;">
                    <div style="position:absolute; bottom:0; left:0; right:0; padding:20px; background:linear-gradient(transparent,rgba(0,0,0,0.75));">
                        <div class="text-base font-semibold">项目 Gamma</div>
                        <div class="text-sm text-muted">交互设计</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
```
```

---

## 主题完整 CSS 变量

### midnight（深色科技）
```css
:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --accent: #a78bfa;
    --bg: #0a0a0f;
    --bgSecondary: #13132b;
    --text: #f0f0ff;
    --textMuted: #8888cc;
    --glass: rgba(99,102,241,0.08);
    --glassBorder: rgba(99,102,241,0.15);
    --cardBg: rgba(99,102,241,0.06);
    --shadow: rgba(99,102,241,0.15);
}
```

### aurora（极光蓝）
```css
:root {
    --primary: #0ea5e9;
    --secondary: #06b6d4;
    --accent: #22d3ee;
    --bg: #0c1929;
    --bgSecondary: #0f2847;
    --text: #f0f9ff;
    --textMuted: #7dd3fc;
    --glass: rgba(14,165,233,0.08);
    --glassBorder: rgba(14,165,233,0.15);
    --cardBg: rgba(14,165,233,0.06);
    --shadow: rgba(14,165,233,0.15);
}
```

### forest（自然绿）
```css
:root {
    --primary: #22c55e;
    --secondary: #10b981;
    --accent: #34d399;
    --bg: #0a1a0f;
    --bgSecondary: #0f2d18;
    --text: #f0fff4;
    --textMuted: #86efac;
    --glass: rgba(34,197,94,0.08);
    --glassBorder: rgba(34,197,94,0.15);
    --cardBg: rgba(34,197,94,0.06);
    --shadow: rgba(34,197,94,0.15);
}
```

### sunset（暖色活力）
```css
:root {
    --primary: #f97316;
    --secondary: #ef4444;
    --accent: #fbbf24;
    --bg: #1a0a0a;
    --bgSecondary: #2d1410;
    --text: #fff7ed;
    --textMuted: #fdba74;
    --glass: rgba(249,115,22,0.08);
    --glassBorder: rgba(249,115,22,0.15);
    --cardBg: rgba(249,115,22,0.06);
    --shadow: rgba(249,115,22,0.15);
}
```

### ocean（海洋蓝）
```css
:root {
    --primary: #3b82f6;
    --secondary: #0ea5e9;
    --accent: #38bdf8;
    --bg: #0c1222;
    --bgSecondary: #0f1f3d;
    --text: #f0f9ff;
    --textMuted: #7dd3fc;
    --glass: rgba(59,130,246,0.08);
    --glassBorder: rgba(59,130,246,0.15);
    --cardBg: rgba(59,130,246,0.06);
    --shadow: rgba(59,130,246,0.15);
}
```

### cyber（赛博朋克）
```css
:root {
    --primary: #00ff88;
    --secondary: #00e5ff;
    --accent: #76ff03;
    --bg: #050508;
    --bgSecondary: #0a0f0e;
    --text: #e0ffe0;
    --textMuted: #00cc66;
    --glass: rgba(0,255,136,0.06);
    --glassBorder: rgba(0,255,136,0.12);
    --cardBg: rgba(0,255,136,0.04);
    --shadow: rgba(0,255,136,0.1);
}
```

### elegant（浅色商务）
```css
:root {
    --primary: #18181b;
    --secondary: #3f3f46;
    --accent: #52525b;
    --bg: #fafafa;
    --bgSecondary: #f4f4f5;
    --text: #18181b;
    --textMuted: #71717a;
    --glass: rgba(255,255,255,0.7);
    --glassBorder: rgba(0,0,0,0.08);
    --cardBg: rgba(255,255,255,0.8);
    --shadow: rgba(0,0,0,0.05);
    --radius: 8px;
}
```

### rose（玫瑰粉）
```css
:root {
    --primary: #e11d48;
    --secondary: #f43f5e;
    --accent: #fda4af;
    --bg: #1a0a10;
    --bgSecondary: #2d0f1c;
    --text: #fff1f2;
    --textMuted: #fda4af;
    --glass: rgba(225,29,72,0.08);
    --glassBorder: rgba(225,29,72,0.15);
    --cardBg: rgba(225,29,72,0.06);
    --shadow: rgba(225,29,72,0.15);
}
```

### earth（大地棕）
```css
:root {
    --primary: #92400e;
    --secondary: #b45309;
    --accent: #d97706;
    --bg: #1a1008;
    --bgSecondary: #2d1f10;
    --text: #fffbeb;
    --textMuted: #d4a574;
    --glass: rgba(146,64,14,0.08);
    --glassBorder: rgba(146,64,14,0.15);
    --cardBg: rgba(146,64,14,0.06);
    --shadow: rgba(146,64,14,0.15);
}
```

### prism（多彩创意）
```css
:root {
    --primary: #a855f7;
    --secondary: #ec4899;
    --accent: #f97316;
    --bg: #0f0a1a;
    --bgSecondary: #1a1030;
    --text: #faf5ff;
    --textMuted: #c4b5fd;
    --glass: rgba(168,85,247,0.08);
    --glassBorder: rgba(168,85,247,0.15);
    --cardBg: rgba(168,85,247,0.06);
    --shadow: rgba(168,85,247,0.15);
}
```

### calm（宁静青）
```css
:root {
    --primary: #0891b2;
    --secondary: #06b6d4;
    --accent: #67e8f9;
    --bg: #0a1820;
    --bgSecondary: #0f2835;
    --text: #ecfeff;
    --textMuted: #67e8f9;
    --glass: rgba(8,145,178,0.08);
    --glassBorder: rgba(8,145,178,0.15);
    --cardBg: rgba(8,145,178,0.06);
    --shadow: rgba(8,145,178,0.15);
}
```

### slate（石板灰）
```css
:root {
    --primary: #334155;
    --secondary: #475569;
    --accent: #94a3b8;
    --bg: #0f172a;
    --bgSecondary: #1e293b;
    --text: #f1f5f9;
    --textMuted: #94a3b8;
    --glass: rgba(51,65,85,0.08);
    --glassBorder: rgba(51,65,85,0.15);
    --cardBg: rgba(51,65,85,0.06);
    --shadow: rgba(51,65,85,0.15);
}
```
```

---

## 页面切换动画 CSS

```css
/* fade */
.slide.transition-fade { animation: fadeOut 0.5s ease forwards; }
.slide.transition-fade.active { animation: fadeIn 0.5s ease forwards; }

/* slide */
.slide.transition-slide { animation: slideOutLeft 0.5s ease forwards; }
.slide.transition-slide.active { animation: slideInRight 0.5s ease forwards; }

/* zoom */
.slide.transition-zoom { animation: zoomOut 0.6s ease forwards; }
.slide.transition-zoom.active { animation: zoomIn 0.6s cubic-bezier(0.4,0,0.2,1) forwards; }

/* flip */
.slide.transition-flip { animation: flipOut 0.6s ease forwards; transform-origin: center center; }
.slide.transition-flip.active { animation: flipIn 0.6s ease forwards; transform-origin: center center; }

/* blur */
.slide.transition-blur { animation: blurOut 0.6s ease forwards; }
.slide.transition-blur.active { animation: blurIn 0.6s ease forwards; }

/* elastic */
.slide.transition-elastic { animation: elasticOut 0.7s ease forwards; }
.slide.transition-elastic.active { animation: elasticIn 0.7s cubic-bezier(0.68,-0.55,0.265,1.55) forwards; }

@keyframes fadeOut { to { opacity: 0; } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideOutLeft { to { transform: translateX(-100%); opacity: 0; } }
@keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@keyframes zoomOut { to { transform: scale(0.8); opacity: 0; } }
@keyframes zoomIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes flipOut { to { transform: rotateY(-90deg); opacity: 0; } }
@keyframes flipIn { from { transform: rotateY(90deg); opacity: 0; } to { transform: rotateY(0); opacity: 1; } }
@keyframes blurOut { to { filter: blur(20px); opacity: 0; } }
@keyframes blurIn { from { filter: blur(20px); opacity: 0; } to { filter: blur(0); opacity: 1; } }
@keyframes elasticOut { to { transform: scale(1.2); opacity: 0; } }
@keyframes elasticIn {
    from { transform: scale(0.3); opacity: 0; }
    60% { transform: scale(1.05); opacity: 1; }
    80% { transform: scale(0.95); }
    100% { transform: scale(1); }
}
```
```
