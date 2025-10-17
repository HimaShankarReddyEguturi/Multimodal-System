import os
import pypdf
from PIL import Image
from io import BytesIO

def process_file_to_parts(file_path):
    """
    Processes various file types into a list of Gemini-compatible parts (text or PIL.Image objects).

    Args:
        file_path (str): The path to the local file.
        
    Returns:
        list: A list containing strings (text) or PIL.Image objects.
    """

    # Get the file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    # --- Image Files ---
    if file_extension in ['.png', '.jpg', '.jpeg']:
        try:
            # ✅ Safely load image fully into memory and close file handle
            with Image.open(file_path) as img:
                img_copy = img.copy()  # make a memory copy (no open file handle)
            return [img_copy]
        except Exception as e:
            return [f"Error loading image: {e}"]

    # --- PDF Files ---
    elif file_extension == '.pdf':
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return [text]
        except Exception as e:
            return [f"Error processing PDF: {e}"]

    # --- Text or Markdown Files ---
    elif file_extension in ['.txt', '.md']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [f.read()]
        except Exception as e:
            return [f"Error reading text file: {e}"]

    # --- Audio / Video Placeholders ---
    elif file_extension in ['.mp3', '.mp4']:
        return [f"*Placeholder: Content of {file_path} (Transcription needed)*"]

    # --- Word / PowerPoint Placeholders ---
    elif file_extension in ['.docx', '.pptx']:
        return [f"*Placeholder: Content of {file_path} (Docx/Pptx handler needed)*"]

    # --- Unsupported File Types ---
    else:
        return [f"Unsupported file type: {file_extension}"]
