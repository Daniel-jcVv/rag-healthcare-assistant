const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const welcomeMessage = document.getElementById('welcomeMessage');
const typingIndicator = document.getElementById('typingIndicator');
const themeToggle = document.getElementById('themeToggle');

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Event Listeners
themeToggle.addEventListener('click', toggleTheme);

userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize theme on load
initTheme();

function askExample(question) {
    userInput.value = question;
    sendMessage();
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) return;

    // Hide welcome message on first interaction
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }

    // Add user message
    addMessage(message, 'user');

    // Clear input
    userInput.value = '';

    // Disable input while processing
    sendBtn.disabled = true;
    userInput.disabled = true;

    // Show typing indicator
    typingIndicator.classList.add('active');
    scrollToBottom();

    try {
        // Call backend API
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: message
            })
        });

        const data = await response.json();

        // Hide typing indicator
        typingIndicator.classList.remove('active');

        if (data.success) {
            // Add bot response with sources
            addMessage(data.answer, 'bot', data.sources);
        } else {
            addMessage('Sorry, I encountered an error processing your question. Please try again.', 'bot');
        }

    } catch (error) {
        console.error('Error:', error);
        typingIndicator.classList.remove('active');
        addMessage('Sorry, I couldn\'t connect to the server. Please check your connection and try again.', 'bot');
    } finally {
        // Re-enable input
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

function addMessage(text, sender, sources = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${sender === 'bot' ? 'bot-avatar' : ''}`;

    const avatarIcon = document.createElement('span');
    avatarIcon.textContent = sender === 'user' ? '👤' : '🤖';
    avatar.appendChild(avatarIcon);

    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;

    // Add sources if provided
    if (sources && sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources';
        sourcesDiv.innerHTML = '<strong>📚 Sources:</strong>';

        sources.forEach((source, index) => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'source-item';
            sourceItem.textContent = `${index + 1}. ${source.document} (Page ${source.page})`;
            sourcesDiv.appendChild(sourceItem);
        });

        content.appendChild(sourcesDiv);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    // Insert before typing indicator
    chatContainer.insertBefore(messageDiv, typingIndicator);

    scrollToBottom();
}

function scrollToBottom() {
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 100);
}

// Focus input on load
window.addEventListener('load', () => {
    userInput.focus();
});
