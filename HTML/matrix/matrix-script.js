function showPage(pageId) {
    const pages = document.getElementsByClassName('page');
    for (let i = 0; i < pages.length; i++) {
        pages[i].style.display = 'none';
    }

    const selectedPage = document.getElementById(pageId + 'Page');

    if (selectedPage) {
        selectedPage.style.display = 'block';
        const prepage= document.getElementById('home');
        prepage.style.opacity = '0';
}
}
showPage('home');