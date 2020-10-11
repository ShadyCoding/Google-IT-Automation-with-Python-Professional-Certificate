#!/usr/bin/env python3
import os
import json
import locale
import requests
import datetime
# Importing modules from custom python files
from reports import generate_report as report
from report_email import generate as email_generate
from report_email import send as email_send


def catalog_data():
    """This function will return a list of dictionaries with all the details like name, weight, description, image_name.
    It will change the weight to integer format.
    """
    catalog = []
    # Going through each filename in the directory
    for description_name in description_files:
        # Accepting files that has txt extension and ignoring hidden files
        if not description_name.startswith('.') and 'txt' in description_name:
            # creating absolute path for each image
            description_path = description_directory + description_name
            # creating image name from text files and changing the extension to jpeg
            image_path = description_name.strip('.txt') + '.jpeg'
            # Opening each file
            with open(description_path) as content:
                # parsing content and storing it in a list
                data = content.readlines()
                # extracting the first line and removing the newline
                name = data[0].strip('\n')
                # extracting the second line and removing the newline and lbs. Also changing it to integer
                weight = int(data[1].strip('\n').strip(' lbs'))
                # extracting the third line and removing the newline
                description = data[2].strip('\n')
                # creating a dictionary object with required format
                catalog_object = {"name": "{}".format(name), "weight": weight,
                                  "description": "{}".format(description.replace(u'\xa0', u'')),
                                  "image_name": "{}".format(image_path)}
                # converting dictionary to json
                dict_to_json = json.dumps(catalog_object)
                # Creating headers to push the data to fruits url
                header = {'Content-Type': 'application/json'}
                # pushing data to fruits url
                req = requests.post(url, headers=header, data=dict_to_json)
                # If the error code is not 2xx, raise exception
                print(req.reason)
                # creating a list from the above dictionary
                catalog.append(catalog_object)
                # removing all the none values from the list of dictionaries
                catalog = list(filter(None, catalog))
    return catalog


def summary(input_for):
    """Generating a summary with two lists, which gives the output name and weight"""
    # List of all the names of fruits in catalog list of dictionaries
    res = ['name: ' + sub['name'] for sub in catalog_data()]
    # List of all the weight of fruits in catalog list of dictionaries
    we = ['weight: ' + str(sub['weight']) + ' lbs' for sub in catalog_data()]
    # initializing the object
    new_obj = ""
    # Calling values from two lists one by one.
    for name, weight in zip(res, we):
        if name and input_for == 'pdf':
            new_obj += name + '<br />' + weight + '<br />' + '<br />'
        # If we want to display the same list in mail.
        # elif input_for == 'email':
        # new_obj += name + '\n' + weight + '\n' + '\n'
    return new_obj


if __name__ == "__main__":
    # To get the username from environment variable
    USER = os.getenv('USER')
    # To set encoding to avoid ascii errors
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    # The directory which contains all the files with data in it.
    description_directory = '/home/{}/supplier-data/descriptions/'.format(USER)
    # Listing all the files in description directory
    description_files = os.listdir(description_directory)
    # The directory which contains all the images.
    image_directory = '/home/{}/supplier-data/images/'.format(USER)
    # URL to push the data to the website
    url = "http://localhost/fruits/"
    # Creating data in format "May 5, 2020"
    current_date = datetime.date.today().strftime("%B %d, %Y")
    # Title for the PDF file with the created date
    title = 'Processed Update on ' + str(current_date)
    # subject line give in assignment for email
    new_subject = 'Upload Completed - Online Fruit Store'
    # body line give in assignment for email
    new_body = 'All fruits are uploaded to our website successfully. A detailed list is attached to this email.'
    # calling the report function from custom module
    report('/tmp/processed.pdf', title, summary('pdf'))
    # structuring email and attaching the file. Then sending the email, using the custom module.
    email = email_generate("automation@example.com", "{}@example.com".format(USER),
                         new_subject, new_body, "/tmp/processed.pdf")
    email_send(email)
