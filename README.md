# E-commerce Web Interface in Django

This is a Django-based web interface for an e-commerce platform. The project can be installed directly using the UV project manager.

## Features

### Home Page
- The homepage displays the top 6 most-viewed products on the site.
- For each product, the following details are shown:
  - Product photo (same for all products for simplicity)
  - Product name
  - Price
  - Option to buy the product.
- Clicking on the product's photo or name redirects the user to the product's dedicated page where they can also purchase it. A purchase confirmation screen follows.

### Search & Navigation
- You can search for products using a search bar or select categories from a dropdown menu.
- Option to return to the homepage or log in to your account (or log out).

### User Account
- A screen for logging in or creating an account if the user doesn’t have one, with the option to choose whether to become a seller.
- In the user profile page:
  - Users can track their orders and become a seller if they haven't already.
  - Sellers can list new products and monitor the status of their products and orders.

### Product Creation
- Sellers can create new products, which can be categorized as "Generic," "Books," or "Mobile Phones."
- Required fields for all products: Name, Price, Description, and Stock Quantity.
- For books, additional fields for Author and Number of Pages appear.
- For mobile phones, an additional field for Brand appears.
- Each created product has its own page displaying key information along with the option to purchase it. Sellers can also edit or delete their products.

### Product Status & Seller Dashboard
- Sellers can track the stock of their products, update stock if necessary, and edit or delete their products.
- Sellers can also track their sales and update the delivery status of their orders.

### Order Tracking (Customer)
- Customers can track the status of their orders, which is updated by the seller.

### API Integration
- An API has been configured using the Django REST framework to provide product data for the e-commerce platform (excluding the number of views for each product).