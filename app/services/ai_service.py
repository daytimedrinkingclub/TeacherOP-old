import os
import logging
import json
import anthropic

# Get the absolute path to the tools.json file
tools_file_path = os.path.join(os.path.dirname(__file__), "tools.json")

# Load tools from the JSON file
with open(tools_file_path) as f:
    tools = json.load(f)

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

class AiService:
    @staticmethod
    def generate_onboarding_question(query: str):
        user_query = query
        messages = [
            {"role": "user", "content": "Hi, I want to learn something, but I am not able to figure out where to begin, or even what to actually learn, can you help me figure out what I should learn?"},
            {"role": "assistant", "content": "Sure, I will assist you. Please tell me what you want to learn, and I will ask you some follow-up questions to help you figure this out."},
            {"role": "user", "content": user_query}
        ]
        while True:
            response = client.messages.create(
                model="claude-3-opus-20240229",
                messages=messages,
                max_tokens=4000,
                temperature=0,
                tools=tools
            )
            if response.stop_reason == "tool_use":
                tool_use = response.content[-1]
                tool_name = tool_use.name
                tool_input = tool_use.input
                print(f"======Claude wants to use the {tool_name} tool======")
                print(f"Tool Input: {json.dumps(tool_input, indent=2)}")

                # Append the assistant message with text and tool_use content
                messages.append(
                    {
                        "role": "assistant",
                        "content": [
                            {"type": "text", "text": response.content[0].text},
                            {"type": "tool_use", "id": tool_use.id, "name": tool_name, "input": tool_input}
                        ]
                    }
                )

                tool_result = AiService.handle_tool_use(tool_name, tool_input)
                print(f"\nTool Result: {tool_result}")

                # Append the tool result as the user message
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": str(tool_result)
                            }
                        ]
                    }
                )
            else:
                print("\nAssistant: " + response.content)
                messages.append({"role": "assistant", "content": response.content})
                user_message = input("\nUser: ")
                messages.append({"role": "user", "content": user_message})
                
            print(response.content)