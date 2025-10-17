const API_URL = 'http://localhost:8000';
let threadId = null;
let currentFileName = null;

// Elements
const uploadSection = document.getElementById('uploadSection');
const chatSection = document.getElementById('chatSection');
const fileInput = document.getElementById('fileInput');
const selectedFile = document.getElementById('selectedFile');
const uploadButton = document.getElementById('uploadButton');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');
const fileInfo = document.getElementById('fileInfo');
const newUploadBtn = document.getElementById('newUploadBtn');

// File selection
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    selectedFile.textContent = `Selected: ${file.name}`;
    uploadButton.classList.add('show');
  } else {
    selectedFile.textContent = '';
    uploadButton.classList.remove('show');
  }
});

// Upload file
uploadButton.addEventListener('click', async () => {
  const file = fileInput.files[0];
  if (!file) return;

  uploadButton.disabled = true;
  uploadButton.textContent = 'Uploading...';

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    const data = await response.json();
    threadId = data.thread_id;
    currentFileName = data.filename;

    // Show chat section
    uploadSection.classList.add('hidden');
    chatSection.classList.add('show');
    fileInfo.textContent = `📄 ${currentFileName}`;
    fileInfo.classList.add('show');
    newUploadBtn.style.display = 'inline-block';

    // Add system message
    addMessage(data.message, 'system');
    messageInput.focus();

  } catch (error) {
    alert(`Error: ${error.message}`);
  } finally {
    uploadButton.disabled = false;
    uploadButton.textContent = 'Upload & Start Chat';
  }
});

// New upload button
newUploadBtn.addEventListener('click', () => {
  threadId = null;
  currentFileName = null;
  fileInput.value = '';
  selectedFile.textContent = '';
  uploadButton.classList.remove('show');
  chatMessages.innerHTML = '';
  uploadSection.classList.remove('hidden');
  chatSection.classList.remove('show');
  fileInfo.classList.remove('show');
  newUploadBtn.style.display = 'none';
});

function addMessage(content, type = 'assistant') {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  
  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';
  contentDiv.textContent = content;
  
  messageDiv.appendChild(contentDiv);
  chatMessages.appendChild(messageDiv);
  
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
  typingIndicator.classList.add('show');
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
  typingIndicator.classList.remove('show');
}

function showError(message) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.textContent = `Error: ${message}`;
  chatMessages.appendChild(errorDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  setTimeout(() => errorDiv.remove(), 5000);
}

async function sendMessage() {
  const message = messageInput.value.trim();
  if (!message || !threadId) return;

  messageInput.disabled = true;
  sendButton.disabled = true;

  addMessage(message, 'user');
  messageInput.value = '';

  showTypingIndicator();

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        thread_id: threadId
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get response');
    }

    const data = await response.json();
    
    hideTypingIndicator();
    addMessage(data.response, 'assistant');

  } catch (error) {
    hideTypingIndicator();
    showError(error.message);
    console.error('Error:', error);
  } finally {
    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.focus();
  }
}

sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});
