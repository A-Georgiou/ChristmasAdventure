from flask import Flask, request, jsonify
import replicate
from dotenv import load_dotenv
import os
from functools import lru_cache
import google.generativeai as genai
import typing_extensions as typing
from dataclasses import dataclass
from enum import Enum
import json
from flask_cors import CORS

class StoryPhase(Enum):
    BEGINNING = "beginning"
    MIDDLE = "middle"
    CONCLUSION = "conclusion"

@dataclass
class StoryState:
    def __init__(self, node_count):
        self.node_count: int = node_count
        self.MAX_NODES: int = 5
        self.phase = StoryPhase.BEGINNING
        self.set_phase()

    def should_conclude(self) -> bool:
        return self.node_count >= self.MAX_NODES

    def increment_node(self) -> None:
        self.node_count += 1
        self.set_phase()
        
    def set_phase(self) -> StoryPhase:
        if self.node_count >= self.MAX_NODES:
            self.phase = StoryPhase.CONCLUSION
        elif self.node_count >= 3:
            self.phase = StoryPhase.MIDDLE
        else:
            self.phase = StoryPhase.BEGINNING

class ChristmasStory(typing.TypedDict):
    story: str
    image_prompt: str

class ChristmasChoices(typing.TypedDict):
    choice: list[str]

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

story_model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-002",
  generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=ChristmasStory
    ),
)

choices_model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-002",
  generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=ChristmasChoices
    ),
)

def create_image_prompt(story_data, story_state):
    base_prompt = f"""
    {story_data['image_prompt']}
    
    Artistic style: Detailed digital art, warm lighting, festive colors, magical atmosphere, 
    similar to Disney concept art meets classic Christmas illustrations.
    High quality, highly detailed, warm lighting, Christmas sparkle, 4k, focus on environmental elements.
    """

    cleaned_prompt = " ".join(base_prompt.split())
    return f"{cleaned_prompt}"

def generate_final_story_prompt(story_so_far, chosen_choice):
    text_prompt = """
        You are narrating an urgent Christmas adventure where Santa has mysteriously disappeared just days before Christmas.
        Write in second person ("you") perspective as one of Santa's trusted elves trying to find him.
        This is the final scene, wrap up the story in a satisfying way that resolves the mystery of Santa's disappearance.
        Narrate the conclusion with a hopeful and magical tone.
        Congratulate the player on their bravery and resourcefulness in saving Christmas.

        Each response must include:
        1. A vivid scene description (around 200 words) that:
        - Resolves the mystery of Santa's disappearance.
        - Includes a heartwarming reunion with Santa.
        - Reflects the player's final choice.

        2. "image_prompt": A concise 2-3 sentence prompt for generating an illustration that:
        - Focuses on the main visual elements of the scene.
        - Describes only the key characters and core scene elements.
        - Emphasizes the magical Christmas atmosphere

        Here is the story so far:
        """

    return f"{text_prompt} {story_so_far} The player has decided to make the final choice: {chosen_choice}."

def generate_next_story_prompt(story_so_far, chosen_choice):
    text_prompt = """
        You are narrating an urgent Christmas adventure where Santa has mysteriously disappeared just days before Christmas.
        Write in second person ("you") perspective as one of Santa's trusted elves trying to find him.
       
       1. A vivid scene description (around 100 words) that:
       - Use simple language for children
       - Only add details that will be used in ALL THREE choices
       - Maximum of 3-4 key elements (objects, clues, locations) that need investigation
       - Focus on describing the environment and magical elements

       3. "image_prompt": A concise 2-3 sentence prompt for generating an illustration that:
        - Focuses on the main visual elements of the scene.
        - Describes only the key characters and core scene elements.
        - Emphasizes the magical Christmas atmosphere
        - Avoid including Santa or his likeness in the scene

       Here is the story so far:
    """

    return f"{text_prompt} {story_so_far} The player has decided to do the following choice: {chosen_choice}."

def generate_choices_prompt(story_response):
    return f"""
        You are narrating an urgent Christmas adventure where Santa has mysteriously disappeared just days before Christmas.
        Write in second person ("you") perspective as one of Santa's trusted elves trying to find him.
        
        You must provide 3 distinct choices for what the player can do next, each:
        - Must ONLY use elements from the scene.
        - Must start with action words.

        Here is the scene you must extract your choices from:
        {story_response}
    """

def generate_story_segment(story_so_far: str, chosen_choice: str, story_state: StoryState) -> ChristmasStory:
    if story_state.phase == StoryPhase.CONCLUSION:
        story_prompt = generate_final_story_prompt(story_so_far, chosen_choice)
    else:
        story_prompt = generate_next_story_prompt(story_so_far, chosen_choice)
        if story_state.phase == StoryPhase.MIDDLE:
            story_prompt += "\nStart building towards a conclusion as the search for Santa intensifies."
        if story_state.node_count == story_state.MAX_NODES - 1:
            story_prompt += "\nAdd in a major twist or reveal that sets up the finale of this story."
    story_response = story_model.generate_content(story_prompt)
    story_data = json.loads(story_response.text)
    choices_prompt = generate_choices_prompt(story_data['story'])
    choices = choices_model.generate_content(choices_prompt)
    choices_data = json.loads(choices.text)
    story_data['choices'] = choices_data['choice']
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

app = Flask(__name__)
CORS(app)

@app.route('/api/continue_story', methods=['POST'])
def continue_story():
    data = request.json
    story_so_far = data.get('story_so_far', '')
    chosen_choice = data.get('choice', '')
    node_count = data.get('node_count', 0)
    story_state = StoryState(node_count=node_count)
    story_state.increment_node()
    
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