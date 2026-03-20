from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

def main():
    # Create an AIProjectClient using your Foundry project endpoint
    project_client = AIProjectClient(
        endpoint="https://dqwdwfsfsdfewf.services.ai.azure.com/api/projects/proj-default",
        credential=DefaultAzureCredential()
    )

    # Get an OpenAI client from the project client
    openai_client = project_client.get_openai_client()

    user_prompt = "Analyze the sentiment of this text: I love using Azure AI services!"

    # Call the agent by name via the OpenAI Responses API
    response = openai_client.responses.create(
        input=[{"role": "user", "content": user_prompt}],
        extra_body={
            "agent_reference": {
                "name": "my-agent-incodebuild1",
                "type": "agent_reference"
            }
        },
    )

    print(response.output_text)

    # Optionally inspect full response JSON to see which tools the agent called
    # print(response.model_dump_json())

if __name__ == "__main__":
    main()
