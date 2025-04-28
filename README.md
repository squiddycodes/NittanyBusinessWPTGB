# NittanyBusinessWPTGB
NittanyBusiness enables businesses to buy products from other businesses, sell products to other businesses, and has a helpdesk user type for moderation of the site. Our implementation includes:
- Database Creation, imported from the dataset csvs
  - Passwords are hashed
  - Primary keys are generated as specified
  - Creation is upon first run of app.py
- Create Account Functionality
  - Email, Password and Confirm Password fields
  - Input sanitization Modals (inputs must have an @, password & confirm password fields must match, fields can not be null, account created cannot match existing account)
  - Dropdown for account creation of three user types: Buyer, Seller, and HelpDesk
  - Helpdesk user creation sends form that must be accepted before account access
- Account Login Functionality
  - Password hidden while writing
  - Incorrect Password Modal
  - Login leads to respective user landing page (different for the 3 users)
 
- Product Listing Management - Sellers:
  - Found within each Seller's Lading Page are two buttons that will allow them the ability to edit, add, or remove products from the catalogue available to Buyers.
    - My Products:
      - Leads Sellers to a list of all their registered products on Nittany Business, being able to view the Product's Name, ID, Category, Quantity Available, and its current status.
      - Clicking on the product's name will open a new page where the Seller can edit all attributes of the product.
      - Leaving any field blank will maintain the current attribute's value.
      - Once the Seller is satisfied with the changes, they can choose to Submit them or Return to the Product List, leaving the product unchanged.
      - If the changes were submitted, they are viewable immediately.
    - Register a Product
      - Leads Sellers to a page where they must enter all required Fields to submit their new product.
      - Fields include: Title, Name, Description, Category, Quantity, Price, and Status
      - Once submitted, the new product is viewable under the Seller's product list, and, if activated, viewable to Buyers.

- Product Search - Buyers:
  - When Buyers are searching for products in the catalogue, they have the ability to search using keywords specific to an attribute of the product.
  - Displayed info on the Product Catalogue: Seller Email, Seller Rating, Product Name, Price, Listing ID, Quantity, and Category
  - Each attribute (besides Category and seller rating) can be searched for by choosing one attrbiute to search by, as well as what keyword to search with
  - Categories can be traversed through the dropdown, Go! and Back buttons. Products are loaded from the current category selected, and all of its children categories (not past one tree level, as specified in the requirements).
- Product Purchase - Buyers
  - Buyers can select products from the product catalogue,
  - Product pages show the product and seller's details, and prompt the user for the quantity they want to buy
  - after selecting a valid quantity (invalid quantity shows a modal), the user can place their order, and leave a review. The order and review is entered into database.db.
  - Reviews are on a 5 star scale, if the user wants to leave a review they can select a star rating, and write a short message (<100 characters). They will then be brough back to the product page.

- Editing Profile Information - Buyers & Sellers
  - Buyers and Sellers can both edit their profile information, given they provide their password.
  - Zip codes must be valid to be edited, and must be in the database already (our db has all zipcodes we ship to). Zip codes automatically determine the city and state.
  - Buyers and sellers can submit a request to change their UserID, but it will not happen right away.
 
- Reviewing Requests - HelpDesk
  - HelpDesk users can view requests submitted to them, including Site Maintenence Requests and Staff Recruitment Requests.
  - HelpDesk users can approve Staff Recruitment Requests given to them, allowing the new user to log in as a HelpDeskUser.


# Running the Code
The "ready to run" code is in app.py - run app.py to generate the webpage, and then visit http://127.0.0.1:5000 on any web browser to use the application. Be sure to download all py files as well as the templates, and NittanyBusinessDataset_v3 folders along with the files inside them. All of these files & folders must be in the same directory for the code to run. Database.db will be automatically generated when you run the code.
