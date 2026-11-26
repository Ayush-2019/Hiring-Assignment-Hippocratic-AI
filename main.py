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

# Create the Anthropic client using the API key from the environment
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Send a prompt to Claude and return the text of its reply
def call_claude(prompt: str, max_tokens=2000) -> str:
    resp = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text

# Ask the user what kind of story they want
def get_story_request() -> str:
    print("Hi there! I can tell you a bedtime story. What kind of story would you like to hear?")
    return input("> ")

# Write the first draft of the story
def generate_story(request: str) -> str:
    prompt = f"""
You are a children's story writer. Write an engaging bedtime story for this request:

{request}

The story should:
- Be appropriate for children ages 5-10
- Have a clear beginning, middle, and end
- Teach a positive lesson or moral
- Use creative description to spark the imagination
- Have the tone and style of a classic fairy tale
"""
    return call_claude(prompt)

# Have the judge critique the story
def get_judge_feedback(story: str) -> str:
    prompt = f"""
You are an editor evaluating a children's bedtime story for ages 5-10.

{story}

Give short, specific feedback on age-appropriateness, structure, imagery,
the moral, and overall engagement. List the top fixes needed.
"""
    return call_claude(prompt)

# Rewrite the story using feedback from the judge or the user
def revise_story(story: str, feedback: str) -> str:
    prompt = f"""
Here is a bedtime story for children ages 5-10:

{story}

Rewrite it, applying this feedback while keeping it age-appropriate:

{feedback}

Return only the revised story.
"""
    return call_claude(prompt)

# Run the full flow: draft, judge, revise, then optional user changes
def tell_story():
    request = get_story_request()
    story = generate_story(request)
    feedback = get_judge_feedback(story)
    story = revise_story(story, feedback)
    print(f"\nHere is your story:\n\n{story}\n")

    # Keep revising until the user has no more changes
    while True:
        change = input("Want any changes? (press Enter to finish) > ")
        if not change.strip():
            break
        story = revise_story(story, change)
        print(f"\n{story}\n")

    print("Sleep tight!")

# Main program entry point
if __name__ == "__main__":
    tell_story()
