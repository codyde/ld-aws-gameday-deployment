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
It's Day 1, your first build pipeline for the the new Unicorn.Rentals website is running currently. Roll up your sleeves, crack your knuckles, and get the application UP! 

As the Cloud Administrator at Unicorn.Rentals, you need to deploy the image for the website using AWS App Runner.  

## App Runner Configuration: 

1. **Container Image URL** - Select **Browse** and type in `unicornrentalsapp` in the image list, choose the corresponding image. The image name will have have many additional characters in addition to `unicornrentalsapp` that is the correct one. If you do not see the image, check to see if you pipeline has finished building and refresh App Runner. 
2. **ECR Access Role** - Select **Create new service role** and use the default name that appears.  
3. **Service name** - Your choice! 
4. **Environment Variables** - Create one called `LD_SERVER_KEY` and use the Server SDK key from above as the value 
5. **Port** - Set it to `5000`
6. **Security Tab > Instance role** - Set to `LDUnicornAppRunnerInstanceRole`

When you complete the above steps, enter the name you created (**CASE SENSITIVE**) below to validate your configuration.

**Note: Incorrect submissions will cost you!**
"""
TASK1_INDEX=10
TASK1_MARKDOWN=True

# TASK 1 - For outputting LD credentials
TASK1_CREDS_KEY="task1_creds"
TASK1_CREDS_VALUE="### Use the following credentials:"
TASK1_CREDS_INDEX=2
TASK1_CREDS_MARKDOWN=True

TASK1_APPRUNNER_WRONG_KEY="task1_bad_app"
TASK1_APPRUNNER_WRONG_LABEL="Well - there's nothing here"
TASK1_APPRUNNER_WRONG_VALUE="""
Uh oh! The App Runner name you entered isn't returning any data! Its possible that you used the wrong case int he name, or just a simple hoof-typo. Happens to the best unicorns. Sorry about the points loss! Head over to **App Runner** in your AWS account and give it another try.
""" 
TASK1_APPRUNNER_WRONG_INDEX=11
TASK1_APPRUNNER_WRONG_MARKDOWN=True

TASK1_APPRUNNER_INPUT_REMOVED_KEY='task1_input_remove'
TASK1_APPRUNNER_INPUT_REMOVED_LABEL="Input evaluating..."
TASK1_APPRUNNER_INPUT_REMOVED_VALUE="Our Unicorns are currently checking the status of this answer... standby"
TASK1_APPRUNNER_INPUT_REMOVED_INDEX=16
TASK1_APPRUNNER_INPUT_REMOVED_MARKDOWN=True


TASK1_APPRUNNER_COMPLETE_KEY="task1_apprunner_complete"
TASK1_APPRUNNER_COMPLETE_LABEL="Unicorn.Rentals is up and running!"
TASK1_APPRUNNER_COMPLETE_VALUE="""
Unicorn.Rentals is in the process of deploying. You created an App Runner deployment of the new marketing website, and validated the URL thats being generated, which will be functional shortly (within 5-10 minutes). You are one step closer to having the site live and serving user traffic! 

We're going to use LaunchDarkly to manage our feature releases separate from the deployment using [Feature Flags](https://launchdarkly.com/blog/what-are-feature-flags/).

While the site is building, we need to acquire an API key that other teams can use to integrate with LaunchDarkly services. Navigate to LaunchDarkly and [create an API token](https://docs.launchdarkly.com/home/account-security/api-access-tokens#creating-api-access-tokens) using the `Custom Role` option with your student box checked, you don't need to change any other settings. Copy this API key and paste it below for the other teams at Unicorn.Rentals to use! 

It's time to start creating our feature flags and launching the **NEW** Unicorn.Rentals!
"""
TASK1_APPRUNNER_COMPLETE_INDEX=13
TASK1_APPRUNNER_COMPLETE_MARKDOWN=True

# API Task addition
TASK1_API_WRONG_KEY="task1_bad_api"
TASK1_API_WRONG_LABEL="This API key doesn't appear valid"
TASK1_API_WRONG_VALUE="When our Unicorns tried to check the API key, it didn't return valid data. Check that you've created the API key with the correct role, and that you copied the correct key value."
TASK1_API_WRONG_INDEX="17"
TASK1_API_WRONG_MARKDOWN=True

# API Task addition
TASK1_COMPLETE_KEY="task1_complete"
TASK1_COMPLETE_LABEL="App is up, and API is good!"
TASK1_COMPLETE_VALUE="The Unicorn.Rentals site is spinning up in AWS App Runner and the LaunchDarkly API key is validating successfully. You have all the tools in place now to begin releasing the Unicorn.Rentals site to end users!"
TASK1_COMPLETE_INDEX="18"
TASK1_COMPLETE_MARKDOWN=True

# TASK 2 - Releasing
TASK2_KEY="task2"
TASK2_LABEL="Task 2 - Releasing the new Unicorn.Rentals!"
TASK2_VALUE="""
You just received a notification from the web development team that the new version of the Unicorn.Rentals website is ready for user testing! 

They included a **[feature flag](https://launchdarkly.com/blog/what-are-feature-flags/)** in the new code that is preventing it from being seen by most users. It's now up to you to create a flag in [LaunchDarkly](https://app.launchdarkly.com) that allows users to see the new website. Here are your tasks: 

1. Check the [application code](https://github.com/codyde/ld-aws-gameday/blob/db49c4be0791e2cb0a46c7d0f803ac078067644a/pages/index.js#L58) and locate the name of the flag and information about the flag.
2. Use this information to create a feature flag in LaunchDarkly that will release the Unicorn.Rentals website.

Once the feature flag is enabled, you should see the new site! You'll also be able to access a new API on the `/status` route. Use that path to retrieve the version of Unicorn.Rentals that is running. We will verify that you have the correct version by validating value in the input box below.   
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
Your team notices significant amounts of debug data on the newly released Unicorn.Rentals site. We could just turn off the flag and take the site down, but fortunately we have another option.

During development, the team added enhanced logging, behind a feature flag, for specific users. Enabling this flag will help those users to help isolate problems. For this task, we'll create a feature flag in LaunchDarkly and configure it to target to be our `debuguser`. For this task you'll need to:

1. Check the application code to find the feature flag configuration. You can use the [client-side code](https://github.com/codyde/ld-aws-gameday/blob/a383dbf064d081b841937b27b637519243726470/pages/index.js#L78) or the [server-side code](https://github.com/codyde/ld-aws-gameday/blob/6cfe5fc27d2d1a05d99cf815563ace17b504f2b1/main.py#L195) for this information. 
2. In LaunchDarkly, create a [multi-variate feature flag](https://docs.launchdarkly.com/home/flags/variations) that matches the code. 
3. Create a [targeting rule](https://docs.launchdarkly.com/home/flags/targeting-users) that serves the `debug` feature for `debuguser` and serves the `default` rule to everyone else. 

Once enabled, login as `debuguser` to view the administrative menu, you can enter the value from this UI menu or visit the `/teamdebug` route. Enter the `debugcode` value in the input below. 
"""
TASK3_INDEX=30
TASK3_MARKDOWN=True


TASK3_INCORRECT_KEY="task3_incorrect"
TASK3_INCORRECT_LABEL="The status code you entered is invalid or your targeting rule is missing"
TASK3_INCORRECT_VALUE="""
We need the status code, and to ensure that only our targeting unicorn, `debuguser`, is receiving the logMode. It appears that either the status code value that you showed is incorrect, or your targeting rule is missing for this feature flag. Ensure you've created the correct feature flag of `logMode`, targeted the `debuguser` with the `debug` value, and enabled the feature flag.
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
From our last task, we learned that we are using local debug data instead of the database in AWS. Fortunately, we can use a feature flag to [roll out the database change](https://launchdarkly.com/blog/database-migration-using-launchdarkly/) to the Unicorn.Rentals environment. 

Just like before, the development team has already staged our code for the database migration. To complete this task you must do the following: 

1. Check the [application code](https://github.com/codyde/ld-aws-gameday/blob/6cfe5fc27d2d1a05d99cf815563ace17b504f2b1/main.py#L128) and retrieve the flag information. 
2. Create a feature flag in LaunchDarkly to enable the database change.  

After the feature flag is enabled, navigate to the `/health` endpoint to determine if Unicorn.Rentals is operating on the migrated cloud database. 
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
TASK4_CORRECT_VALUE="""
Your migration is successful, you are now returning data to the Unicorn.Rentals UI from AWS DynamoDB!  

In this example, we just made a hard switch to the new database, but with LaunchDarkly these changes can be made either gradually, or all at once. If we had discovered a problem with the database connection - we can disable the feature and return it back to the original code in milliseconds (the "kill switch").

All in a days work for a Unicorn Admin!
"""
TASK4_CORRECT_INDEX=43
TASK4_CORRECT_MARKDOWN=True


# QUEST COMPLETE
QUEST_COMPLETE_KEY='quest_complete'
QUEST_COMPLETE_LABEL="You're a Dark Launcher now!"
QUEST_COMPLETE_VALUE='Congratulations! You have successfully created feature flags for several features, used targeting to roll out features to specific users, and even migrated a database - all without redeploying your application once! Great work!'
QUEST_COMPLETE_INDEX=100
QUEST_COMPLETE_MARKDOWN=True