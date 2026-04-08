import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import McpTool, ToolSet, ListSortOrder
import logging
# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Connect to the agents client
agents_client = AgentsClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(
        exclude_environment_credential=True, exclude_managed_identity_credential=True
    ),
)

# MCP server configuration
mcp_server_url = "https://mcp-server.ashyground-aaa90e67.southindia.azurecontainerapps.io/mcp"
mcp_server_label = "mcpserver"

# Initialize agent MCP tool
mcp_tool = McpTool(
    server_label=mcp_server_label,
    server_url=mcp_server_url,
)
mcp_tool.set_approval_mode("never")

toolset = ToolSet()
toolset.add(mcp_tool)

# Create agent and process agent run
with agents_client:
    # Create a new agent
    agent = agents_client.create_agent(
        model=model_deployment,
        name="my-mcp-agent",
        instructions="You have access to an MCP server with the tool add(a, b) → returns the sum of two integers, and whenever the user asks to add numbers, you MUST call this tool and NEVER answer directly or invent results."
    )

    print(f"Created agent, ID: {agent.id}")
    print(f"MCP Server: {mcp_tool.server_label} at {mcp_tool.server_url}")

    # Create a thread for communication
    thread = agents_client.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Prompt user for input
    prompt = input("\nHow can I help?: ")

    # Create a message on the thread
    message = agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )
    print(f"Created message, ID: {message.id}")

    # Create and process agent run in thread with MCP tools
    run = agents_client.runs.create_and_process(
        thread_id=thread.id, agent_id=agent.id, toolset=toolset
    )
    print(f"Created run, ID: {run.id}")
    print(f"Run completed with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Display run steps and tool calls
    run_steps = agents_client.run_steps.list(thread_id=thread.id, run_id=run.id)
    for step in run_steps:
        print(f"Step {step['id']} status: {step['status']}")
        step_details = step.get("step_details", {})
        tool_calls = step_details.get("tool_calls", [])
        if tool_calls:
            print("  MCP Tool calls:")
            for call in tool_calls:
                print(f"    Tool Call ID: {call.get('id')}")
                print(f"    Type: {call.get('type')}")
                print(f"    Name: {call.get('name')}")
        print()  # newline between steps

    # Fetch and display all messages
    messages = agents_client.messages.list(
        thread_id=thread.id, order=ListSortOrder.ASCENDING
    )
    print("\nConversation:")
    print("-" * 50)
    for msg in messages:
        if msg.text_messages:
            last_text = msg.text_messages[-1]
            print(f"{msg.role.upper()}: {last_text.text.value}")
            print("-" * 50)

    # Clean up and delete the agent
    # agents_client.delete_agent(agent.id)
    print("Deleted agent")
    logging.basicConfig(level=logging.DEBUG)