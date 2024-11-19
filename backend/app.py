from flask import Flask, request, jsonify
import replicate
import os
from functools import lru_cache
import google.generativeai as genai
import typing_extensions as typing
from dataclasses import dataclass
from enum import Enum
import json

class StoryPhase(Enum):
    BEGINNING = "beginning"
    MIDDLE = "middle"
    CONCLUSION = "conclusion"

@dataclass
class StoryState:
    node_count: int = 0
    MAX_NODES: int = 8
    phase: StoryPhase = StoryPhase.BEGINNING

    def should_conclude(self) -> bool:
        return self.node_count >= self.MAX_NODES

    def increment_node(self) -> None:
        self.node_count += 1
        if self.node_count >= self.MAX_NODES:
            self.phase = StoryPhase.CONCLUSION
        elif self.node_count > 3:
            self.phase = StoryPhase.MIDDLE

class ChristmasStory(typing.TypedDict):
    story: str
    choices: list[str]
    image_prompt: str

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=ChristmasStory
    ),
)

def create_image_prompt(story_data, story_state):
    base_prompt = f"""
    {story_data['image_prompt']}
    
    Artistic style: Detailed digital art, warm lighting, festive colors, magical atmosphere, 
    similar to Disney concept art meets classic Christmas illustrations.
    High quality, highly detailed, warm lighting, Christmas sparkle, 4k
    """

    cleaned_prompt = " ".join(base_prompt.split())
    return f"{cleaned_prompt}"

def generate_final_story_prompt(story_so_far, chosen_choice):
    text_prompt = """
        You are narrating an urgent Christmas adventure where Santa has mysteriously disappeared just days before Christmas.
        Write in second person ("you") perspective as one of Santa's trusted elves trying to find him.
        Each scene should build tension while maintaining a magical, hopeful tone.
        This is the final prompt, wrap up the story in a satisfying way that resolves the mystery of Santa's disappearance.
        Congratulate the player on their bravery and resourcefulness in saving Christmas.

        Each response must include:
        1. A vivid scene description (around 250 words) that:
        - Resolves the mystery of Santa's disappearance
        - Includes magical Christmas elements
        - Describes the North Pole environment
        - Reflects the player's final choice.

        2. Exactly 3 distinct choices for what to do next, each:
        - Starting with an action verb
        - Relating to investigating Santa's disappearance
        - Staying within this area of the north pole and ending the story.

        3. "image_prompt": A concise 2-3 sentence prompt for generating an illustration that:
        - Focuses on the main visual elements of the scene
        - Describes only the key characters and core scene elements
        - Emphasizes the magical Christmas atmosphere
        - Uses clear, specific visual language

        Here is the story so far:
        """

    return f"{text_prompt} {story_so_far} The player has decided to make the final choice: {chosen_choice}."

def generate_next_story_prompt(story_so_far, chosen_choice):
    text_prompt = """
        You are narrating an urgent Christmas adventure where Santa has mysteriously disappeared just days before Christmas.
        Write in second person ("you") perspective as one of Santa's trusted elves trying to find him.
        Each scene should build tension while maintaining a magical, hopeful tone.

        Each response must include:
        1. A vivid scene description (around 100 words) that:
        - Advances the search for Santa
        - Includes magical Christmas elements
        - Describes the North Pole environment
        - Hints at possible clues about Santa's whereabouts
        - Concise and engaging to keep the player invested

        2. Exactly 3 distinct choices for what to do next, each:
        - Starting with an action verb
        - Relating to investigating Santa's disappearance
        - Leading to different areas of the North Pole or following different clues

        3. "image_prompt": A concise 2-3 sentence prompt for generating an illustration that:
        - Focuses on the main visual elements of the scene
        - Describes only the key characters and core scene elements
        - Emphasizes the magical Christmas atmosphere
        - Uses clear, specific visual language

        Here is the story so far:
    """

    return f"{text_prompt} {story_so_far} The player has decided to do the following choice: {chosen_choice}."

def generate_story_segment(story_so_far: str, chosen_choice: str, story_state: StoryState) -> ChristmasStory:
    """Generate next story segment based on current state"""
    
    if story_state.phase == StoryPhase.CONCLUSION:
        prompt = generate_final_story_prompt(story_so_far, chosen_choice)
    else:
        prompt = generate_next_story_prompt(story_so_far, chosen_choice)
        if story_state.phase == StoryPhase.MIDDLE:
            prompt += "\nStart building towards a conclusion as the search for Santa intensifies."
    response = model.generate_content(prompt)
    story_data = json.loads(response.text)
    story_state.increment_node()
    
    return story_data

@lru_cache(maxsize=100)
def generate_image(prompt):
    input = {"prompt": prompt}
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input=input
    )
    return output[0].url

def save_image(output):
    for index, item in enumerate(output):
        with open(f"output_{index}.webp", "wb") as file:
            file.write(item.read())

@app.route('/api/continue_story', methods=['POST'])
def continue_story():
    data = request.json
    story_so_far = data.get('story_so_far', '')
    chosen_choice = data.get('choice', '')
    node_count = data.get('node_count', 0)
    story_state = StoryState(node_count=node_count)
    
    try:
        story_data = generate_story_segment(story_so_far, chosen_choice, story_state)
        image_prompt = create_image_prompt(story_data, story_state)
        image_url = generate_image(image_prompt)
        
        return jsonify({
            'story': story_data['story'],
            'choices': story_data['choices'],
            'image_url': image_url,
            'node_count': story_state.node_count,
            'is_conclusion': story_state.phase == StoryPhase.CONCLUSION
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app = Flask(__name__)