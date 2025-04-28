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
 
- Product Listing Management:
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

- Product Search:
  - When Buyers are searching for products in the catalogue, they have the ability to search using keywords specific to an attribute of the product.
  - Displayed info on the Product Catalogue: Seller Email, Product Name, Price, Listing ID, Quantity, and Category
  - Each attribute (besides Category) can be searched for by choosing one attrbiute to search by, as well as what keyword to search with


# Running the Code
The "ready to run" code is in app.py - run app.py to generate the webpage, and then visit http://127.0.0.1:5000 on any web browser to use the application. Be sure to download app.py as well as the templates, and NittanyBusinessDataset_v3 folders along with the files inside them. All of these files & folders must be in the same directory for the code to run.
