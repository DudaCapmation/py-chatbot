from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
from openai import OpenAI
import tempfile
import json
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def process_unstructured(request):
    # Preparing the unstructured file content with unstructured, if needed
    from unstructured.partition.auto import partition
    from unstructured.partition.text import partition_text #Using this for now, having issues with libmagic

    file = request.FILES.get("file", None)
    text = request.POST.get("text", "")
    schema = request.POST.get ("schema", "{}")

    unstructured_data = ""

    print("Received request.")

    if file:
        print("File received.")
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
        elements = partition_text(filename=temp_file.name)
        unstructured_data = "\n".join([el.text for el in elements if el.text])
    elif text:
        print("Text received.")
        if file is None:
            unstructured_data = text
        else:
            unstructured_data += "\n" + text
    else:
        return JsonResponse({"error": "No file or text provided."}, status=400)

    # Structuring the data with OpenAI

    prompt = f"""
    Given the following text:
    
    {unstructured_data}
    
    And the following JSON schema:
    
    {schema}
    
    Extract the values from the text and return the JSON with fields filled in.
    Only return the JSON.
    """

    print("Sending prompt to OpenAI.")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    print("Received response from OpenAI.")

    structured_data = response.choices[0].message.content

    print("Returning structured data.")

    return JsonResponse({"structured_data": structured_data}, status=200)