console.log(`Loading page...`)

// Responds to popup.js with the content of current tab
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        sendResponse({url: document.location.href, title: document.title, bodyHTML: document.body.innerHTML});
    }
);
