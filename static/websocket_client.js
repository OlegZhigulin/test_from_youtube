document.addEventListener("DOMContentLoaded", () => {
    const sendMessageButton = document.querySelector("[name=send_message_button]")
    const ws = new WebSocket("ws://localhost:8000/ws");
    ws.onopen = () => {
        console.log("Connect OK");
        sendMessageButton.onclick = () => {
            let msg = {
                type: "message",
                text: document.getElementById("messageText").value,
                date: Date.now(),
                status: "User"
            };
            ws.send(JSON.stringify(msg));
            document.getElementById("messageText").value = "";
            event.preventDefault()
            };
    };
    ws.onmessage = event => {
        let messages = document.getElementById("messages")
        let message = document.createElement("li")
        msg = JSON.parse(event.data)
        let content = document.createTextNode(msg.text)
        message.appendChild(content)
        messages.appendChild(message)
        }
    ws.onclose = function() {
        console.log("Disconect");
    };
}, false);