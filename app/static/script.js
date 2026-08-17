const sendButton =
    document.getElementById("send");

const chatWindow =
    document.getElementById("chat-window");

const questionInput =
    document.getElementById("question");

const uploadInput =
    document.getElementById("upload");

const fileList =
    document.getElementById("file-list");

const dropArea =
    document.querySelector(".drop-area");

const newChatButton =
    document.querySelector(".new-chat");

const suggestionButtons =
    document.querySelectorAll(".suggestion");


// --------------------------------------------------
// Initial State
// --------------------------------------------------

setChatEnabled(false);

addMessage(
    "Welcome to CareerCopilot! Upload your resume to start chatting with your CV.",
    "bot-message"
);


// --------------------------------------------------
// Upload CV
// --------------------------------------------------

uploadInput.addEventListener(
    "change",
    handleUpload
);


async function handleUpload() {

    const file =
        uploadInput.files[0];

    if (!file) {
        return;
    }


    // Show selected file
    fileList.innerHTML = "";

    const listItem =
        document.createElement("li");

    listItem.textContent =
        file.name;

    fileList.appendChild(
        listItem
    );


    addMessage(
        `Processing <strong>${file.name}</strong>...`,
        "bot-message",
        true
    );


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    try {

        setChatEnabled(false);


        const response =
            await fetch(
                "/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to upload resume."
            );
        }


        addMessage(
            `✅ <strong>${file.name}</strong> has been successfully analyzed. You can now ask questions about your resume.`,
            "bot-message",
            true
        );


        setChatEnabled(true);


    } catch (error) {

        addMessage(
            `❌ ${error.message}`,
            "bot-message"
        );

        setChatEnabled(false);
    }
}


// --------------------------------------------------
// Send Message
// --------------------------------------------------

sendButton.addEventListener(
    "click",
    sendMessage
);


questionInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);


async function sendMessage() {

    const question =
        questionInput.value.trim();


    if (!question) {
        return;
    }


    addMessage(
        question,
        "user-message"
    );


    questionInput.value = "";


    sendButton.disabled = true;


    const thinkingMessage =
        addMessage(
            "Thinking...",
            "bot-message"
        );


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: question
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to get response."
            );
        }


        thinkingMessage.remove();


        addMessage(
            data.response,
            "bot-message",
            true
        );


    } catch (error) {

        thinkingMessage.remove();


        addMessage(
            `❌ ${error.message}`,
            "bot-message"
        );

    } finally {

        sendButton.disabled = false;

        questionInput.focus();
    }
}


// --------------------------------------------------
// Add Message
// --------------------------------------------------

function addMessage(
    text,
    className,
    markdown = false
) {

    const message =
        document.createElement("div");


    message.classList.add(
        "message",
        className
    );


    if (markdown) {

        message.innerHTML =
            marked.parse(text);

    } else {

        message.textContent =
            text;
    }


    chatWindow.appendChild(
        message
    );


    chatWindow.scrollTop =
        chatWindow.scrollHeight;


    return message;
}


// --------------------------------------------------
// Enable / Disable Chat
// --------------------------------------------------

function setChatEnabled(enabled) {

    questionInput.disabled =
        !enabled;

    sendButton.disabled =
        !enabled;


    if (enabled) {

        questionInput.placeholder =
            "Ask about your resume...";

    } else {

        questionInput.placeholder =
            "Upload your resume first...";
    }
}


// --------------------------------------------------
// Suggested Questions
// --------------------------------------------------

suggestionButtons.forEach(
    button => {

        button.addEventListener(
            "click",
            () => {

                if (
                    questionInput.disabled
                ) {
                    return;
                }


                questionInput.value =
                    button.textContent.trim();


                questionInput.focus();
            }
        );
    }
);


// --------------------------------------------------
// New Chat
// --------------------------------------------------

newChatButton.addEventListener(
    "click",
    () => {

        chatWindow.innerHTML = "";

        addMessage(
            "New conversation started. Ask me anything about your resume.",
            "bot-message"
        );
    }
);