# Unicorn.Rentals New Website   

Collection of the website code for our website, Unicorn.Rentals

Quickstart locally with Docker - 
* populate the .env file in the root directory with your LD information
* Execute the following command: 
`docker build -t <yourrepo>:<yourtag> .; docker run -d -p 5000:5000 <yourrepo>:<yourtag>`
* 3 flags are needed - `siteRelease` (boolean), `dbDetails` (json), `logMode` (multi-variate string; values should be 'default' and 'debug')