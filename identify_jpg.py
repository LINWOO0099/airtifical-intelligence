import sys
import os

# Add Windows folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Windows"))

from core.registry import SkillRegistry
from dotenv import load_dotenv

load_dotenv()

# Initialize registry and load skills
registry = SkillRegistry()
skills_dir = os.path.join(os.path.dirname(__file__), "Windows", "skills")
registry.load_skills(skills_dir)

# Get the vision skill
vision_skill = registry.skills.get("vision_skill")

if not vision_skill:
    print("Vision skill not available")
    exit(1)

# Image path
image_path = r"assets/_ Even if we forget the faces of our friends_ We will never forget the bonds that were carved into our souls _ 😍❤️__📱iPhone Users_ Tap_zoom in fo_2-OBITO.jpg"

if not os.path.exists(image_path):
    print(f"Image not found: {image_path}")
    exit(1)

print(f"Identifying image: {image_path}")
print("-" * 50)

try:
    # Call the identify_image function
    result = vision_skill.identify_image(image_path)
    print(result)
except Exception as e:
    print(f"Error: {e}")
