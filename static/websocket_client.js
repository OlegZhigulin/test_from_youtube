document.addEventListener("DOMContentLoaded", () => {
    const sendMessageButton = document.querySelector("[name=send_message_button]")
    let clientID = Date.now();
    let ws = new WebSocket(`ws://localhost:8000/ws/${clientID}`);
    ws.onopen = () => {
        console.log("Connect OK");
        sendMessageButton.onclick = () => {
            let msg = {
                type: "message",
                text: document.getElementById("messageText").value,
                date: Date.now(),
                status: "User",
            };
            ws.send(JSON.stringify(msg));
            document.getElementById("messageText").value = "";
            event.preventDefault()
            };
    };
    ws.onmessage = event => {
        let messages = document.getElementById("messages")
        let message = document.createElement("li")
        let data = JSON.parse(event.data)
        let num_message = document.createTextNode(data.numbers + ". ")
        let text_message = document.createTextNode(data.text)
        message.appendChild(num_message)
        message.appendChild(text_message)
        messages.appendChild(message)
        }
    ws.onclose = function() {
        console.log("Disconect");
    };
}, false);