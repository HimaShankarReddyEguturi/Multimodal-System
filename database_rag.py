import os
from google import genai
from google.genai import types

# Initialize the Gemini Client. Assumes GEMINI_API_KEY is set in environment.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    # Fallback/Error state for the application

def answer_query_with_context(query, all_processed_parts):
    """
    Generates a natural language answer using the Gemini model.
    
    Args:
        query (str): The user's question.
        all_processed_parts (list): All content (text, images, placeholders) processed from input files.
        
    Returns:
        str: The natural language response from Gemini.
    """
    
    # 1. Construct the System Instruction and Context
    # We combine the user query, instructions, and ALL content into one prompt/API call.
    
    # Text part of the prompt
    system_instruction = """
    You are an expert Multimodal Data Processing System. Your task is to answer a user's question 
    based on the provided context, which includes documents, images, and other file content.
    
    RULES:
    1. Use ONLY the provided context and images to formulate your answer.
    2. If the answer is not in the context, state clearly: "I cannot find the answer in the provided documents."
    3. Maintain a helpful and professional tone.
    """

    # 2. Build the API contents list
    
    # Start with the system instruction and user query text
    contents = [system_instruction, "USER QUESTION:", query]
    
    # Append all multimodal parts (text and images)
    # The Gemini API handles mixed list of text (str) and image (PIL.Image) objects.
    contents.extend(all_processed_parts)
    
    # 3. Generation (Using gemini-2.5-flash for speed and multimodal capability)
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents
        )
        return response.text
        
    except Exception as e:
        return f"An error occurred during generation. Check API key and context size: {e}"