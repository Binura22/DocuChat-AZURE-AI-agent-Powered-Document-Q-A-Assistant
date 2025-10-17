# DocuChat - AI-Powered Document Q&A Assistant

DocuChat is an intelligent document question-answering system built with Azure AI Foundry. Upload any text document and ask questions about its content using natural language.

## 🌟 Features

- **Document Upload**: Upload .txt files for analysis
- **Intelligent Q&A**: Ask questions about your document in natural language
- **Conversation Memory**: Maintains context throughout the conversation
- **Modern UI**: Clean, responsive interface with real-time chat
- **Azure AI Powered**: Leverages Azure AI Foundry's agent capabilities

## 📁 Project Structure

```
AZURE_Agent_project/
│
├── backend/
│   ├── .env                    # Environment variables (Azure credentials)
│   ├── main.py                 # FastAPI application
│   ├── agent_manager.py        # Azure AI Agent manager
│   └── requirements.txt        # Python dependencies
│
└── frontend/
    └── index.html             # Web interface
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Azure AI Foundry project with an agent deployed
- Azure subscription with proper credentials

### Installation

1. **Clone or download the project**

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the `backend` folder with the following:
   ```
   PROJECT_ENDPOINT=your-project-endpoint
   MODEL_DEPLOYMENT_NAME=your-model-deployment
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   AZURE_RESOURCE_GROUP=your-resource-group
   AZURE_PROJECT_NAME=your-project-name
   AGENT_ID=your-agent-id
   ```

   **How to get these values:**
   - Go to [Azure AI Foundry](https://ai.azure.com)
   - Open your project
   - Navigate to "Project settings" for endpoint and IDs
   - Navigate to "Agents" to get your Agent ID

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   The backend will run at: `http://localhost:8000`

2. **Open the Frontend**
   - Navigate to the `frontend` folder
   - Double-click `index.html` to open in your browser
   
   Alternative: Use a local server
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   Then open: `http://localhost:3000`

## 📖 Usage

1. **Upload a Document**
   - Click "Choose File" and select a .txt file
   - Click "Upload & Start Chat"
   - Wait for the upload to complete

2. **Ask Questions**
   - Type your question in the input box
   - Press Enter or click "Send"
   - The AI will answer based on the document content

3. **Upload New Document**
   - Click "Upload New Document" button in the header
   - Start a fresh conversation with a different file

## 🛠️ Technical Details

### Backend (FastAPI)

- **Framework**: FastAPI
- **AI Service**: Azure AI Foundry (Agents API)
- **Authentication**: Azure Default Credentials
- **Key Endpoints**:
  - `POST /upload` - Upload document and create thread
  - `POST /chat` - Send message and get response
  - `GET /health` - Health check

### Frontend (HTML/CSS/JavaScript)

- **Pure Vanilla JavaScript** (no frameworks required)
- **Responsive Design** with modern gradient UI
- **Real-time Chat** interface
- **File Upload** with drag-and-drop support

### Azure AI Agent Configuration

Your Azure AI agent should have these instructions:

```
You are a helpful AI assistant that answers questions about documents. 
When a user uploads a document, they will provide its content to you. 
Answer questions accurately based on the document content provided. 
If the answer is not in the document, say so clearly.
```

## 🔧 Configuration

### Backend Configuration (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `PROJECT_ENDPOINT` | Azure AI Project endpoint URL | `https://your-project.services.ai.azure.com/api/projects/your-project` |
| `MODEL_DEPLOYMENT_NAME` | Deployed model name | `gpt-4o-mini` |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `AZURE_RESOURCE_GROUP` | Resource group name | `my-resource-group` |
| `AZURE_PROJECT_NAME` | AI Foundry project name | `my-ai-project` |
| `AGENT_ID` | Agent identifier | `asst_xxxxxxxxxxxxx` |

### Frontend Configuration (index.html)

Change the API URL if your backend runs on a different port:
```javascript
const API_URL = 'http://localhost:8000';  // Change if needed
```

## 📦 Dependencies

### Backend Requirements
```
fastapi
uvicorn
python-dotenv
azure-identity
azure-ai-projects
azure-ai-agents
python-multipart
```

### Frontend Requirements
- Modern web browser (Chrome, Firefox, Edge, Safari)
- JavaScript enabled

## 🐛 Troubleshooting

### Backend Issues

**Error: Missing required Azure environment variables**
- Check that all variables in `.env` are filled in correctly
- Ensure no extra spaces in variable values

**Error: Authentication failed**
- Run `az login` to authenticate with Azure CLI
- Verify your Azure credentials have proper permissions

**Error: Agent not found**
- Verify the `AGENT_ID` in your `.env` file
- Check that the agent exists in your Azure AI Foundry project

### Frontend Issues

**CORS Error**
- Ensure the FastAPI backend has CORS middleware enabled (already included)
- Check that the API_URL in index.html matches your backend URL

**File Upload Failed**
- Only .txt files are supported
- File must be UTF-8 encoded
- Check file size (large files may take time)

**Chat Not Working**
- Ensure you've uploaded a document first
- Check browser console (F12) for errors
- Verify backend is running at http://localhost:8000

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore` file
- Use Azure Managed Identity in production
- Restrict CORS origins in production environments

## 📝 Example Use Cases

- **Research**: Upload academic papers and ask questions
- **Legal**: Analyze contracts and terms of service
- **Education**: Study from textbooks and notes
- **Business**: Review reports and documentation
- **Personal**: Analyze any text-based content

## 🆘 Support

For issues related to:
- **Azure AI Foundry**: Check [Azure AI documentation](https://learn.microsoft.com/azure/ai-studio/)
- **FastAPI**: See [FastAPI documentation](https://fastapi.tiangolo.com/)
- **This project**: Open an issue in the repository


---

*Last Updated: October 2025*
