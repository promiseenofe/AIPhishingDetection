import os
import email
from email import policy
from email.parser import BytesParser
import openai

#function to read plain text files
def read_text_file(filepath):
    with open (filepath, 'r') as file:
        return file.read()


def extract_email(file_path):
    with open(file_path, 'rb') as file:
        #parse email content
        message = BytesParser(policy = policy.default).parse(file)
    
    # Extract essential fields
    email_subject = message['subject']
    sender = message['from']
    email_body = message.get_body(preferencelist = ('plain')).get_content()
    
    return email_subject, sender, email_body

#Set up OpenAI using your own paid api key!
openai.api_key = "insert the api key here"

def phishing_detect(email_content):
    prompt = f"""
    You are a cybersecurity expert. Analyze the following email for signs of phishing.
    Look for: suspicious links, threatening language, urgent requests for personal information. or any general indicators of phishing.
    
    Email content:
    {email_content}
    
    Do the following:
    1. Generate a likelihood score from 0 to 100 for whether this email is a phishing attempt or not.
    2. Generate an explaination of the indicators that contribute to this score.
    3. Generate the next form of action the recipient should take with reference to the generated score and explaination of indicators.
    """
    
    #Calling OpenAI with the prompt reference your prefer gpt model
    result = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": prompt}]
    )
    
    #return the phishing detection analysis
    return result.choices[0].message['content']

def generate_report(filepath):
    
    if file_path.endswith('.eml'):
        #Parse email content of a eml file
        email_subject, sender, email_body = extract_email(filepath)
        email_content = f"Subject: {email_subject} From: from_address {email_body}"
    else:
        #read plain text files
        email_content = read_text_file(filepath)
    
    #Analyze the extracted email content
    analysis = phishing_detect(email_content)
    
    print("\n===== Phishing Analysis Report =====")
    print(analysis)
    
#Function to run the script
if __name__ == "__main__":
    #This will be where the program will prompt the user to enter the path of the suspected file
    file_path = input("Enter the path to the email file or text file: ")
    if os.path.exists(file_path):
        #if the path exists it will generate the analysis and the report
       print("File successfully located! Please review report below:")
       generate_report(file_path)
    else:
        #If the path cannot be found then the user will see an error prompt and be asked to try again
      print("Hold on ! Error ! File not found. Please check the path & try again.")