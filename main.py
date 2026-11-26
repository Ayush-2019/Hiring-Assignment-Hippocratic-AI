import os
import anthropic
from typing import List, Dict

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

If I could spend more time on this project, I would focus on a few enhancements:

1. Allow the user to provide more specific story parameters up front, such as character names, setting, or key plot points to include. This would make the stories more personalized.
2. Experiment with using Claude's multi-shot prompting to have the judge and writer engage in back-and-forth collaboration to iteratively improve the story before presenting it.
3. Add functionality to save the generated stories to a file or database so the user can access a library of past tales.
4. Explore using Claude's tone and personality controls to generate stories in different styles (for example: rhyming)

"""

# Load API key from environment variable
api_key = os.environ["ANTHROPIC_API_KEY"]

# Define function to call Anthropic Claude API
def call_claude(messages: List[Dict], model="claude-v1.3-haiku-5.5", max_tokens=2000) -> str:
    client = anthropic.Client(api_key)
    resp = client.chat_completion(
        prompt=anthropic.HUMAN_PROMPT,
        messages=messages, 
        model=model,
        max_tokens_to_sample=max_tokens,
    )
    return resp.completion

# Define function to get story request from user
def get_story_request() -> str:
    print("Hi there! I can tell you a bedtime story. What kind of story would you like to hear?")
    return input("> ")

# Define function to generate story based on request
def generate_story(request: str) -> str:
    story_prompt = f"""
You are a children's story writer. Your task is to write an engaging bedtime story 
based on the following request:

{request}

The story should:
- Be appropriate for children ages 5-10 
- Have a clear beginning, middle, and end
- Teach a positive lesson or moral
- Use creative description to spark the imagination
- Have the tone and style of a classic fairy tale

Story:
"""
    story = call_claude([{"role": "system", "content": story_prompt}])
    return story

# Define function to get feedback from Claude judge
def get_judge_feedback(story: str) -> str:
    judge_prompt = f"""
You are an editor evaluating a children's bedtime story for quality. 
Please provide constructive feedback on the following story:

{story}

Evaluate the story on:
- Age-appropriateness for 5-10 year olds
- Story structure and completeness 
- Vividness of description 
- Positive lesson or moral
- Overall engagement and quality

Provide specific suggestions for improvement if applicable.

Feedback:
"""
    feedback = call_claude([{"role": "system", "content": judge_prompt}])
    return feedback

# Define function to ask user if they want to regenerate
def get_user_regen_choice(feedback: str) -> bool:
    print(f"Here is some feedback on the story:\n{feedback}")
    print("Would you like me to try generating the story again? (y/n)")
    choice = input("> ")
    return choice.lower().startswith('y')

# Define main storytelling loop  
def tell_story():
    request = get_story_request()
    
    while True:
        story = generate_story(request)
        print(f"\nHere is a story for you:\n\n{story}\n")
        
        feedback = get_judge_feedback(story)  
        regen = get_user_regen_choice(feedback)
        
        if not regen:
            break
        
    print("I hope you enjoyed the bedtime story! Sleep tight!")

# Main program entry point
if __name__ == "__main__":
    print(system_diagram)
    tell_story()
