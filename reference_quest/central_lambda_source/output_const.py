# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.

# WELCOME
WELCOME_KEY="welcome"
WELCOME_LABEL="Welcome to the (soon to be) NEW Unicorn.Rentals"
WELCOME_VALUE="""
At Unicorn.Rentals, we hire dreamers not just "techs”. We seek those who share our vision and are willing to put in extra hours to take our offering of mythical creatures to the next level. Our solutions are diverse and the things wer are building are going to delight our users. 

But first... Unicorn.Rentals needs to deliver it's next generation, cloud hosted, marketing website! As the core team responsibile for the deployment and migration, you'll ship the features that power Unicorn.Rentals new marketing website, and debug any problems that come up when the Unicorns break loose. You'll divide tasks up between your team focused on building new feature flags, creating rollout strategies, and delivering the new website... hopefully with no broken horns! 
"""
WELCOME_INDEX=1
WELCOME_MARKDOWN=True


# TASK 1 - App Runner Deployment
TASK1_KEY="task1"
TASK1_LABEL="Unicorns in the Clouds! Deploying the new Unicorn.Rentals!"
TASK1_VALUE="""
The pipelines have ran and its time to deploy our new Unicorn.Rentals into AWS! Roll up your sleeves, crack your knuckles, and get the application UP. As the Cloud Administrator at Unicorn.Rentals, you'll need to deploy the image for the website to AWS App Runner. You'll need to ensure that you import the **LaunchDarkly Server SDK** key as an **environment variable (`LD_SDK_KEY`)** as well as your **Team ID (`TEAM_ID`)**. Ensure you're using the correct **App Runner Instance Role** during the deployment to allow connectivity to the rest of the Unicorn.Rentals cloud environments.

When your deployment is complete and running successfully, enter the full URL (including https://) below and the system will validate if the application is up! 

**Note: From the time your submit your first check, you're on the clock! You'll lose points each time you submit an incorrect answer, and points every minute the correct URL isn't entered.**
"""
TASK1_INDEX=10
TASK1_MARKDOWN=True

TASK1_APPRUNNER_WRONG_KEY="task1_bad_url"
TASK1_APPRUNNER_WRONG_LABEL="Well - there's nothing here"
TASK1_APPRUNNER_WRONG_VALUE="""
Uh oh! The URL you entered isn't returning any data! Its possible the URL is wrong or App Runner isn't up yet. Sorry about the points loss! Head over to **App Runner** in your AWS account and give it another try.
""" 
TASK1_APPRUNNER_WRONG_INDEX=14
TASK1_APPRUNNER_WRONG_MARKDOWN=True

TASK1_APPRUNNER_CORRECT_KEY="task1_url_up"
TASK1_APPRUNNER_CORRECT_LABEL="We've got ignition!"
TASK1_APPRUNNER_CORRECT_VALUE="The URL checks out! Our new website has been deployed into App Runner **successfully**!"
TASK1_APPRUNNER_CORRECT_INDEX=15
TASK1_APPRUNNER_CORRECT_MARKDOWN=True

TASK1_APPRUNNER_INPUT_REMOVED_KEY='task1_input_remove'
TASK1_APPRUNNER_INPUT_REMOVED_LABEL="Input evaluating..."
TASK1_APPRUNNER_INPUT_REMOVED_VALUE="Our Unicorns are currently checking the status of this answer... standby"
TASK1_APPRUNNER_INPUT_REMOVED_INDEX=16
TASK1_APPRUNNER_INPUT_REMOVED_MARKDOWN=True


TASK1_APPRUNNER_DOWN_KEY="task1_webapp_down"
TASK1_APPRUNNER_DOWN_LABEL="Something’s wrong!"
TASK1_APPRUNNER_DOWN_VALUE="""
App Runner may be up, but the webapp is still down and not reporting a healthy code. Time to debug! 
"""
TASK1_APPRUNNER_DOWN_INDEX=17
TASK1_APPRUNNER_DOWN_MARKDOWN=True

TASK1_COMPLETE_KEY="task1_complete"
TASK1_COMPLETE_LABEL="All systems are green!"
TASK1_COMPLETE_VALUE="""
The Unicorn.Rentals site on AWS App Runner is returning a 200 OK status code, indicating its up and running and ready to start releasing features in LaunchDarkly! You successfully launched our application into the cloud!
"""
TASK1_COMPLETE_INDEX=19
TASK1_COMPLETE_MARKDOWN=True


# TASK 2 - Releasing
TASK2_KEY="task2"
TASK2_LABEL="Releasing the new Unicorn.Rentals!"
TASK2_VALUE="""
The pipelines have ran and the new Unicorn.Rentals code is deployed, but running stealth mode, gated behind feature flags to limit the users who can see the new changes. To get the new site launched, we'll need you to use LaunchDarkly to manage these feature flags. Navigate into your LaunchDarkly account, create the feature, and enable targeting for your users. Once rolled out, enter the version code from the bottom right of the application below to validate the page has launched! As a reminder, please work in the AWS region.
"""
TASK2_INDEX=20
TASK2_MARKDOWN=True

TASK2_UNRELEASED_KEY="task2_app_unreleased"
TASK2_UNRELEASED_LABEL="Still unreleased!"
TASK2_UNRELEASED_INDEX=21
TASK2_UNRELEASED_VALUE="The preview version of the page is still running..."
TASK2_UNRELEASED_VALUE=True

TASK2_COMPLETE_KEY="task2_complete"
TASK2_COMPLETE_LABEL="The new Unicorn.Rentals has been released!"
TASK2_COMPLETE_VALUE="""
Amazing! You were able to launch the new website using LaunchDarkly! 
"""
TASK2_COMPLETE_INDEX=29
TASK2_COMPLETE_MARKDOWN=True


# TASK 3 - Access Key
TASK3_KEY="task3"
TASK3_LABEL="Gone, but still here"
TASK3_VALUE="""
Our security team (one person in the basement) has discovered that one of our previous employees is still using old credentials to poke around inside our account. This is a serious matter. Every minute that passes increases the risk for malicious activity. You will lose points until this is resolved.
"""
TASK3_INDEX=30
TASK3_MARKDOWN=True


TASK3_STARTED_KEY="task3_started"
TASK3_STARTED_LABEL="Your move now!"
TASK3_STARTED_VALUE="""
As we anticipated, the previous employee has already started doing some damage in the account. Please locate the user 
“ReferenceDeveloper” and rotate its access keys. The longer it will take you, the more points you will lose, but no pressure.
"""
TASK3_STARTED_INDEX=35
TASK3_STARTED_MARKDOWN=True


TASK3_COMPLETE_KEY="task3_complete"
TASK3_COMPLETE_LABEL="Compromised access key: Passed!"
TASK3_COMPLETE_VALUE="""
All done. Great job neutralizing the compromised access key.
"""
TASK3_COMPLETE_INDEX=39
TASK3_COMPLETE_MARKDOWN=True


# TASK 4 - Final question
TASK4_KEY="task4"
TASK4_LABEL="One last thing and we are done here"
TASK4_VALUE="""
Our CEO has a final question for you. It's a bit cryptic I must say, so I wanted to ask for clarifications, 
but they said they were late for the golf game.
"""
TASK4_INDEX=40
TASK4_MARKDOWN=True


TASK4_WRONG_KEY="task4_wrong_answer"
TASK4_WRONG_LABEL="You don't know THE answer, do you?"
TASK4_WRONG_VALUE="Our CEO will be very disappointed"
TASK4_WRONG_INDEX=42
TASK4_WRONG_MARKDOWN=True


TASK4_CORRECT_KEY="task4_correct_answer"
TASK4_CORRECT_LABEL="What is “THE” answer to life, the universe, everything?"
TASK4_CORRECT_VALUE="That's right! 42 is THE answer."
TASK4_CORRECT_INDEX=43
TASK4_CORRECT_MARKDOWN=True


# QUEST COMPLETE
QUEST_COMPLETE_KEY='quest_complete'
QUEST_COMPLETE_LABEL='Wonderful job!'
QUEST_COMPLETE_VALUE='You\'ve completed this quest.'
QUEST_COMPLETE_INDEX=100
QUEST_COMPLETE_MARKDOWN=True
