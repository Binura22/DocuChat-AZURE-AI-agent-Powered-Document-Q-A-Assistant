import os
from typing import Optional
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()


class AzureAIAgentManager:
    def __init__(self):
        # Initialize project client
        self.project_client = self._setup_project_client()
        self.agent_id = os.getenv("AGENT_ID")

    def _setup_project_client(self):
        """Setup Azure AI Project Client"""
        endpoint = os.getenv("PROJECT_ENDPOINT")
        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        resource_group_name = os.getenv("AZURE_RESOURCE_GROUP")
        project_name = os.getenv("AZURE_PROJECT_NAME")

        if not all([endpoint, subscription_id, resource_group_name, project_name]):
            raise ValueError("Missing required Azure environment variables.")

        return AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(),
            subscription_id=subscription_id,
            resource_group_name=resource_group_name,
            project_name=project_name,
        )

    def create_thread_with_document(self, filename: str, content: str) -> str:
        """Create a new thread with document content as context"""
        
        # Create initial message with document content
        initial_message = f"""I have uploaded a document called "{filename}". Here is its content:

---BEGIN DOCUMENT---
{content}
---END DOCUMENT---

I will ask you questions about this document. Please answer based on the information provided above."""

        # Create thread and run with initial message
        run = self.project_client.agents.create_thread_and_process_run(
            agent_id=self.agent_id,
            thread={
                "messages": [
                    {
                        "role": "user",
                        "content": initial_message,
                    }
                ]
            }
        )
        
        # Check status
        if run.status == "failed":
            error_msg = getattr(run, 'last_error', 'Unknown error')
            raise RuntimeError(f"Failed to create thread: {error_msg}")
        
        # Return the thread_id
        return run.thread_id

    def send_message_and_run(self, thread_id: Optional[str], user_message: str):
        """Send message and get agent response"""
        
        if not thread_id:
            raise ValueError("Thread ID is required")
        
        try:
            # Get the messages operations from agents
            messages_ops = self.project_client.agents.messages
            
            # Create message
            messages_ops.create(
                thread_id=thread_id,
                role="user",
                content=user_message,
            )
            
            # Create and process run
            runs_ops = self.project_client.agents.runs
            run = runs_ops.create_and_process(
                thread_id=thread_id,
                agent_id=self.agent_id,
            )
            
            # Check status
            if run.status == "failed":
                error_msg = getattr(run, 'last_error', 'Unknown error')
                raise RuntimeError(f"Run failed: {error_msg}")
            
            # Get messages
            messages_list = list(messages_ops.list(thread_id=thread_id))
            
            # Get the latest assistant message
            for msg in messages_list:
                if msg.role == "assistant" and msg.content:
                    for content_item in msg.content:
                        if hasattr(content_item, 'text'):
                            return thread_id, content_item.text.value
            
            return thread_id, "No response from agent."
            
        except Exception as e:
            raise RuntimeError(f"Error processing message: {str(e)}")