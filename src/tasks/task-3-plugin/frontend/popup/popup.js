// Function to execute when button is clicked
function report_db() {
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
        let activeTab = tabs[0];
        console.log(activeTab.url)

        // Send info to backend API
        fetch('https://7cvyjy.deta.dev/report', {
            method: 'POST',
            body: JSON.stringify({
                site_name: activeTab.title,
                url: activeTab.url,
                document: activeTab.bodyHTML,
                label: 'reported',
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            },
        })
        .then((response) => response.json())
        .then((json) => console.log(json));
    });

    // Show message to user in popup
    const confirmMessage = document.createElement("P");
    confirmMessage.innerText = "Thanks! We'll review the information sent";
    document.body.appendChild(confirmMessage);
}

// Function to execute when button is clicked
function get_context() {
    chrome.tabs.query({currentWindow: true, active: true}, async function (tabs){
        const activeTab = tabs[0];
        console.log("Contextualize pressed")
        console.log(activeTab.url)

        //Show loading animation
        var loader = document.createElement("div");
        loader.className = "loader";
        loader.appendChild(document.createElement("div"));
        loader.appendChild(document.createElement("div"));
        loader.appendChild(document.createElement("div"));
        var container = document.querySelector(".extension-container");
        container.appendChild(loader);

        // Send info to backend API
        return await fetch('https://7cvyjy.deta.dev/contextualize', {
            method: 'POST',
            body: JSON.stringify({
                url: activeTab.url,
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            },
        })
        .then((response) => response.json())
        .then((data) => {
            // Remove loader animation
            var container = document.querySelector(".extension-container");
            container.removeChild(container.lastChild);
            
            // Report container
            var report = document.createElement("div");
            report.className = "report-container";
            
            // Report elements
            let report_title = document.createElement("h3");
            report_title.innerText = "Result:";
            report.appendChild(report_title);

            if(data.label !== null){
                let report_item1 = document.createElement("P");
                report_item1.innerText = `Found URL reported as: ${data.label}`;
                report.appendChild(report_item1);
            }
            if(data.website_count !== null){
                let report_item2 = document.createElement("P");
                report_item2.innerText = `Website has been reported: ${data.website_count} time` + (data.website_count == 1 ? '' : 's');
                report.appendChild(report_item2);
            }

            // Add report
            container.appendChild(report);
        })
        .catch(() => console.log("Oops! Error while making request"));
    });
}

// Bind functions to buttons
document.addEventListener("DOMContentLoaded", function(){
    //document.getElementById("report").addEventListener("click", report_db);
    document.getElementById("context-button").addEventListener("click", get_context);
})