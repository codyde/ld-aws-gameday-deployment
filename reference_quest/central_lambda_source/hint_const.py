# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.

# HINT STATUS
STATUS_OFFERED="OFFERED"
STATUS_DISPLAYED="DISPLAYED"


# TASK 1 HINTS
TASK1_HINT1_KEY="task1_hint1"
TASK1_HINT1_LABEL="Need help with your App Runner deployment?"
TASK1_HINT1_DESCRIPTION="Click on the Reveal Hint button to get some guidance. Remembers, hints will cost you!"
TASK1_HINT1_VALUE="""
You can check for the URL in the App Runner console. Try browsing the page first. If the app is not up - its possible that the environment variables were not provided during deployment. The LaunchDarkly SDK key can be found in LaunchDarkly by pressing CMD+K or CTRL+K and selecting copy. For the AWS App Runner instance role, it needs to be in place in order to allow communication.
"""
TASK1_HINT1_INDEX=19
TASK1_HINT1_COST=200


# TASK 2 HINTS
TASK2_HINT1_KEY="task2_hint1"
TASK2_HINT1_LABEL="Is your feature not deploying?"
TASK2_HINT1_DESCRIPTION="Bad launch? Click reveal to get an additional hint. "
TASK2_HINT1_VALUE="Check the console logs for the application for error messages to ensure your SDK key is configured successfully. Ensure you have created a boolean flag in LaunchDarkly."
TASK2_HINT1_INDEX=27
TASK2_HINT1_COST=200


# TASK 3 HINTS
TASK3_HINT1_KEY="task3_hint1"
TASK3_HINT1_LABEL="Having difficulty rotating the user's credentials"
TASK3_HINT1_DESCRIPTION="If you're stuck, click on the Reveal Hint button to get some guidance"
TASK3_HINT1_VALUE="""
Ensure that you have navigated to your team's AWS Console. Then click on 'Services' in the upper left and find 'IAM'.
Then. locate the 'Developer' user and... do we need to tell you everything?
"""
TASK3_HINT1_INDEX=37
TASK3_HINT1_COST=200
