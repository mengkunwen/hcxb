// 导航链接平滑滚动效果
document.querySelectorAll('nav ul li a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// 点击了解更多按钮切换显示和隐藏介绍内容
document.getElementById('moreAbout').addEventListener('click', function () {
    const extraInfo = document.getElementById('extraInfo');
    extraInfo.style.display = extraInfo.style.display === 'none' ? 'block' : 'none';
});

// 回到顶部按钮功能
document.getElementById('backToTop').addEventListener('click', function () {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// 监听页面滚动，显示/隐藏回到顶部按钮
window.addEventListener('scroll', function () {
    const backToTop = document.getElementById('backToTop');
    backToTop.style.display = window.scrollY > 100 ? 'block' : 'none';
});

// 表单提交事件
document.getElementById('contactForm').addEventListener('submit', function (e) {
    e.preventDefault();
    alert('感谢您的信息，我们会尽快与您联系！');
    this.reset(); // 重置表单
});

// 切换主题模式
document.getElementById('themeToggle').addEventListener('click', function () {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark-mode' : 'light-mode');
});

// 页面加载时应用保存的主题
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.body.classList.add(savedTheme);
    } else {
        document.body.classList.add('light-mode');
    }
});