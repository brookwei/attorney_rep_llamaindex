import streamlit as st
import pandas as pd
import tempfile
import json
from llama_cloud_services import LlamaParse
import json
from dotenv import load_dotenv
load_dotenv()
api_key="llx-JC2JgOFpGcobqDpwCaqafLSDWFPuBXlyYz2nNqdaCXroMie3"





json_schema={
  
  "attorneys": {
    "type": "array",
    "minItems": 1,
    "items": {
      "type": "object",
      "properties": {
        "initialContactDate": {
          "type": "string",
          "minLength": 8,
          "maxLength": 8,
          "description": "Date of initial contact by attorney, format CCYYMMDD."
        },
        "firmName": {
          "type": "string",
          "minLength": 5,
          "maxLength": 120,
          "description": "Name of the law firm. Either firmName or attorney fullName is required."
        },
        "firmTaxId": {
          "type": "string",
          "minLength": 9,
          "maxLength": 9,
          "description": "Law firm Taxpayer Identification Number, required when claim status is CLOSEWP."
        },
        "firmPhone": {
          "type": "string",
          "minLength": 10,
          "maxLength": 10,
          "description": "Law firm phone number, numeric, including area code."
        },
        "lastName": {
          "type": "string",
          "minLength": 1,
          "maxLength": 50,
          "description": "Attorney's last name."
        },
        "firstName": {
          "type": "string",
          "minLength": 1,
          "maxLength": 50,
          "description": "Attorney's first name."
        },
        "middleName": {
          "type": "string",
          "minLength": 0,
          "maxLength": 15,
          "description": "Attorney's middle name."
        },
        "suffix": {
          "type": "string",
          "minLength": 0,
          "maxLength": 4,
          "description": "Attorney's suffix (e.g., Jr., Sr.)."
        },
        "fullName": {
          "type": "string",
          "minLength": 3,
          "maxLength": 120,
          "description": "Attorney's full name. Either fullName or name components are required."
        },
        "taxId": {
          "type": "string",
          "minLength": 9,
          "maxLength": 9,
          "description": "Attorney's Taxpayer Identification Number, required when claim status is CLOSEWP."
        },
        "businessPhone": {
          "type": "string",
          "minLength": 10,
          "maxLength": 10,
          "description": "Attorney's business phone number."
        },
        "businessEmail": {
          "type": "string",
          "minLength": 0,
          "maxLength": 50,
          "description": "Attorney's business email address."
        },
        "businessAddress": {
          "type": "object",
          "properties": {
            "streetNumber": {
              "type": "string",
              "minLength": 0,
              "maxLength": 10,
              "description": "Street number of attorney's business address."
            },
            "streetName": {
              "type": "string",
              "minLength": 0,
              "maxLength": 60,
              "description": "Street name, required if addressLine is not provided."
            },
            "aptNumber": {
              "type": "string",
              "minLength": 0,
              "maxLength": 18,
              "description": "Apartment, suite, or building number."
            },
            "addressLine": {
              "type": "string",
              "minLength": 0,
              "maxLength": 100,
              "description": "Full address line, excluding city, state, or zip code."
            },
            "city": {
              "type": "string",
              "minLength": 1,
              "maxLength": 30,
              "description": "City of attorney's business address."
            },
            "state": {
              "type": "string",
              "minLength": 2,
              "maxLength": 2,
              "description": "State of attorney's business address."
            },
            "zipCode": {
              "type": "string",
              "minLength": 5,
              "maxLength": 9,
              "description": "Zip code of attorney's business address."
            }
          },
          "required": ["city", "state", "zipCode"]
        }
      },
      "required": ["initialContactDate", "businessAddress"],
      "oneOf": [
        { "required": ["firmName"] },
        { "required": ["fullName"] }
      ]
    }
  },
  
  "initialDemand": {
    "type": "object",
    "properties": {
      "date": {
        "type": "string",
        "minLength": 8,
        "maxLength": 8,
        "description": "Date of initial demand from attorney, format CCYYMMDD."
      },
      "amount": {
        "type": "string",
        "minLength": 3,
        "maxLength": 11,
        "description": "Amount of initial demand"
      },
      "hasTimeLimit": {
        "type": "string",
        "minLength": 1,
        "maxLength": 1,
        "description": "Is there a time limit? Y = Yes, N = No."
      },
      "isConditional": {
        "type": "string",
        "minLength": 1,
        "maxLength": 1,
        "description": "Is the demand conditional? Y = Yes, N = No."
      }
    },
    "required": ["date", "amount"]
  }
 ,
  "medicalProviders": {
    "type": "array",
    "minItems": 0,
    "items": {
      "type": "object",
      "properties": {
        "lastName": {
          "type": "string",
          "minLength": 1,
          "maxLength": 50,
          "description": "Provider's last name, required if reporting parsed name."
        },
        "firstName": {
          "type": "string",
          "minLength": 1,
          "maxLength": 50,
          "description": "Provider's first name, required if reporting parsed name."
        },
        "middleName": {
          "type": "string",
          "minLength": 0,
          "maxLength": 15,
          "description": "Provider's middle name."
        },
        "suffix": {
          "type": "string",
          "minLength": 0,
          "maxLength": 4,
          "description": "Provider's suffix."
        },
        "fullName": {
          "type": "string",
          "minLength": 3,
          "maxLength": 120,
          "description": "Provider's full name."
        },
        "practiceName": {
          "type": "string",
          "minLength": 3,
          "maxLength": 120,
          "description": "Provider's practice or facility name."
        },
        "phoneNumber": {
          "type": "string",
          "minLength": 10,
          "maxLength": 10,
          "description": "Provider's phone number, numeric, including area code."
        },
        "address": {
          "type": "object",
          "properties": {
            "streetNumber": {
              "type": "string",
              "minLength": 0,
              "maxLength": 10,
              "description": "Provider's address street number."
            },
            "streetName": {
              "type": "string",
              "minLength": 0,
              "maxLength": 60,
              "description": "Provider's address street name, required if addressLine is not provided."
            },
            "aptNumber": {
              "type": "string",
              "minLength": 0,
              "maxLength": 18,
              "description": "Provider's address apartment, suite, or building number."
            },
            "addressLine": {
              "type": "string",
              "minLength": 0,
              "maxLength": 100,
              "description": "Provider's full address line, excluding city, state, or zip code."
            },
            "city": {
              "type": "string",
              "minLength": 1,
              "maxLength": 30,
              "description": "Provider's address city."
            },
            "state": {
              "type": "string",
              "minLength": 2,
              "maxLength": 2,
              "description": "Provider's address state."
            },
            "zipCode": {
              "type": "string",
              "minLength": 5,
              "maxLength": 9,
              "description": "Provider's address zip code."
            }
          },
          "required": ["city", "state", "zipCode"]
        },
        "taxId": {
          "type": "string",
          "minLength": 9,
          "maxLength": 9,
          "description": "Provider's Taxpayer Identification Number, 9 numeric digits."
        },
        "npi": {
          "type": "string",
          "minLength": 10,
          "maxLength": 10,
          "description": "Provider's National Provider Identification Number, 10 numeric digits."
        },
      
        "MedicalAttached": {
          "type": "string",
          "minLength": 1,
          "maxLength": 1,
          "description": "Is there a Medical attachment? Y = Yes, N = No."
        }
      },
      "required": ["phoneNumber", "address", "MedicalAttached"]
    }
  }
}

parser = LlamaParse(api_key=api_key)
def process_pdf_file(pdf_file_name):
    parser = LlamaParse(
        num_workers=8,
        parse_mode="parse_document_with_agent",
        user_prompt="In an attorney letter, there's a deadline or period within which a specific action or response is required, set hasTimeLimit to Y, otherwise set it to N.If the demand is conditional on the recipient's compliance with the terms of the demand, set isConditional to Y, otherwise set it to N.Review the attorney letter. If any sentence indicates that medical bills or records are included or attached, set MedicalAttached to 'Y'. If there is no such indication, set MedicalAttached to 'N'.",
        system_prompt=f"1. Please convert this into a well-structured JSON object 2. Only return file with no extra commentary, markdown, or explanation. 3. Map the extracted information to each field in the JSON schema provided. This is the Json schema:\n\n{json_schema}\n.\n"
    )

    result = parser.parse(pdf_file_name)
    response_dict = result.pages[1].md
    
    if '```json' in response_dict:
        response_dict=  response_dict.split('```json')[1].split('```')[0].strip()
    else:
        response_dict = response_dict.strip()
    return response_dict
    


st.title("Document Extraction with Llama Cloud Services")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_file_path = tmp_file.name
    response_dict= process_pdf_file(temp_file_path)
    st.write("Processing complete!")
    st.json(response_dict, expanded=True)
        
