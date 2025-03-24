# NittanyBusinessWPTGB
NittanyBusiness enables businesses to buy products from other businesses. The current implementation includes:
- Database Creation, imported from the dataset csvs
  - Passwords are hashed
  - Primary keys are generated as specified
- Create Account Functionality
  - Email, Password and Confirm Password fields
  - Input sanitization Modals (inputs must have an @, password & confirm password fields must match, fields can not be null, account created cannot match existing account)
- Account Login Functionality
  - Password hidden while writing
  - Incorrect Password Modal
  - Login leads to landing page, with user email passed over as a parameter (will help in future implementation).

# Running the Code
The "ready to run" code is in app.py - run app.py to generate the webpage, and then visit http://127.0.0.1:5000 on any web browser to use the application. Be sure to download app.py as well as the templates, and NittanyBusinessDataset_v3 folders along with the files inside them. All of these files & folders must be in the same directory for the code to run.
