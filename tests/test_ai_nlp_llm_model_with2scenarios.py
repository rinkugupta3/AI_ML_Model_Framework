"""
This project leverages Natural Language Processing (NLP) with spaCy and a Large Language Model (LLM)
through the Gemini API to automate the generation of comprehensive test cases from user stories.
The generated test cases encompass functional, security, performance, accessibility (WCAG 2.1 compliance),
and cross-browser testing scenarios. The script handles API rate limits and saves the generated test cases
to a specified directory.
"""
# python tests/test_ai_nlp_llm_model_with2scenarios.py
import os
import time
import logging
import spacy
import google.generativeai as genai
from dotenv import load_dotenv
import docx


# Load API Key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Load a spaCy model (you might need to download one)
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# File path to the user story document
USER_STORY_PATH = r"C:\Users\dhira\Desktop\Dhiraj HP Laptop\Projects\AI_ML_Model_Framework\Login and Logout Functionality Validation Across Multiple Browsers.docx"

# Directory to store logs
LOGS_DIR = "logs"

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure Logging
logging.basicConfig(level=logging.INFO,  # Set the desired logging level
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=os.path.join(LOGS_DIR, 'test_case_generator_1.log'))  # Save to a file in the logs directory

def read_user_story(file_path):
    """Reads text content from a .docx file."""
    try:
        doc = docx.Document(file_path)
        content = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return content
    except Exception as e:
        print(f"Error reading user story file: {e}")
        return None


def analyze_user_story(user_story):
    """Performs NLP analysis on the user story using spaCy.  Currently just returns the doc."""
    doc = nlp(user_story)
    return doc


def generate_test_case_specifications(nlp_doc):
    """Generates test case specifications covering various testing aspects."""
    test_case_specs = []

    # Functional - Positive
    test_case_specs.append({
        "type": "Functional - Positive",
        "description": "Verify successful login with valid credentials.",
        "preconditions": "User account exists.",
        "steps": "Enter valid username and password. Click login button.",
        "expected_result": "User is logged in successfully."
    })

    # Functional - Negative
    test_case_specs.append({
        "type": "Functional - Negative",
        "description": "Verify login failure with invalid credentials.",
        "preconditions": "None.",
        "steps": "Enter invalid username and password. Click login button.",
        "expected_result": "Error message is displayed."
    })
    return test_case_specs


"""
    # Edge Case - Long Username
    test_case_specs.append({
        "type": "Edge Case",
        "description": "Verify login with a very long username.",
        "preconditions": "None.",
        "steps": "Enter a username exceeding maximum length. Enter valid password. Click login button.",
        "expected_result": "Appropriate error message is displayed or username is truncated."
    })

    # Edge Case - Special Characters in Username
    test_case_specs.append({
        "type": "Edge Case",
        "description": "Verify login with special characters in the username.",
        "preconditions": "None.",
        "steps": "Enter a username containing special characters. Enter valid password. Click login button.",
        "expected_result": "Login is successful or appropriate error message is displayed."
    })

    # Cross-Browser - Chrome
    test_case_specs.append({
        "type": "Cross-Browser - Chrome",
        "description": "Verify login functionality on Chrome browser.",
        "preconditions": "Chrome browser is installed.",
        "steps": "Open application in Chrome. Enter valid username and password. Click login button.",
        "expected_result": "User is logged in successfully in Chrome."
    })

    # Cross-Browser - Firefox
    test_case_specs.append({
        "type": "Cross-Browser - Firefox",
        "description": "Verify login functionality on Firefox browser.",
        "preconditions": "Firefox browser is installed.",
        "steps": "Open application in Firefox. Enter valid username and password. Click login button.",
        "expected_result": "User is logged in successfully in Firefox."
    })

    # Cross-Browser - Edge
    test_case_specs.append({
        "type": "Cross-Browser - Edge",
        "description": "Verify login functionality on Edge browser.",
        "preconditions": "Edge browser is installed.",
        "steps": "Open application in Edge. Enter valid username and password. Click login button.",
        "expected_result": "User is logged in successfully in Edge."
    })

    # Security - SQL Injection
    test_case_specs.append({
        "type": "Security - SQL Injection",
        "description": "Attempt SQL injection in username field.",
        "preconditions": "None.",
        "steps": "Enter SQL injection string in username field. Enter valid password. Click login.",
        "expected_result": "Application is not vulnerable to SQL injection. Error message or secure handling."
    })

    # Security - Brute Force
    test_case_specs.append({
        "type": "Security - Brute Force",
        "description": "Attempt to brute force the login.",
        "preconditions": "None.",
        "steps": "Simulate multiple login attempts with incorrect passwords.",
        "expected_result": "Account lockout mechanism or rate limiting is in place."
    })

    # Performance - Response Time
    test_case_specs.append({
        "type": "Performance - Response Time",
        "description": "Measure login response time.",
        "preconditions": "Stable network connection.",
        "steps": "Enter valid credentials and click login. Measure time taken for login to complete.",
        "expected_result": "Login response time is within acceptable limits (e.g., < 2 seconds)."
    })

    # Performance - Concurrent Users
    test_case_specs.append({
        "type": "Performance - Concurrent Users",
        "description": "Verify login performance with concurrent users.",
        "preconditions": "Test environment that supports concurrent users.",
        "steps": "Simulate multiple users logging in simultaneously.",
        "expected_result": "Application handles concurrent logins without significant performance degradation."
    })

    # Accessibility - WCAG 2.1 Perceivable - Text Alternatives
    test_case_specs.append({
        "type": "Accessibility - Perceivable",
        "description": "Verify that all non-text content has text alternatives.",
        "preconditions": "Login page is displayed.",
        "steps": "Check if all images and icons on the login page have appropriate alt text.",
        "expected_result": "All non-text content has text alternatives."
    })

     # Accessibility - WCAG 2.1 Operable - Keyboard Accessibility
    test_case_specs.append({
        "type": "Accessibility - Operable",
        "description": "Verify that all functionality is available from a keyboard.",
        "preconditions": "Login page is displayed.",
        "steps": "Navigate the login page using only the keyboard (Tab, Shift+Tab, Enter).",
        "expected_result": "All elements, including the login form and buttons, are accessible and operable via keyboard."
    })

    # Accessibility - WCAG 2.1 Understandable - Readable Text
    test_case_specs.append({
        "type": "Accessibility - Understandable",
        "description": "Verify that the login page text is readable.",
        "preconditions": "Login page is displayed.",
        "steps": "Check the contrast ratio between text and background.  Check font size and readability.",
        "expected_result": "Text is easily readable with sufficient contrast and appropriate font size."
    })

    # Accessibility - WCAG 2.1 Robust - Compatibility
    test_case_specs.append({
        "type": "Accessibility - Robust",
        "description": "Verify that the login page is compatible with assistive technologies.",
        "preconditions": "Login page is displayed.  Screen reader software is installed and running.",
        "steps": "Use a screen reader to navigate the login page.",
        "expected_result": "Screen reader can correctly interpret and announce all elements on the page, including labels, form fields, and buttons."
    })

"""


def generate_test_cases_from_specifications(test_case_specs):
    """Uses Gemini API to generate detailed test cases from specifications."""
    test_cases = []
    request_count = 0
    for i, spec in enumerate(test_case_specs):
        print(f"Generating test case for specification {i + 1}/{len(test_case_specs)}")  # Track progress
        prompt = f"""
        You are a QA engineer specializing in creating detailed test cases.  Based on the following test case specification, generate a comprehensive test case with the following sections:

        *   **Test Case ID:** (A unique ID, e.g., TC_LOGIN_001, TC_SECURITY_005, TC_ACCESSIBILITY_001)
        *   **Test Case Type:** {spec['type']}
        *   **Description:** {spec['description']}
        *   **Feature:** Login
        *   **Preconditions:** {spec['preconditions']}
        *   **Test Data:** (If applicable, specify test data, e.g., username, password, special characters)
        *   **Steps:** (Detailed, numbered steps for executing the test)
        *   **Expected Result:** (The expected outcome of each step)
        *   **Postconditions:** (What should be the state after the test case is executed)
        *   **Pass/Fail Criteria:**
        *   **Notes:** (Any additional information or considerations)

        Return only the test case in a well-formatted, readable format with clear sections. Do not include any extra conversation or intro/outro text.  Use markdown formatting for headings and tables where appropriate.
        """
        retries = 1
        for attempt in range(retries):
            try:
                # Rate limiting: Wait if we've made too many requests recently
                if request_count >= 1:  # Limit to 1 requests per minute.
                    print("Rate limit reached.  Sleeping for 60 seconds...")
                    time.sleep(60)  # Wait for 60 seconds
                    request_count = 0

                print(f"Attempt {attempt + 1}/{retries} to generate test case...")  # Track retries
                response = model.generate_content(prompt)
                test_cases.append(response.text.strip())
                request_count += 1
                time.sleep(1)  # Add a delay of 1 second between requests
                break  # Break out of retry loop if successful
            except Exception as e:  # Catch the base exception
                print(f"Error generating test case: {type(e).__name__} - {e}")  # Detailed error
                if "429 Resource has been exhausted" in str(e):
                    print(f"Quota exceeded. Retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)
                else:
                    print(f"Error generating test case: {e}")
                    return None
        else:
            print("Max retries reached. Failed to generate test case.")
            return None  # Return None if all retries fail

    return test_cases


def save_test_cases(test_cases, filename="generated_test_cases.txt"):
    """Saves the generated test cases to a file with improved formatting."""
    if not test_cases:
        print("No test cases generated. Exiting.")
        return

    with open(filename, "w", encoding="utf-8") as file:
        for i, test_case in enumerate(test_cases):
            file.write(f"## Test Case {i + 1}\n\n")  # Add a section header for each test case
            file.write(test_case)
            file.write("\n\n" + "-" * 80 + "\n\n")  # Add a separator between test cases

    print(f"Test cases saved to {filename}")


def generate_and_save_test_cases_from_story(file_path):
    """Generates and saves test cases from a user story."""
    user_story = read_user_story(file_path)

    if user_story:
        nlp_doc = analyze_user_story(user_story)
        test_case_specs = generate_test_case_specifications(nlp_doc)

        if test_case_specs:
            test_cases = generate_test_cases_from_specifications(test_case_specs)

            if test_cases:
                save_test_cases(test_cases, "test_cases_from_user_story.txt")
            else:
                print("Failed to generate test cases.")
        else:
            print("Failed to generate test case specifications.")
    else:
        print("Failed to read user story.")


if __name__ == "__main__":
    generate_and_save_test_cases_from_story(USER_STORY_PATH)
