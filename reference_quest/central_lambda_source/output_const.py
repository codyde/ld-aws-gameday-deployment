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
TASK1_LABEL="Task 1 - Unicorns in the Clouds! Deploying the new Unicorn.Rentals!"
TASK1_VALUE="""
The pipelines have ran and its time to deploy our new Unicorn.Rentals into AWS! Roll up your sleeves, crack your knuckles, and get the application UP. 

As the Cloud Administrator at Unicorn.Rentals, you'll need to deploy the image for the website to AWS App Runner. As part of this exercise, ensure the following configurations are applied: 

* Search for `Unicorn` in the image list, and use this as your image
* Set the port for the App Runner application to `5000`
* Create an environment variable during your App Runner deployment for your **LaunchDarkly Server SDK**. Use a key named `LD_SERVER_KEY` with the value from the credentails above or from within the LaunchDarkly console. The client side SDK is not needed for this step. 
* Create an additional environment variable for your **Team ID** with a key named `TEAM_ID` and a value of 1 (TODO: Replace this with language for "the team ID")
* On the security tab, ensure you have selected the **instance role** titled **LD-AppRunner-Policy** to allow connectivity to the necessary Unicorn.Rentals cloud resources 

When your deployment is complete and running successfully, enter the full URL (including https://) below and the system will validate if the application is up! 

**Note: Incorrect submissions will cost you! Ensure the website is fully up before you submit, or you'll lose reputation along with score!**
"""
TASK1_INDEX=10
TASK1_MARKDOWN=True

# TASK 1 - For outputting LD credentials
TASK1_CREDS_KEY="task1_creds"
TASK1_CREDS_VALUE=f"""
### Use the following credentials: 
"""
TASK1_CREDS_INDEX=10
TASK1_CREDS_MARKDOWN=True

TASK1_APPRUNNER_WRONG_KEY="task1_bad_url"
TASK1_APPRUNNER_WRONG_LABEL="Well - there's nothing here"
TASK1_APPRUNNER_WRONG_VALUE="""
Uh oh! The URL you entered isn't returning any data! Its possible the URL is wrong or App Runner isn't up yet. Sorry about the points loss! Head over to **App Runner** in your AWS account and give it another try.
""" 
TASK1_APPRUNNER_WRONG_INDEX=11
TASK1_APPRUNNER_WRONG_MARKDOWN=True

TASK1_APPRUNNER_INPUT_REMOVED_KEY='task1_input_remove'
TASK1_APPRUNNER_INPUT_REMOVED_LABEL="Input evaluating..."
TASK1_APPRUNNER_INPUT_REMOVED_VALUE="Our Unicorns are currently checking the status of this answer... standby"
TASK1_APPRUNNER_INPUT_REMOVED_INDEX=16
TASK1_APPRUNNER_INPUT_REMOVED_MARKDOWN=True


TASK1_COMPLETE_KEY="task1_complete"
TASK1_COMPLETE_LABEL="Unicorn.Rentals is up and running!"
TASK1_COMPLETE_VALUE="""
Unicorn.Rentals has been launched successfully. You created an App Runner deployment of the new marketing website, and validated that it's up and returning a **200 OK** code, indicating its functional. You are one step closer to having the site live and serving user traffic! Now, it's time to start creating our feature flags and launching the **NEW** Unicorn.Rentals!
"""
TASK1_COMPLETE_INDEX=13
TASK1_COMPLETE_MARKDOWN=True


# TASK 2 - Releasing
TASK2_KEY="task2"
TASK2_LABEL="Task 2 - Releasing the new Unicorn.Rentals!"
TASK2_VALUE="""
You just received a notification from the web development team that the new version of the Unicorn.Rentals website is ready for user testing! They have pushed their changed to the site already, but also included a **[feature flag value](https://github.com/codyde/ld-aws-gameday/blob/a61d1857bc5e7042de095d6f896facc7f048931b/pages/index.js#L54)** that is preventing it from being seen by most users. as the engineer helping roll out the new site and release the changes, it's now up to you to create a flag in LaunchDarkly that allows users to see the new website.  

Once enabled, the Unicorn.Rentals UI will update, and you'll be able to access a new API on the `/status` route, which you can use to validate that the correct version of Unicorn.Rentals has launched! When you're creating the flag, keep in mind that we are just saying that the new site is available, true or false, choose the flag type that matches these options.   
"""
TASK2_INDEX=20
TASK2_MARKDOWN=True

TASK2_UNRELEASED_KEY="task2_app_unreleased"
TASK2_UNRELEASED_LABEL="Uh oh... This status doesn't look very good..."
TASK2_UNRELEASED_INDEX=21
TASK2_UNRELEASED_VALUE="The status code you entered is incorrect. Is the website actually released? Check your feature flag key and ensure it matches what the development team has in their code!"
TASK2_UNRELEASED_MARKDOWN=True

TASK2_COMPLETE_KEY="task2_complete"
TASK2_COMPLETE_LABEL="The new Unicorn.Rentals is **LIVE** for user traffic!"
TASK2_COMPLETE_VALUE="""
Toggling the feature flag on for `SiteRelease` has enabled the new version of the Unicorn.Rentals website, however, something looks wrong. You can see debug messages reflected in the card views on the main page. Looks like it's time to dig in and figure out what went wrong!
"""
TASK2_COMPLETE_INDEX=29
TASK2_COMPLETE_MARKDOWN=True


# TASK 3 - Access Key
TASK3_KEY="task3"
TASK3_LABEL="Task 3 - Uh, we've got a problem here. This data looks off."
TASK3_VALUE="""
Your team noticies significant amounts of debug data on the newly released Unicorn.Rentals site. You could leverage a "kill switch" in LaunchDarkly to quickly turn the feature flag off for all users, removing the problem website from view, but our innovative teams have given us another option.

The development team has placed enhanced logging for both our server and client side behind a feature flag. This allows teams to activate enhanced logging for specific users to help isolate problems. Your team will need to create and manage this feature flag in LaunchDarkly and configure the target to be our `debuguser`.

We will use multiple variations within LaunchDarkly to confiugure different potential values that our feature flags may resolve to. 

##### Feature Flag Details to Create in LaunchDarkly
* **Feature Flag Name** - `logMode` 
* **Flag Type** - String
* **Variation 1** - Value `debug`, Name -  Debug
* **Variation 2** - Value `default`, Name - Default Logging
* **Default Variation** for `On` and `Off` to be Default Logs
* **Individual Targeting** - set `debuguser` to receive the `Debug` feature flag value

Once enabled, login as `debuguser` to view the administrative menu, you can enter the value from this UI menu or visit the `/teamdebug` API route and enter the `debug-code` value in the input below. 
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
TASK3_COMPLETE_LABEL="Success! You found the debug answer!"
TASK3_COMPLETE_VALUE="""
Upon enabling the debug menu you have found that the application is still connecting to its local debug data. In order to resolve the new data, we'll need to update the code for our application to enable the new connectivity feature flag. We'll need to update the code in our CodeCommit repository, allow our website image to rebuild, and AWS App Runner to automatically deploy the new version of our application. Let's get started! 
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
