// language.js
function toLocalFileUrl(url) {
    if (window.location.protocol !== 'file:' || !url) return url;
    if (/^(https?:|mailto:|tel:|javascript:|#)/i.test(url)) return url;
    var match = url.match(/^([^?#]*)(.*)$/);
    if (!match) return url;
    var pathPart = match[1];
    var suffix = match[2] || '';
    if (!pathPart) return url;
    var lastPart = pathPart.substring(pathPart.lastIndexOf('/') + 1);
    if (lastPart.indexOf('.') !== -1 && lastPart !== '.' && lastPart !== '..') {
        return url;
    }
    var sep = pathPart.endsWith('/') ? '' : '/';
    return pathPart + sep + 'index.html' + suffix;
}

(function() {
    var knownBases = [
        'index', 'aboutus', 'Services', 'Contact',
        'industries', 'privacy_pol', 'resources',
        'use-cases', 'mbse-self-assessment'
    ];

    // Define the language based on the current path
    var currentPath = window.location.pathname;
    var cleanPath = currentPath.replace(/\/index\.html$/i, '').replace(/\.html$/i, '').replace(/\/+$/, '');
    var lastSegment = cleanPath.substring(cleanPath.lastIndexOf('/') + 1);

    var baseCheck = lastSegment.replace(/_(TR|DE)$/, '');
    var isSubfolderPage = knownBases.indexOf(baseCheck) !== -1 && lastSegment !== 'index';
    var pageName = isSubfolderPage ? lastSegment : 'index';
    
    var currentLang = 'en';
    if (pageName.endsWith('_TR')) {
        currentLang = 'tr';
    } else if (pageName.endsWith('_DE')) {
        currentLang = 'de';
    }

    var preferredLang = localStorage.getItem('preferredLang');
    
    // If no preferred language is set, detect from browser
    if (!preferredLang) {
        var browserLang = navigator.language || navigator.userLanguage || 'en';
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
    // (Skip auto-redirect for mbse-self-assessment since _DE/_TR variants don't exist yet)
    if (preferredLang !== currentLang && baseCheck !== 'mbse-self-assessment') {
        var baseName = pageName.replace(/_(TR|DE)$/, '');
        var targetPage = baseName;
        
        if (preferredLang === 'tr') {
            targetPage = baseName + '_TR';
        } else if (preferredLang === 'de') {
            targetPage = baseName + '_DE';
        }
        
        if (pageName !== targetPage) {
            var prefix = isSubfolderPage ? '../' : '';
            var rawTarget = (targetPage === 'index' ? (isSubfolderPage ? '../' : './') : prefix + targetPage) + window.location.search + window.location.hash;
            window.location.replace(toLocalFileUrl(rawTarget));
        }
    }

    // When opened locally via file://, rewrite folder links to point to <folder>/index.html
    // so the browser opens the page instead of showing a directory listing.
    if (window.location.protocol === 'file:') {
        document.addEventListener('DOMContentLoaded', function() {
            var links = document.querySelectorAll('a[href]');
            for (var i = 0; i < links.length; i++) {
                var rawHref = links[i].getAttribute('href');
                var updatedHref = toLocalFileUrl(rawHref);
                if (updatedHref !== rawHref) {
                    links[i].setAttribute('href', updatedHref);
                }
            }
        });
        document.addEventListener('click', function(e) {
            var anchor = e.target.closest ? e.target.closest('a[href]') : null;
            if (anchor) {
                var rawHref = anchor.getAttribute('href');
                var updatedHref = toLocalFileUrl(rawHref);
                if (updatedHref !== rawHref) {
                    anchor.setAttribute('href', updatedHref);
                }
            }
        }, true);
    }
})();

// Function called by language selector to manually change language
function changeLanguage(url) {
    var cleanUrl = url.replace(/\/index\.html$/i, '').replace(/\.html$/i, '').replace(/\/+$/, '');
    var lang = 'en';
    if (cleanUrl.endsWith('_TR')) {
        lang = 'tr';
    } else if (cleanUrl.endsWith('_DE')) {
        lang = 'de';
    }
    localStorage.setItem('preferredLang', lang);
    window.location.href = toLocalFileUrl(url);
}
