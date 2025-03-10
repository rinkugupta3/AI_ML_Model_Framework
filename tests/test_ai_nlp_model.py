# NLP Model uses spaCy library as small "en_core_web_sm"
# Install pip install python-docx
# Install pip install spacy
# Install python -m spacy download en_core_web_sm
# pytest -s -v tests/test_ai_nlp_model.py
import os
import datetime
import spacy
import re
import docx  # Import the docx library

# Load a SpaCy language model
try:
    nlp = spacy.load("en_core_web_sm")  # Or a larger model like "en_core_web_lg"
except OSError:
    print("Downloading en_core_web_sm model for SpaCy...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def extract_test_plan_nlp_docx(user_story_file, output_file="auto_test_plan_nlp.docx"):
    """
    Extracts information from a user story file (in .docx format) using SpaCy NLP and generates a draft test plan.
    """

    try:
        # Open the .docx file using the docx library
        doc = docx.Document(user_story_file)
        # Read all the paragraphs from the document into a single string
        user_story_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except FileNotFoundError:
        print(f"Error: User story file '{user_story_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading user story file: {e}")
        return

    # ---  NLP Processing with SpaCy ---
    doc = nlp(user_story_text)

    # --- Extraction Logic (Adapt this to your user story format) ---
    # --- This is still format-dependent but more robust due to SpaCy ---

    # Extract User Story components using regex
    try:
        user_story = re.search(r"As a (.*), I want to (.*) So that (.*)", user_story_text, re.DOTALL).group(0)
        as_a = re.search(r"As a (.*), I want to", user_story_text, re.DOTALL).group(1).strip()
        i_want_to = re.search(r"I want to (.*) So that", user_story_text, re.DOTALL).group(1).strip()
        so_that = re.search(r"So that (.*)", user_story_text, re.DOTALL).group(1).strip()
    except AttributeError:
        print("Warning: Could not fully parse user story using regex. Check the format.")
        user_story = "Could not parse"
        as_a = "Could not parse"
        i_want_to = "Could not parse"
        so_that = "Could not parse"


    # Extract Acceptance Criteria (Improved with sentence segmentation)
    try:
        acceptance_criteria_header = re.search(r"(?i)(Acceptance Criteria:|Acceptance Criteria:)", user_story_text).group(0)
        acceptance_criteria_text = user_story_text.split(acceptance_criteria_header)[1].strip()
        # Splitting the text into sentences using SpaCy
        acceptance_criteria = [sent.text.strip() for sent in nlp(acceptance_criteria_text).sents]


    except:
        acceptance_criteria = ["No acceptance criteria found.  Please add them!"]

    # Extract Scenarios (Improved with sentence segmentation)
    try:
        scenarios_header = re.search(r"(?i)(Scenarios Covered:|Test Scenarios:)", user_story_text).group(0)
        scenarios_text = user_story_text.split(scenarios_header)[1].strip()
        # Splitting the text into sentences using SpaCy
        scenarios = [sent.text.strip() for sent in nlp(scenarios_text).sents]
    except:
        scenarios = ["No scenarios found.  Please add them!"]



    # Current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---  Generate Markdown Content ---

    markdown_content = f"""
# Auto-Generated Test Plan (with SpaCy NLP)

**Generated on:** {timestamp}

## 1. User Story

**As a:** {as_a}

**I want to:** {i_want_to}

**So that:** {so_that}

## 2. Acceptance Criteria

{chr(10).join([f"* {criteria.strip()}" for criteria in acceptance_criteria])}

## 3. Scenarios Covered

{chr(10).join([f"* {scenario.strip()}" for scenario in scenarios])}

## 4. Test Cases (Draft)

This section provides a draft of test cases based on the acceptance criteria and scenarios.  Further refinement is needed.

| Test Case ID | Test Description | Preconditions | Test Steps | Expected Results | Priority |
|---|---|---|---|---|---|
"""

    # Generate basic test cases based on acceptance criteria (very basic)
    for i, criteria in enumerate(acceptance_criteria):
        markdown_content += f"| TC_AUTO_{i+1:03d} | {criteria} | Application is running | TBD | TBD | Medium |\n"  # TBD = To Be Determined

    markdown_content += """
## 5. Test Environment (Example - Customize as needed)

*   Operating System: Tests will be executed on a platform that supports Chromium, Firefox, and WebKit browsers.
*   Browsers: Chromium, Firefox, WebKit
*   Test Framework: Playwright with Python

(Add more details as needed)
"""

    # ---  Write to File ---

    documents_dir = "documents"
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)

    output_path = os.path.join(documents_dir, output_file)

    try:
        with open(output_path, "w") as f:
            f.write(markdown_content)
        print(f"Draft test plan generated successfully at: {output_path}")
    except Exception as e:
        print(f"Error generating test plan: {e}")


# ---  Example Usage ---
# Replace with the actual path to your .docx file
user_story_file = r"C:\Users\dhira\Desktop\Dhiraj HP Laptop\Projects\AI_Model_Driven_TestCases_Automation_Script\Login and Logout Functionality Validation Across Multiple Browsers.docx"
extract_test_plan_nlp_docx(user_story_file)