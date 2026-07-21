// language.js
(function() {
    // Define the language based on the current filename
    var currentPath = window.location.pathname;
    var filename = currentPath.substring(currentPath.lastIndexOf('/') + 1) || 'index.html';
    
    var currentLang = 'en';
    if (filename.includes('_TR.html')) {
        currentLang = 'tr';
    } else if (filename.includes('_DE.html')) {
        currentLang = 'de';
    }

    var preferredLang = localStorage.getItem('preferredLang');
    
    // If no preferred language is set, detect from browser
    if (!preferredLang) {
        var browserLang = navigator.language || navigator.userLanguage;
        if (browserLang.startsWith('tr')) {
            preferredLang = 'tr';
        } else if (browserLang.startsWith('de')) {
            preferredLang = 'de';
        } else {
            preferredLang = 'en';
        }
        localStorage.setItem('preferredLang', preferredLang);
    }

    // Redirect if the current language does not match the preferred language
    if (preferredLang !== currentLang) {
        var baseName = filename.replace('_TR.html', '.html').replace('_DE.html', '.html');
        var targetFilename = baseName;
        
        if (preferredLang === 'tr') {
            targetFilename = baseName.replace('.html', '_TR.html');
        } else if (preferredLang === 'de') {
            targetFilename = baseName.replace('.html', '_DE.html');
        }
        
        if (filename !== targetFilename) {
            window.location.replace(targetFilename);
        }
    }
})();

// Function called by language selector to manually change language
function changeLanguage(url) {
    var lang = 'en';
    if (url.includes('_TR.html')) {
        lang = 'tr';
    } else if (url.includes('_DE.html')) {
        lang = 'de';
    }
    localStorage.setItem('preferredLang', lang);
    window.location.href = url;
}
