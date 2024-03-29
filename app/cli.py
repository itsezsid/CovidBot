from __future__ import print_function, unicode_literals
from pyfiglet import Figlet
from PyInquirer import prompt, print_json
import functions
from colorama import Fore, Back, Style
from dotenv import load_dotenv
import subprocess
import os
import json
import sentry_sdk
from sentry_sdk import capture_exception
SENTRY = os.getenv("SENTRYURL")
sentry_sdk.init(
    SENTRY,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


path = os.getcwd()
tempath = os.getcwd().split('/')

# Checks if CLI is running in the correct directory
if tempath[-1] == 'CovidBot':
    app = (path + '/app')


# Clears terminal


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


# Makes the figlet
clear()
f = Figlet(font='slant', width=100)
print(Fore.MAGENTA + Style.BRIGHT +
      f.renderText('CovidBot CLI') + Style.RESET_ALL)


# Menu 1 [Intro]


def begin_prompt():
    questions = [

        {
            'type': 'confirm',
            'name': 'start',
            'message': 'Welcome to CovidBot CLI. This app is only for maintaining the app systems. The chatbot is powered by IBM Watson. Press Ctrl + C to quit anytime. Do you want to continue? :'

        }

    ]

    answers = prompt(questions)
    return answers


# Menu 2 [Main menu]


def choiceForExec():
    questions = [

        {
            'type': 'list',
            'name': 'choiceForExec',
            'message': 'What would you like to do? ',
            'choices': ["Install Dependencies", 'Run the GraphQL APP', 'Stop the GraphQL app', 'Update the Database',
                        'Create SQL Tables in a new Database', "Check API Call", "Get Stats"]

        }

    ]

    answers = prompt(questions)
    if answers["choiceForExec"] == "Install Dependencies":
        try:  # Option 1. Does pipenv install
            command = 'pipenv install'
            subprocess.getstatusoutput(command)
            print(Fore.GREEN + 'Dependencies installed successfully')
        except Exception as e:
            capture_exception(e)
            print(
                Fore.RED + 'Could not install dependencies. Install pipenv manually')
    elif answers["choiceForExec"] == 'Run the GraphQL APP':
        try:  # Runs gunicorn app
            execution = 'cd  {}  && gunicorn -w 3 -k uvicorn.workers.UvicornWorker graphql-app:app -b 0.0.0.0:8000 '.format(
                app)
            print(
                Fore.GREEN + "App is running successfully. Go to https://graphql.itsezsid.com or "
                             "0.0.0.0:8000 to access the GraphQL endpoint" + Style.RESET_ALL)
            subprocess.getstatusoutput(execution)

        except KeyboardInterrupt:
            try:  # Stops gunicorn using pkill [Kills Process]
                execution = 'cd {} && pkill gunicorn'.format(app)
                subprocess.getstatusoutput(execution)
                print(Fore.GREEN + "Gunicorn Stopped Successfully" + Style.RESET_ALL)

            except Exception as e:  # Except block
                capture_exception(e)
                print(
                    Fore.RED + "Unable To stop Gunicorn Directly.\n" + Fore.GREEN + "Please enter the app directory and run 'pkill gunicorn'" +
                    + Style.RESET_ALL)

        except:  # Except block if cli cant run gunicorn
            print(Fore.RED + "Unable To Run Gunicorn Directly.\n" + Fore.GREEN + "Please enter the app directory "
                                                                                 "and run 'gunicorn -w 3 -k "
                                                                                 "uvicorn.workers.UvicornWorker "
                                                                                 "graphql-app:app -b "
                                                                                 "0.0.0.0:8000'" +
                  + Style.RESET_ALL)

    elif answers["choiceForExec"] == 'Stop the GraphQL app':
        try:  # Stops gunicorn using pkill [Kills Process]
            execution = 'cd {} && pkill gunicorn'.format(app)
            subprocess.getstatusoutput(execution)
            print(Fore.GREEN + "Gunicorn Stopped Successfully" + Style.RESET_ALL)

        except Exception as e:  # Except block
            capture_exception(e)
            print(
                Fore.RED + "Unable To stop Gunicorn Directly.\n" + Fore.GREEN + "Please enter the app directory and run 'pkill gunicorn'" +
                + Style.RESET_ALL)
    elif answers["choiceForExec"] == 'Update the Database':
        try:  # Runs the update function
            functions.updateDb()
            print(Fore.GREEN + "Database Updated Successfully" + Style.RESET_ALL)
        except Exception as e:
            capture_exception(e)
            print(Fore.RED + "Database couldnt be updated . Check .env file")
    elif answers["choiceForExec"] == 'Create SQL Tables in a new Database':
        try:  # Runs the update function
            functions.insertDb()
            print(Fore.GREEN + "Database Updated Successfully" + Style.RESET_ALL)
        except Exception as e:
            capture_exception(e)
            print(Fore.RED + "Database couldnt be updated . Check .env file")
    elif answers["choiceForExec"] == 'Check API Call':
        try:  # Makes the API call for testing
            data = functions.apiCall()
            print(json.dumps(data, indent=2))
            print(Fore.GREEN + "Command ran successfully")
        except Exception as e:
            capture_exception(e)
            print(Fore.RED + "Command Failed" + Style.RESET_ALL)
    elif answers["choiceForExec"] == 'Get Stats':
        try:  # Runs the stats_promp() function to
            stats_prompt()
        except Exception as e:
            capture_exception(e)
            print(Fore.RED + 'Could not get stats' + Style.RESET_ALL)


# Menu to take country name


def countryStatsInput():
    questions = [

        {
            'type': 'input',
            'name': 'country',
            'message': 'Please enter the country name [Countries like United States of America have the indentifier as united-states] : ',

        }

    ]

    answers = prompt(questions)
    return answers


# Menu for stats


def stats_prompt():
    questions = [

        {
            'type': 'list',
            'name': 'Statistics',
            'message': 'Do you want world stats or country stats?',
            'choices': ['World Statistics', 'Country Statistics'],

        }

    ]

    answers = prompt(questions)
    if answers["Statistics"] == "World Statistics":

        data = functions.getStats()

        print(json.dumps(data, indent=2))
        # print(data)

    else:
        slug = countryStatsInput()
        data = functions.getCountryStats(slug["country"])
        print(json.dumps(data, indent=2))


# Driver code


def main():
    choice = begin_prompt()
    if choice['start'] == True:
        choiceForExec()

    else:
        print(Fore.YELLOW + "Designed by Siddharth and Varun" + Style.RESET_ALL)


if tempath[-1] == 'CovidBot':
    try:
        main()
    except:
        if KeyboardInterrupt:
            print(Fore.YELLOW + "Designed by Siddharth and Varun" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Error" + Style.RESET_ALL)
else:
    print(Fore.RED + "Please run the CLI in the CovidBot directory." + Style.RESET_ALL)
