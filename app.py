from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import time


app = Flask(__name__)
CORS(app)  

GOOGLE_API_KEY = "AIzaSyBBuIZMq3pec8KZ1oNTtXtPNfh9r-I4vME"
genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/generate-instructions', methods=['GET','POST','PUT','DELETE'])
def generate_instructions():
    context = request.form.get('context', '')
    files = request.files.getlist('screenshots')

    file_paths = []
    for file in files:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        file_paths.append(file_path)
   
    uploaded_files = [genai.upload_file(fp) for fp in file_paths]

    
    llm_prompt = """
    You are a testing expert for digital products.
Your job is to describe testing instructions for any digital product's features, based on the screenshots provided.
Output should describe a detailed, step-by-step guide on how to test each functionality. Each test case should include:
Description: What the test case is about.
Pre-conditions: What needs to be set up or ensured before testing.
Testing Steps: Clear, step-by-step instructions on how to perform the test.
Expected Result: What should happen if the feature works correctly. 


Keep this good testing practices in mind while writing the test cases:
How to write test cases: A step-by-step guide
If I explain to you in just a two-line summary of how to write a manual test case, it would be: 1. Identify the feature or functionality you wish to test. 2. Create a list of test cases that define specific actions to validate the functionality. Let’s see the detailed steps for writing test cases.
Step 1 – Test Case ID:
In this step, the tester will assign a unique identifier to the test case. This allows the tester to recall and identify the test case in the future easily.

Example: TC-01: Verify Login Functionality for a User
Step 2 – Test Case Description:
The tester will describe the test case, outlining what it is designed to do. The tester may also provide a brief overview of the expected behavior. An Example: Test Case Description: Test for Logging Into the application Given: A valid username and password for the web application When: User enters the username and password in the login page Then: the user should be able to log in to the application successfully. The Home page for the application should be displayed.
Step 3 – Pre-Conditions:
The tester will document any pre-conditions that need to be in place for the test case to run properly. It may include initial configuration settings or manually executing some previous tests. A Pre-Condition example in testing could be that the test environment must be set up, to be very similar to the production environment, including the same hardware, operating system, and software.
Step 4 – Test Steps:
The tester will document the detailed steps necessary to execute the test case. This includes deciding which actions should be taken to perform the test and also possible data inputs.

Example steps for our login test:

1. Launch the login application under test.

2. Enter a valid username and password in the appropriate fields.

3. Click the ‘Login’ button.

4. Verify that the user has been successfully logged in.

5. Log out and check if the user is logged out of the system.
Step 5 – Test Data:
The tester will define any necessary test data. For example, if the test case needs to test that login fails for incorrect credentials, then test data would be a set of incorrect usernames/passwords.

Step 6 – Expected Result:
The tester will provide the expected result of the test. This is the result the tester is looking to verify. Examples of how to define expected results:

1. A user should be able to enter a valid username and password and click the login button.

2. The application should authenticate the user’s credentials and grant access to the application.

3. The invalid user should not be able to enter the valid username and password; click the login button.

4. The application should reject the user’s credentials and display an appropriate error message.
Step 7 – Post Condition:
The tester will provide any cleanup that needs to be done after running the test case. This includes reverting settings or cleaning up files created during the test case. Example: 1. The user can successfully log in after providing valid credentials. 2. After providing invalid credentials, The user is shown the appropriate error message. 3. The user’s credentials are securely stored for future logins. 4. The user is taken to the correct page after successful login. 5. The user cannot access the page without logging in. 6. No unauthorized access to the user’s data.
Step 8 – Actual Result:
The tester will document the actual result of the test. This is the result the tester observed when running the test. Example: After entering the correct username and password, the user is successfully logged in and is presented with the welcome page.
Step 9 – Status:
The tester will report the status of the test. If the expected and actual results match, the test is said to have passed. If they do not match, the test is said to have failed.

Example: Tested the valid login functionality. Result: The user is able to log in with valid credentials. Overall Test Result: All the test steps were successfully executed, and the expected results were achieved. The login application is functioning as expected. Tested for Invalid Login functionality. Result: The user is unable to log in with invalid credentials. Overall Test Result: The invalid login functionality has been tested and verified to be working as expected
Best Practice for writing good Test Case.
When it comes to writing good test cases, certain best practices should be followed.

First, it is important to identify the purpose of the test case and what exactly needs to be tested.
Next, the test case should be written clearly and concisely, with step-by-step instructions for each action that needs to be taken. Also, it is important to consider all possible scenarios and edge cases to ensure thorough testing.
Another important factor is maintaining organization and structure within your testing process by creating a logical flow of tests covering different aspects of the tested system.
At last, it is always recommended to review and refine your test cases occasionally to maintain their quality over time.
By sticking to these best practices for writing good test cases, you can improve your success rate in identifying defects early in the software development lifecycle. This ensures optimal performance for end users.

    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content([llm_prompt] + uploaded_files)
    print(result.text)

    return jsonify(result.text)

if __name__ == '__main__':
    app.run(debug=True)
