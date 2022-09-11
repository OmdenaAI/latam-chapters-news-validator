// Function to execute when button is clicked
function popup() {
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
        let activeTab = tabs[0];

        // get tab webpage information (URL, webpage name and html <body> content)
        chrome.tabs.sendMessage(activeTab.id, {"message": "start"}, function(response){
            console.log(response.bodyHTML)
            console.log(response.title)
            console.log(response.url)

            // Send info to backend API
            fetch('https://e0trq0.deta.dev/upload', {
                method: 'POST',
                body: JSON.stringify({
                    site_name: response.title,
                    url: response.url,
                    document: response.bodyHTML,
                    label: 'possibly-fake',
                }),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
            .then((response) => response.json())
            .then((json) => console.log(json));
        });
    });

    // Show message to user in popup
    const confirmMessage = document.createElement("P");
    confirmMessage.innerText = "Gracias! Revisaremos la información enviada / Thanks! We'll review the information sent";
    document.body.appendChild(confirmMessage);
}

// Bind popup() function to button
document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("report").addEventListener("click", popup);
})