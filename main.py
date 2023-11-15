'''from IPython.display import display, HTML, clear_output, Javascript
import ipywidgets as widgets
pip
import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import base64'''

print("Enter your email id: ")
senderEmail = input()
print("Enter your email id secret password(2-Factor encryption should be enabled from where secret pwd is generated): ")
password = input()
print("Enter recipients as a comma-separated list: ")
recipients = eval(input())
print("Enter open-ai secret key: ")
openai_api_key = input()
print("Enter your imgur api client id: ")
imgur_client_id = input()

import pyimgur

import time
import openai

from jinja2 import Template
from tensorflow import keras

import os
current_directory = os.path.dirname(os.path.abspath(__file__))
model_file_path = os.path.join(current_directory, 'models', 'blurdetectmodel.h5')
model = keras.models.load_model(model_file_path)

import requests
import cv2
import numpy as np

# Set up your OpenAI API key
openai.api_key = openai_api_key

def generate_email_template_subject(subject):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": 'Draft an appropriate poster title based on the prompt. Use only Uppercase. It must be between 3-6 words.'},
                {"role": "user", "content": f"{subject}"}  # First message for subject
            ]
        )
        generated_subject = response.choices[0]['message']['content']
        return generated_subject
    except Exception as e:
        print(f"Error generating subject: {e}")
        print("Retrying in 20 seconds...")
        time.sleep(20)
        return generate_email_template_subject(subject)
def generate_email_template_call_to_action(call_to_action):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": 'You are an email Generating assistant. Add newline characters to make it presentable. Draft an appropriate company marketing email of 50 words.'},
                {"role": "user", "content": f"\n\n{call_to_action}"}
            ]
        )
        generated_call_to_action = response.choices[0]['message']['content']

        return generated_call_to_action
    except Exception as e:
        print(f"Error generating call to action: {e}")
        print("Retrying in 20 seconds...")
        time.sleep(20)
        generate_email_template_call_to_action(call_to_action)

def generate_image_prompt(user_input):
    try:
        conversation_history=[]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system",
                 "content": 'You are an image prompt generating assistant. Generate a text prompt that describes a non-blurry image featuring vibrant colors, dynamic composition, and conveys a sense of the users input. Limit it to 35 words at most.'},
                *conversation_history,
                {"role": "user", "content": user_input}
            ],
            max_tokens=50
        )
        generated_image_prompt = response.choices[0]['message']['content']
        return generated_image_prompt

    except Exception as e:
        print(f"Error generating image prompt: {e}")
        print("Retrying in 20 seconds...")
        time.sleep(20)
        return generate_image_prompt(user_input)

def generate_image(image_prompt):
    try:
      response = openai.Image.create(
        #prompt="In 4k nikon resolution, Create an image with lush, vibrant nature framing the edges",
        #prompt="The image is set in a lush and vibrant forest during a golden hour. The composition is dynamic, with the viewer positioned at the edge of a winding",
        prompt = image_prompt,
        n=1,
        size="1024x1024"
      )
      image_url = response['data'][0]['url']
      #print(image_url)
      generated_image = image_url
      return generated_image

    except Exception as e:
        print(f"Error generating image: {e}")
        print("Retrying in 20 seconds...")
        time.sleep(20)
        return generate_image(image_prompt)

def process_image(resized_image, model):
    # Expand dimensions and scale pixel values
    resized_image = np.expand_dims(resized_image / 255, 0)

    # Predict using the model
    prediction = model.predict(resized_image)
    return prediction

'''def generate_logo():
    response = openai.Image.create(
        prompt="A single Beautiful Geometric Design logo in the style of Gmail or LinkedIn etc, pastel background",
        n=1,
        size="1024x1024"
    )
    logo_url = response['data'][0]['url']
    return logo_url'''

#subject = "Environment Day sale"
#call_to_action = "Claim your discount now. Limited time offer."
print("User prompt input: ")
user_input = input()

# Generate subject title and short email body
subject_title = generate_email_template_subject(user_input)
print("Subject successfully generated")
call_to_action_text = generate_email_template_call_to_action(user_input)
print("Call to Action successfully generated")

# Initialize an empty list to store the prompts
image_prompt_list = []

# Generate and store the prompts
for _ in range(3):
    image_prompt = generate_image_prompt(user_input)
    image_prompt_list.append(image_prompt)
    print("Image prompt successfully generated")

    if _ == 0:
        time.sleep(60)  # Sleep for 60 seconds (1 minute)
    else:
        time.sleep(5)

# Print the list of prompts
print(image_prompt_list)

time.sleep(120)

generated_image_list = []  # Assuming you have a list to store the generated images

for prompt in image_prompt_list:
    generated_image = generate_image(prompt)
    generated_image_list.append(generated_image)
    print("Image successfully generated")
    time.sleep(60)

print(generated_image_list)

results_list = []
i=0

for generated_image in generated_image_list:
    response = requests.get(generated_image)
    image_data = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Save the image with different names based on the index
    if i == 0:
        cv2.imwrite('generated_image_0.jpg', image)
    elif i == 1:
        cv2.imwrite('generated_image_1.jpg', image)
    elif i == 2:
        cv2.imwrite('generated_image_2.jpg', image)

    # Perform resizing using OpenCV
    resized_image = cv2.resize(image, (256, 256))

    result = process_image(resized_image, model)
    results_list.append(result)
    i=i+1

# Print the list of results
print(results_list)

# Find the index of the maximum value in results_list (index of highest rated prediction in the image list )
max_index = np.argmax(results_list)

# Use the index to get the corresponding element from generated_image_list
selected_image = generated_image_list[max_index]

print(f"The image with the highest prediction is: {selected_image}")

if max_index == 0:
    imgurpath = 'generated_image_0.jpg'
elif max_index == 1:
    imgurpath = 'generated_image_1.jpg'
elif max_index == 2:
    imgurpath = 'generated_image_2.jpg'

print("Max Index:",max_index)

im = pyimgur.Imgur(imgur_client_id)

uploaded_image = im.upload_image(imgurpath, title="name_any")

generated_image_link = uploaded_image.link

print('uploaded link:', generated_image_link)

final_email = f'''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>

a.button {{
    display: inline-block;
    padding: 2px 2px;
    text-decoration: none;
    background-color: white;
    color: #fff;
    border-radius: 50%;
  }}

  a.button:hover {{
    background-color: rgb(229, 220, 220);
  }}

</style>
</head>
<body>
    <p>&nbsp;</p>
    <table style="width: 1024px; height: 1024px;" role="presentation" border="0" width="640" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr>
    <td style="background: url('{generated_image_link}') center center / cover no-repeat #000000; width: 636px;" align="center" valign="top" bgcolor="#000000" height="400"><!-- [if gte mso 9]>
    <v:image xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style=" border: 0;display: inline-block; width: 480pt; height: 300pt;" src="https://via.placeholder.com/640x400" />                <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style=" border: 0;display: inline-block;position: absolute; width: 480pt; height:300pt;">
    <v:fill  opacity="0%" color="#000000”  />
    <v:textbox inset="0,0,0,0">
    <![endif]-->
    <div>
    <table style="width: 691px; height: 971px;" role="presentation" border="0" width="640" cellspacing="0" cellpadding="0" align="center">
    <tbody>
    <tr style="height: 34px;">
    <td style="width: 687px; height: 10px;" align="center" height="400">&nbsp;</td>
    </tr>
    <tr style="height: 18px;">
    <td style="width: 687px; height: 961px;">
    <div style="height: 500px; background-color: white; border-radius: 10px; text-align: center; margin: 20px; color: black;"><img style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%; border: 2px solid grey; float: right; margin: 10px;" src="https://i.imgur.com/kBvT72z.png" alt="Generated Logo" />
    <p>&nbsp;</p>
    <div style="text-align: center;">
    <h1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{subject_title}</h1>
    </div>
    <div style="height: 10px;">
    </div>
    <div style="margin: 70px 70px 50px 70px;"><em>{call_to_action_text}</em></div>
    <div>&nbsp;</div>
    <div style="text-align: center; font-size: 10px; width: 100%;">
      <div style="height: 35px;">
     </div>
     <div>
        <a href="https://twitter.com" class="button">
            <img src="https://imgur.com/SaOxUV8.png" alt="Twitter" width="43" height="43">
        </a>
        <a href="https://facebook.com" class="button">
            <img src="https://imgur.com/3sc11WX.png" alt="Facebook" width="43" height="43">
        </a>
        <a href="https://linkedin.com" class="button">
            <img src="https://imgur.com/CWW6k7f.png" alt="Linkedin" width="43" height="43">
        </a>
        <a href="https://instagram.com" class="button">
            <img src="https://imgur.com/5CBpfwc.png" alt="Instagram" width="43" height="43">
        </a>

     </div>
    <p>&copy; Copyright Your Brand Name 2023.</p>
    <p>All rights reserved.</p>
    </div>
    </div>
    </td>
    </tr>
    </tbody>
    </table>
    </div>
    <!-- [if gte mso 9]>
    </v:textbox>
    </v:fill>
    </v:rect>
    </v:image>
    <![endif]--></td>
    </tr>
    </tbody>
    </table>
<!-- [if gte mso 9]>
</v:textbox>
</v:fill>
</v:rect>
</v:image>
<![endif]--></td>
</tr>
</tbody>
</table>
</body>
</html>
'''

#display(HTML(final_email))
with open('generated_email3.html', 'w') as f:
  f.write(final_email)

with open('generated_email3.html', 'r') as f:
    final_email_template = f.read()

# Replace the placeholders with actual values
template = Template(final_email)

rendered_email = template.render(
    generated_image_link = generated_image_link,
    subject_title = subject_title,
    call_to_action_text = call_to_action_text
)

'''
import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText
'''


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(message, recipients):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "TRIAL MAIL"
    msg['From'] = senderEmail
    msg['Bcc'] = ", ".join(recipients)  # Comma-separated list of BCC recipients

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(senderEmail, password)

    print("Connected To Server")

    server.sendmail(senderEmail, recipients, msg.as_string())

    print("Email sent")

    server.quit()

sendEmail(rendered_email, recipients)
print("\n")