// Function to execute when button is clicked
function report_db() {
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
        let activeTab = tabs[0];

        // get tab webpage information (URL, webpage name and html <body> content)
        chrome.tabs.sendMessage(activeTab.id, {"message": "start"}, function(response){
            console.log(response.bodyHTML)
            console.log(response.title)
            console.log(response.url)

            // Send info to backend API
            fetch('https://7cvyjy.deta.dev/report', {
                method: 'POST',
                body: JSON.stringify({
                    site_name: response.title,
                    url: response.url,
                    document: response.bodyHTML,
                    label: 'reported',
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
    confirmMessage.innerText = "Thanks! We'll review the information sent";
    document.body.appendChild(confirmMessage);
}

// Function to execute when button is clicked
function get_context() {
    const url = document.getElementById('context-input').value
    console.log("Contextualize pressed")
    console.log(url)
    // Send info to backend API
    fetch('https://7cvyjy.deta.dev/contextualize', {
        method: 'POST',
        body: JSON.stringify({
            url: url,
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    })
    .then((response) => response.json())
    .then((data) => {
        let confirmMessage = document.createElement("P");
        confirmMessage.innerText = "Result:";
        document.body.appendChild(confirmMessage);

        if(data.label !== null){
            confirmMessage = document.createElement("P");
            confirmMessage.innerText = `Found URL reported as: ${data.label}`;
            document.body.appendChild(confirmMessage);
        }
        if(data.website_count !== null){
            confirmMessage = document.createElement("P");
            confirmMessage.innerText = `Website has been reported: ${data.website_count} times`;
            document.body.appendChild(confirmMessage);
        }
    })
    .catch(() => console.log("Oops! Error while making request"));
}

// Bind functions to buttons
document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("report").addEventListener("click", report_db);
    document.getElementById("context-button").addEventListener("click", get_context);
})