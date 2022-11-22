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
Double check that you used the right Instance Role. If the ECR Access Role says it already exists, just add a number to the default role name.
Verify that you used the right environment variables and port 5000
You can check for the URL in the App Runner console and try browsing the page.
"""
TASK1_HINT1_INDEX=9
TASK1_HINT1_COST=1000


# TASK 2 HINTS
TASK2_HINT1_KEY="task2_hint1"
TASK2_HINT1_LABEL="Is your feature not deploying?"
TASK2_HINT1_DESCRIPTION="Bad launch? Click reveal to get an additional hint. "
TASK2_HINT1_VALUE="Check the console logs for the application for error messages to ensure your SDK key is configured successfully. Ensure you have created a boolean flag in LaunchDarkly, turned targeting ON and saved!"
TASK2_HINT1_INDEX=27
TASK2_HINT1_COST=1000


# TASK 3 HINTS
TASK3_HINT1_KEY="task3_hint1"
TASK3_HINT1_LABEL="Having a hard time with the right flag configuration?"
TASK3_HINT1_DESCRIPTION="If you're stuck, click on the Reveal Hint button to get some guidance"
TASK3_HINT1_VALUE="""
This is going to be a string flag, with 2 different values. The code links above will show you that the flag values should be `debug` (variation 1, the On value by default) and `default` (variation 2, the Off value by default)
"""
TASK3_HINT1_INDEX=37
TASK3_HINT1_COST=1000

# TASK 4 HINTS
TASK4_HINT1_KEY="task4_hint1"
TASK4_HINT1_LABEL="Not able to migrate the database connectivity?"
TASK4_HINT1_DESCRIPTION="If you're stuck, click on the Reveal Hint button to get some guidance"
TASK4_HINT1_VALUE="""
The feature flag is a JSON based feature flag with values for the database host type, database name, and mode. Ensure you've formatted it properly as per the code in the description text.
"""
TASK4_HINT1_INDEX=47
TASK4_HINT1_COST=1000