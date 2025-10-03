// Highlight active nav link based on current URL
document.addEventListener('DOMContentLoaded', function () {
    var navLinks = document.querySelectorAll('.nav-links a');
    var currentPath = window.location.pathname.replace(/\/index\.html$/, '/');
    // Always ensure trailing slash for folder URLs
    if (!currentPath.endsWith('/')) currentPath += '/';
    navLinks.forEach(function(link) {
        var linkPath = link.getAttribute('href').replace(/\/index\.html$/, '/');
        if (!linkPath.endsWith('/')) linkPath += '/';
        if (linkPath === currentPath || (currentPath === '/' && (linkPath === '/home/' || linkPath === '/home'))) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});
// Main JavaScript for FileConverter Pro

// PDF to Word tool logic
// Show file name on select
const pdfInput = document.getElementById('pdfFile');
const dropZone = document.getElementById('pdfDropZone');
if (pdfInput && dropZone) {
    pdfInput.addEventListener('change', function () {
        if (pdfInput.files && pdfInput.files.length > 0) {
            dropZone.querySelector('span').textContent = pdfInput.files[0].name;
        } else {
            dropZone.querySelector('span').innerHTML = "Drag & drop PDF here or <span style='text-decoration:underline;color:#667eea;'>browse</span>";
        }
    });
}
// Simulate conversion and show loading/download
const form = document.getElementById('pdfToWordForm');
const loading = document.getElementById('pdfLoading');
const download = document.getElementById('pdfDownload');
const downloadBtn = document.getElementById('pdfDownloadBtn');
if(form && loading && download && pdfInput) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!pdfInput.files || pdfInput.files.length === 0) return;
        loading.style.display = 'block';
        download.style.display = 'none';
        setTimeout(function() {
            loading.style.display = 'none';
            download.style.display = 'block';
            // Use uploaded file name for download
            let original = pdfInput.files[0].name;
            let base = original.replace(/\.[^.]+$/, "");
            let outName = base + ".docx";
            downloadBtn.setAttribute('download', outName);
            // Simulate a file for download (with demo content)
            const content = `Converted from PDF: ${original}\nThis is a demo Word file.`;
            const blob = new Blob([content], {type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'});
            downloadBtn.href = URL.createObjectURL(blob);
        }, 1800);
    });
}



// Dropdown open/close for mobile
function toggleToolsDropdown(e) {
    e.preventDefault();
    var dropdown = document.getElementById('toolsDropdown');
    dropdown.classList.toggle('open');
}

// SPA navigation using history API
function navigateTo(event, pageId) {
    event.preventDefault();
    history.pushState({ pageId: pageId }, '', '/' + pageId);
    showPage(pageId);
}

function showPage(pageId) {
    // Hide all .page elements
    var pages = document.querySelectorAll('.page');
    pages.forEach(function (page) {
        page.style.display = 'none';
        page.classList.remove('active');
    });
    // Show the requested page
    var target = document.getElementById(pageId);
    if (target) {
        target.style.display = '';
        target.classList.add('active');
    }
    // Optionally scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// On page load, show correct page based on path
document.addEventListener('DOMContentLoaded', function () {
    var path = window.location.pathname.replace(/^\//, '');
    if (!path || path === '' || path === 'home') path = 'home';
    showPage(path);
});

// Handle browser navigation (back/forward)
window.onpopstate = function (event) {
    var pageId = (event.state && event.state.pageId) || window.location.pathname.replace(/^\//, '') || 'home';
    showPage(pageId);
};

