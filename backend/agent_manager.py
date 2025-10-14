# backend/agent_manager.py
import os
import time
from typing import Optional, Tuple
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool, ToolSet
from .tools import get_company_details

class AzureAIAgentManager:
    def __init__(self):
        self.project_client = self._setup_project_client()
        self.model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")
        self.agent_toolset = self._setup_toolset()
        self.project_client.agents.enable_auto_function_calls(self.agent_toolset)

    def _setup_project_client(self):
        endpoint = os.getenv("PROJECT_ENDPOINT")
        if not endpoint:
            raise ValueError("PROJECT_ENDPOINT missing in .env")
        return AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )

    def _setup_toolset(self):
        user_functions = {get_company_details}
        functions = FunctionTool(user_functions)
        toolset = ToolSet()
        toolset.add(functions)
        return toolset

    def get_or_create_agent(self, agent_id: Optional[str] = None):
        if agent_id:
            return self.project_client.agents.get_agent(agent_id)
        # Create new
        agent = self.project_client.agents.create_agent(
            model=self.model_deployment_name,
            name="company-info-web-agent",
            instructions=(
                "You are an expert assistant that provides company information. "
                "Answer user queries about the company's details, mission, vision, "
                "values, contact info, and legal policies. Always provide accurate, "
                "clear, and professional responses."
            ),
            description="Web-based company info assistant",
            toolset=self.agent_toolset
        )
        return agent

    def get_or_create_thread(self, thread_id: Optional[str] = None):
        if thread_id:
            return self.project_client.agents.threads.get(thread_id)
        return self.project_client.agents.threads.create()

    def send_message_and_run(self, thread_id: str, agent_id: str, user_message: str):
        # Send message
        self.project_client.agents.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )

        # Run agent
        run = self.project_client.agents.runs.create_and_process(
            thread_id=thread_id,
            agent_id=agent_id
        )

        # Poll until completion
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = self.project_client.agents.runs.get(thread_id=thread_id, run_id=run.id)
            if run.status == "requires_action":
                # Auto-handled by enable_auto_function_calls()
                # But if needed, you can add manual handling here
                pass

        if run.status == "failed":
            raise RuntimeError(f"Run failed: {run.last_error}")

        # Get latest assistant message
        messages = self.project_client.agents.messages.list(thread_id=thread_id)
        assistant_msg = next((m for m in messages if m["role"] == "assistant"), None)
        if assistant_msg and assistant_msg["content"]:
            return assistant_msg["content"][0]["text"]["value"]
        return "No response from agent."