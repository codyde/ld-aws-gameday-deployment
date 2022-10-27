# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.

# WELCOME
WELCOME_KEY="welcome"
WELCOME_LABEL="Welcome to the (soon to be) NEW Unicorn.Rentals"
WELCOME_VALUE="""
At Unicorn.Rentals, we hire dreamers not just "techs”. We seek those who share our vision and are willing to put in extra hours to take our offering of mythical creatures to the next level. Our solutions are diverse and the things we are building are going to delight our users. 

But first... Unicorn.Rentals needs to deliver it's next generation, cloud hosted, marketing website! As the core team responsible for the deployment and migration, you'll ship the features that power Unicorn.Rentals new marketing website, and debug any problems that come up when the Unicorns break loose. Throughout this challenge you'll explore rolling out the new website, building feature flags, troubleshooting problems, and rolling out new capabilities... hopefully with no broken horns! 
"""
WELCOME_INDEX=1
WELCOME_MARKDOWN=True


# TASK 1 - App Runner Deployment
TASK1_KEY="task1"
TASK1_LABEL="Task 1 - Unicorns in the Clouds! Deploying the new Unicorn.Rentals!"
TASK1_VALUE="""
The pipelines have ran and its time to deploy our new Unicorn.Rentals into AWS! Roll up your sleeves, crack your knuckles, and get the application UP. 

As the Cloud Administrator at Unicorn.Rentals, you'll need to deploy the image for the website to AWS App Runner. As part of this exercise, ensure the following configurations are applied: 

* For the image, select **Browse** and type in `unicornrentalsapp` in the image list, and use this as your image. **NOTE: The actual image name will have have many additional characters on the front and end of "unicornrentalsapp" - this is to ensure your Unicorn is the most unique Unicorn possible.**
* For the **ECR Access Role** ensure you have selected the `AppRunnerECRAccessRole` from the list
* Create an environment variable named `LD_SERVER_KEY`, with the matching Server SDK key values from the credential list (or from within LaunchDarkly). This allows the server component of your application to render feature flags from LaunchDarkly. The client side SDK is not needed for this step. 
* Create an additional environment variable for your **Team ID** named `TEAM_ID` and the TEAM value from your credentials. 
* Set the port for the App Runner application to `5000`
* On the security tab, ensure you have selected the **instance role** titled **LDUnicornAppRunnerInstanceRole** to allow connectivity to the necessary Unicorn.Rentals cloud resources 

When your deployment is complete and running successfully (this may take around 5 minutes), enter the full URL (including https://) below and the system will validate if the application is up! 

**Note: Incorrect submissions will cost you! Ensure the website is fully up before you submit, or you'll lose reputation along with score!**
"""
TASK1_INDEX=10
TASK1_MARKDOWN=True

# TASK 1 - For outputting LD credentials
TASK1_CREDS_KEY="task1_creds"
TASK1_CREDS_VALUE="### Use the following credentials:"
TASK1_CREDS_INDEX=2
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
You just received a notification from the web development team that the new version of the Unicorn.Rentals website is ready for user testing! They have pushed their changes to the site already, but also included a **[feature flag](https://launchdarkly.com/blog/what-are-feature-flags/)** that is preventing it from being seen by most users. As the engineer helping roll out the new site and release the changes, it's now up to you to create a flag in [LaunchDarkly](https://app.launchdarkly.com) that allows users to see the new website. 

The development team has included the details for the feature flag to be created in the application code [here](https://github.com/codyde/ld-aws-gameday/blob/a383dbf064d081b841937b27b637519243726470/pages/index.js#L55). Use this information to create a feature flag that will release the Unicorn.Rentals website with LaunchDarkly.

Once the feature flag is enabled, you'll be able to access a new API on the `/status` route, which you can use to validate that the correct version of Unicorn.Rentals has launched! We will use this value in the input box below.   
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
Toggling the feature flag on for `siteRelease` has enabled the new version of the Unicorn.Rentals website, however, something looks wrong. You can see debug messages reflected in the card views on the main page. Looks like it's time to dig in and figure out what went wrong!
"""
TASK2_COMPLETE_INDEX=29
TASK2_COMPLETE_MARKDOWN=True


# TASK 3 - Access Key
TASK3_KEY="task3"
TASK3_LABEL="Task 3 - Uh, we've got a problem here. This data looks off."
TASK3_VALUE="""
Your team noticies significant amounts of debug data on the newly released Unicorn.Rentals site. You could leverage a "kill switch" in LaunchDarkly to quickly turn the feature flag off for all users, removing the problem website from view, but our innovative teams have given us another option.

The development team has placed enhanced logging for both our server and client side behind a feature flag. This allows teams to activate enhanced logging for specific users to help isolate problems. Your team will need to create and manage this feature flag in LaunchDarkly and configure the target to be our `debuguser`.

We will use multiple [variations within LaunchDarkly](https://docs.launchdarkly.com/home/flags/variations) to configure different potential values that our feature flags may resolve to. Variations allow LaunchDarkly to serve up multiple different value types based on what version is set to enabled, or what targeting rules you have configured for users or systems.

The development team has included comments in the application code around what feature flag configuration should be implemented for this task. You can find the [client-side code here](https://github.com/codyde/ld-aws-gameday/blob/a383dbf064d081b841937b27b637519243726470/pages/index.js#L78) and the [server-side code here](https://github.com/codyde/ld-aws-gameday/blob/6cfe5fc27d2d1a05d99cf815563ace17b504f2b1/main.py#L195) (the comments are the same between each - you do not need to use both). Browse the code to find the details, and create the multi-variate feature flag. Create a [targeting rule](https://docs.launchdarkly.com/home/flags/targeting-users) that points at `debuguser`, and enables the **Debug** feature for them, while serving the `default` rule to everyone else. 

Once enabled, login as `debuguser` to view the administrative menu, you can enter the value from this UI menu or visit the `/teamdebug` API route and enter the `debugcode` value in the input below. 
"""
TASK3_INDEX=30
TASK3_MARKDOWN=True


TASK3_INCORRECT_KEY="task3_incorrect"
TASK3_INCORRECT_LABEL="The status code you entered is invalid"
TASK3_INCORRECT_VALUE="""
It appears the status code value that you showed is incorrect. Ensure you've created the correct feature flag of `logMode`, targeted the `debuguser` with the `debug` value, and enabled the feature flag.
"""
TASK3_INCORRECT_INDEX=35
TASK3_INCORRECT_MARKDOWN=True


TASK3_COMPLETE_KEY="task3_complete"
TASK3_COMPLETE_LABEL="Success! You found the debug answer!"
TASK3_COMPLETE_VALUE="""
Upon enabling the debug menu you have found that the application is still connecting to its local debug data. This data was left in place from previous development iterations and was meant to be swapped out! Similar to before, we COULD kill switch this feature and disable the website entirely, but fortunately our development team gave us another option. 

The connectivity code for the database is in place and a feature flag is controlling it. We can use feature flags to rollout our database! Onto Task 4! 
"""
TASK3_COMPLETE_INDEX=39
TASK3_COMPLETE_MARKDOWN=True


# TASK 4 - Final question
TASK4_KEY="task4"
TASK4_LABEL="Task 4 - Time to migrate!"
TASK4_VALUE="""
Upon inspection of the debug code, you discover that the data is using the local debug data instead of the database in AWS that the development team intended on being used. Since feature flags allow us to control how code executes, we can use a feature flag to [roll out the database change](https://launchdarkly.com/blog/database-migration-using-launchdarkly/) to the Unicorn.Rentals environment - either gradually, or all at once. Furthermore, if we discover a problem with the database connection - we can disable the feature and return it back to the original code in milliseconds (the "kill switch"). 

Just like before, the development team has already staged our code for the database migration, along with the feature flag configuration that needs to be in place. These details can be found [here](https://github.com/codyde/ld-aws-gameday/blob/6cfe5fc27d2d1a05d99cf815563ace17b504f2b1/main.py#L128), and will provide you the necessary details for creating the feature flag to control which database is being used. 

After the feature flag is enabled for `dbDetails`, navigate to the `/health` endpoint to determine if Unicorn.Rentals is operating on the migrated cloud database. 
"""
TASK4_INDEX=40
TASK4_MARKDOWN=True


TASK4_WRONG_KEY="task4_wrong_answer"
TASK4_WRONG_LABEL="This database does not appear to be migrated yet"
TASK4_WRONG_VALUE="Looking at the return of the data, this database does not appear to be migrated. Please check your feature flags and ensure you are set to the correct database configuration in your feature flag."
TASK4_WRONG_INDEX=42
TASK4_WRONG_MARKDOWN=True


TASK4_CORRECT_KEY="task4_correct_answer"
TASK4_CORRECT_LABEL="Look at that, our Unicorns are ALL CLOUDY NOW!"
TASK4_CORRECT_VALUE="Your migration is successful, you are now returning data to the Unicorn.Rentals UI from AWS DynamoDB. All in a days work for a Unicorn Admin!"
TASK4_CORRECT_INDEX=43
TASK4_CORRECT_MARKDOWN=True


# QUEST COMPLETE
QUEST_COMPLETE_KEY='quest_complete'
QUEST_COMPLETE_LABEL="You're a Dark Launcher now!"
QUEST_COMPLETE_VALUE='Congratulations! You have successfully created feature flags for several features, used targeting to roll out features to specific users, and even migrated a database - all without redeploying your application once! Great work!'
QUEST_COMPLETE_INDEX=100
QUEST_COMPLETE_MARKDOWN=True
