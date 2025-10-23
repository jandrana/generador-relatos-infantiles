import os
from dotenv import load_dotenv

from google import genai
from google.genai import types
from fpdf import FPDF
from PIL import Image
from io import BytesIO

from pydantic import BaseModel

load_dotenv()

try:
	client = genai.Client(api_key=os.getenv("API_KEY"))
except Exception as e:
	print(f"Error configuring Gemini API: {e}")
	print("Check that the API key is set correctly in the .env file")
	exit()

class Story(BaseModel):
	story_title: str
	story_text: str
	story_characters: list[str]

instructions = """
You are an AI assistant specialized in generating creative and engaging children's stories.
Every story you generate must adhere to the following rules:
- story_text: Must contain between 450 and 550 words.
- Structure: Must follow a clear 3-part structure: 1. Introduction, 2. Rising Action, 3. Conclusion.
- Characters: Must contain at least 3 different characters.
"""

model = "gemini-2.5-flash"


def generate_prompt(prompt):
	try:
		complete_prompt = f""" {instructions}
		User input: {prompt}
		"""
		response = client.models.generate_content(
			model=model,
			contents=complete_prompt,
			config={
				"response_mime_type":"application/json",
				"response_schema":Story.model_json_schema(),
			}
		)
		generated_story: Story = Story.model_validate_json(response.text)
		return generated_story
	except Exception as e:
		print(f"Error generating prompt: {e}")
		return None

def check_response(generated_content: Story):
	if not generated_content:
		print("No content generated.")
		return False
	if len(generated_content.story_characters) < 3:
		print("Generated story does not have at least 3 characters.")
		return False
	word_count = len(generated_content.story_text.split())
	if word_count < 450 or word_count > 550:
		print(f"Generated story length is out of bounds: {word_count} words.")
		return False
	return True

def generate_trace_file(attempts: list[Story]):
	try:
		with open("generation_traces.txt", "w") as f:
			for i, attempt in enumerate(attempts):
				f.write(f"Attempt {i+1}:\n")
				f.write(f"Title: {attempt.story_title}\n")
				f.write(f"Characters: {', '.join(attempt.story_characters)}\n")
				f.write(f"Text: {attempt.story_text}\n\n")
		print("Trace file 'generation_traces.txt' created successfully.")
	except Exception as e:
		print(f"Error creating trace file: {e}")

def generate_image(generated_story: Story):
	try:
		prompt = "Illustrate a scene from the following children's story: " + generated_story.story_text
		response = client.models.generate_content(
			    model="gemini-2.5-flash-image",
    			contents=[prompt]
		)
		for part in response.candidates[0].content.parts:
			if part.text is not None:
				print(part.text)
			elif part.inline_data is not None:
				image = Image.open(BytesIO(part.inline_data.data))
				image.save("generated_image.png")
	except Exception as e:
		print(f"Error generating image: {e}")

def generate_pdf(story: Story):
	try:
		out_dir = "output"
		os.makedirs(out_dir, exist_ok=True)

		filename = "generated_story.pdf"
		out_path = os.path.join(out_dir, filename)

		pdf = FPDF()
		pdf.set_auto_page_break(auto=True, margin=15)
		pdf.add_page()

		# Generate and add image
		# try:
		# 	generate_image(story)
		# 	if os.path.exists("generated_image.png"):
		# 		pdf.image("generated_image.png", x=10, y=10, w=pdf.w - 20)
		# 		pdf.ln(85)
		# except Exception as e:
		# 	print(f"Error generating image: {e}. Continuing without image.")

		# Title
		pdf.set_font("Arial", "B", 16)
		pdf.multi_cell(0, 10, story.story_title, align="C")
		pdf.ln(4)

		# Characters
		pdf.set_font("Arial", "I", 12)
		pdf.multi_cell(0, 8, "Characters: " + ", ".join(story.story_characters))
		pdf.ln(6)

		# Story text (preserve paragraphs)
		pdf.set_font("Arial", "", 12)
		for para in story.story_text.split("\n\n"):
			pdf.multi_cell(0, 7, para.strip())
			pdf.ln(3)

		pdf.output(out_path)
		print(f"PDF saved to {out_path}")
	except Exception as e:
		print(f"Error generating PDF: {e}")

def main():
	user_input = input("What story would you like to generate?: ")
	generated_story = generate_prompt(user_input)
	if check_response(generated_story):
		print("Story generated successfully!")
		generate_pdf(generated_story)
	else:
		attempts = [generated_story]
		max_retries = 3
		for attempt in range(max_retries):
			print(f"Retrying generation... Attempt {attempt + 1}")
			generated_story = generate_prompt(user_input)
			attempts.append(generated_story)
			if check_response(generated_story):
				print("Story generated successfully on retry!")
				generate_pdf(generated_story)
				break

if __name__ == "__main__":
	main()

