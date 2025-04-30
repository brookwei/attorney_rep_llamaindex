from mistralai import Mistral, DocumentURLChunk
from mistralai.models import OCRResponse
import os
from dotenv import load_dotenv
from pathlib import Path
import json
load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"] #create .env and save your true api key under "Mistral_API_KEY"
client = Mistral(api_key=api_key)
# List of PDF files and corresponding output file names
def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    """
    Replace image placeholders in markdown with base64-encoded images.

    Args:
        markdown_str: Markdown text containing image placeholders
        images_dict: Dictionary mapping image IDs to base64 strings

    Returns:
        Markdown text with images replaced by base64 data
    """
    for img_name, base64_str in images_dict.items():
        markdown_str = markdown_str.replace(
            f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})"
        )
    return markdown_str

def get_combined_markdown(ocr_response: OCRResponse) -> str:
    """
    Combine OCR text and images into a single markdown document.

    Args:
        ocr_response: Response from OCR processing containing text and images

    Returns:
        Combined markdown string with embedded images
    """
    markdowns: list[str] = []
    # Extract images from page
    for page in ocr_response.pages:
        image_data = {}
        for img in page.images:
            image_data[img.id] = img.image_base64
        # Replace image placeholders with actual images
        markdowns.append(replace_images_in_markdown(page.markdown, image_data))

    return "\n\n".join(markdowns)


#JSON schema to a file
schema_file_path = "json_schema.json"
with open(schema_file_path, "r") as schema_file:
    json_schema = json.load(schema_file)
system_prompt = f"""

You are a JSON extraction assistant. You will be given a block of Markdown containing a legal demand letter. 
Your job is to return only valid JSON that matches this schema:
- If a field is not present in the letter add in a question mark (?) as the value.
Here the the json schema summary:
{json_schema}

"""

user_prompt =f"""
"- If there's a deadline or period within which a specific action or response is required, set hasTimeLimit to Y, otherwise set it to N.
 - If the demand is conditional on the recipient's compliance with the terms of the demand, set isConditional to Y, otherwise set it to N.
 - All dates must be in CCYYMMDD (e.g. 20230510).
 - Amounts must be strings of digits (no commas or decimals).
 - Phone numbers must be 10 numeric digits.
 - Arrays (e.g. attorneys[], medicalProviders[]) must list each entry as an object.
 - Do not output any commentary, only the JSON root object.
"""
def process_pdf_file(pdf_file_name):

    pdf_file = Path(pdf_file_name)
   
    # Upload PDF file to Mistral's OCR service
    uploaded_file = client.files.upload(
        file={
            "file_name": pdf_file.stem,
            "content": pdf_file.read_bytes(),
        },
        purpose="ocr",
    )

    # Get URL for the uploaded file
    signed_url = client.files.get_signed_url(file_id=uploaded_file.id)

    # Process PDF with OCR, including embedded images
    pdf_response = client.ocr.process(
        document=DocumentURLChunk(document_url=signed_url.url),
        model="mistral-ocr-latest",
        include_image_base64=True
    )

    # Extract markdown from full PDF OCR result
    pdf_ocr_markdown = get_combined_markdown(pdf_response)

    # Get structured response using pixtral-12b-latest
    chat_response = client.chat.complete(
        model="pixtral-12b-latest",
       messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{pdf_ocr_markdown} +\n\n {user_prompt}"} #put the markdown in the user content
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    # Parse and save JSON response
    response_dict = json.loads(chat_response.choices[0].message.content)
    return response_dict
  
