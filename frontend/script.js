const chatBox = document.getElementById("chat-box");

const userInput = document.getElementById("user-input");

const sendButton = document.getElementById("send-btn");

const chatTitle = document.getElementById("chat-title");



/* ADD USER MESSAGE */

function addUserMessage(message) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        "user-message"
    );


    const messageContent = document.createElement("div");

    messageContent.classList.add(
        "message-content"
    );


    const messageName = document.createElement("div");

    messageName.classList.add(
        "message-name"
    );

    messageName.textContent = "You";


    const messageText = document.createElement("div");

    messageText.classList.add(
        "message-text"
    );

    messageText.textContent = message;


    messageContent.appendChild(messageName);

    messageContent.appendChild(messageText);

    messageDiv.appendChild(messageContent);

    chatBox.appendChild(messageDiv);

    scrollToBottom();

}



/* ADD BOT MESSAGE */

function addBotMessage(message) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        "bot-message"
    );


    const avatar = document.createElement("div");

    avatar.classList.add(
        "avatar"
    );

    avatar.textContent = "🤖";


    const messageContent = document.createElement("div");

    messageContent.classList.add(
        "message-content"
    );


    const messageName = document.createElement("div");

    messageName.classList.add(
        "message-name"
    );

    messageName.textContent = "PlacementPrep AI";


    const messageText = document.createElement("div");

    messageText.classList.add(
        "message-text"
    );

    messageText.textContent = message;


    messageContent.appendChild(messageName);

    messageContent.appendChild(messageText);


    messageDiv.appendChild(avatar);

    messageDiv.appendChild(messageContent);


    chatBox.appendChild(messageDiv);

    scrollToBottom();

}



/* SHOW THINKING */

function showThinking() {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        "bot-message"
    );

    messageDiv.id = "thinking-message";


    const avatar = document.createElement("div");

    avatar.classList.add(
        "avatar"
    );

    avatar.textContent = "🤖";


    const messageContent = document.createElement("div");

    messageContent.classList.add(
        "message-content"
    );


    const messageText = document.createElement("div");

    messageText.classList.add(
        "message-text"
    );

    messageText.textContent = "Thinking...";


    messageContent.appendChild(messageText);

    messageDiv.appendChild(avatar);

    messageDiv.appendChild(messageContent);


    chatBox.appendChild(messageDiv);

    scrollToBottom();

}



/* REMOVE THINKING */

function removeThinking() {

    const thinkingMessage =
        document.getElementById("thinking-message");


    if (thinkingMessage) {

        thinkingMessage.remove();

    }

}



/* SEND MESSAGE */

async function sendMessage() {

    const message =
        userInput.value.trim();


    if (message === "") {

        return;

    }


    addUserMessage(message);


    userInput.value = "";


    userInput.disabled = true;

    sendButton.disabled = true;


    showThinking();


    try {

        const response = await fetch(

            "http://127.0.0.1:5000/chat",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    message: message

                })

            }

        );


        const data =
            await response.json();


        removeThinking();


        if (data.error) {

            addBotMessage(

                "Error: " + data.error

            );

        }

        else {

            addBotMessage(

                data.response

            );

        }

    }


    catch (error) {

        removeThinking();


        addBotMessage(

            "Unable to connect to the backend server. " +
            "Please make sure Python Flask is running."

        );


        console.error(error);

    }


    userInput.disabled = false;

    sendButton.disabled = false;

    userInput.focus();

}



/* PRESS ENTER */

userInput.addEventListener(

    "keydown",

    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }

);



/* SUGGESTED QUESTION */

function askSuggestion(question) {

    userInput.value = question;

    sendMessage();

}



/* CATEGORY */

function selectCategory(category) {

    chatTitle.textContent =
        category + " Preparation";


    const question =

        "I want help with " +
        category +
        " for placement preparation. " +
        "Give me an introduction and tell me " +
        "important topics I should prepare.";


    userInput.value = question;


    sendMessage();

}



/* CLEAR CHAT */

function clearChat() {

    chatBox.innerHTML = "";


    addBotMessage(

        "Chat cleared! 👋\n\n" +
        "Ask me anything related to placement preparation."

    );

}



/* NEW CHAT */

function newChat() {

    clearChat();

    chatTitle.textContent =
        "Placement Preparation Assistant";

}



/* SCROLL */

function scrollToBottom() {

    chatBox.scrollTop =
        chatBox.scrollHeight;

}