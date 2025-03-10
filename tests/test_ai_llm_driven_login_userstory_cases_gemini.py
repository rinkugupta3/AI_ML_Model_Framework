"""
This project automates the creation of structured test cases for validating login and logout functionality
 across multiple browsers, leveraging AI model to generate test scenarios based on a user story.
 The goal is to streamline QA processes by converting natural language requirements from a user story
 into actionable test cases, ensuring comprehensive coverage of functional, security, performance, and
 accessibility requirements.

Use Case
This tool is ideal for QA teams aiming to:
Reduce manual effort in test case design.
Ensure 100% coverage of critical testing dimensions.
Integrate AI-driven test generation into agile workflows.
Standardize test case documentation for compliance and reporting.
"""
# Reads the user story from the .docx file.
# Sends the user story to Gemini AI to generate test cases.
# Formats the test cases based on different categories (functional, negative, edge cases, etc.).
# Saves the test cases to a .txt file.
# pytest -s -v tests/test_ai_llm_driven_login_userstory_cases_gemini.py

import os

import genai as genai
import pytest
import google.generativeai as genai
from dotenv import load_dotenv
import docx

# Load API Key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
# genai.configure(api_key=api_key)
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# File path to the user story document
USER_STORY_PATH = r"C:\Users\dhira\Desktop\Dhiraj HP Laptop\Projects\AI_ML_Model_Framework\Login and Logout Functionality Validation Across Multiple Browsers.docx"


def read_user_story(file_path):
    """
    Reads text content from a .docx file.
    """
    try:
        doc = docx.Document(file_path)
        content = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return content
    except Exception as e:
        print(f"Error reading user story file: {e}")
        return None


def generate_test_cases_from_story(user_story):
    """
    Uses Gemini API to generate diverse test cases based on a user story.
    Returns the generated test cases as a string.
    """
    prompt = f"""
    You are a QA engineer. Generate test cases based on the following user story:

    {user_story}

    The test cases should cover:
    - **Functional scenarios**
    - **Positive scenarios**
    - **Negative scenarios**
    - **Edge cases** (e.g., very long usernames, special characters)
    - **Cross-browser testing** (e.g., Chrome, Firefox, Edge)
    - **Security testing** (e.g., SQL injection, brute force attack)
    - **Performance testing** (e.g., response time, concurrent users)
    - **Accessibility scenarios** covering **ALL** 13 **WCAG 2.1 guidelines**, such as:
        - **Perceivable** (e.g., text alternatives, adaptable content, distinguishable elements)
        - **Operable** (e.g., keyboard accessibility, enough time, seizure prevention, navigability)
        - **Understandable** (e.g., readable text, input assistance)
        - **Robust** (e.g., compatibility with assistive technologies)

    Return the test cases in a structured numbered list format.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating test cases: {e}")
        return None


def save_test_cases(test_cases, filename="generated_test_cases.txt"):
    """
    Saves the generated test cases to a file.
    """
    if not test_cases:
        print("No test cases generated. Exiting.")
        return

    with open(filename, "w", encoding="utf-8") as file:
        file.write(test_cases)

    print(f"Test cases saved to {filename}")


@pytest.mark.parametrize("file_path", [USER_STORY_PATH])
def test_generate_and_save_test_cases_from_story(file_path):
    """
    Test function to generate and save test cases from a user story.
    """
    # Read the user story from the file
    user_story = read_user_story(file_path)

    # Generate test cases using AI
    if user_story:
        test_cases = generate_test_cases_from_story(user_story)

        # Save the test cases to a file
        if test_cases:
            save_test_cases(test_cases, "test_cases_from_user_story.txt")
            assert os.path.exists("test_cases_from_user_story.txt")
        else:
            pytest.fail("Failed to generate test cases.")
    else:
        pytest.fail("Failed to read user story.")


# Run the test manually if needed
if __name__ == "__main__":
    test_generate_and_save_test_cases_from_story(USER_STORY_PATH)
