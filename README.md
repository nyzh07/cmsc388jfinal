# CMSC388J Final Project

## Project Writeup

*Description of our final project idea:*

Our project is a recipe website that allows users to discover, explore, and review a wide range of recipes. We integrated Spoonacular API to fetch recipe data, including images, descriptions, and ingredients, helping us achieve a rich and informative browsing experience. 

1. On the home page, random recipes are displayed, allowing users to scroll through and find inspiration for their next meal. 

2. Users can search for recipes by keywords. After each search, up to 30 recipes are retrieved and displayed, matching the search term in their titles. 

3. Users can register to create an account with a username, email and password. Secure login functionality allows users to access personalized features, like adding a profile photo and writing reviews. 

4. Recipes and reviews are visible to all users, encouraging recipe discovery and personalization. Any user, whether logged in or not, can still browse recipes, search for specific dishes, and view existing reviews and ratings.

5. Going to a user’s page will display the reviews they have written, including the time of review, the specific recipe, the content of the review, and the total number of reviews. 

*Describe what functionality will only be available to logged-in users:*

Logged-in users can write recipes reviews, including a star rating (out of 5) to reflect their personal experience and opinions, and a comment to provide feedback or share their thoughts. Logged-in users also have a username, and can add or update their username and a profile photo. 

*List and describe at least 4 forms:*

Search Form: Allows users to search for recipes using keywords
> Search bar where users must type a string
> 
> Submit button to initiate the API request
> 
> Displays up to 30 recipe results that match the query

Recipe Review Form: Enables logged-in users to provide feedback on recipes by rating them and providing comments

> Comment field where users must enter text
> 
> Clickable star rating input of 1 to 5 stars
>
> Submit button to save the review to our MongoDB database
>
> Review is visible to all users under the recipe details and on the review page of the user who wrote the review

Registration Form: Allows new users to create an account on the website

> Username and email address fields that must be unique
> 
> Password field where users must enter a password
> 
> Confirm password field where users must enter the same password
> 
> Submit button to create the account after validation
> 
> Redirects users to the login page after successful registration or displays error messages if not validated

Login Form: Allows registered users to login to their accounts

> Username field to enter username string
> 
> Password field to enter password
> 
> Submit button to log in
> 
> Redirects users to their account page or displays error messages for incorrect credentials

Update Username Form: Allows logged-in users to update their account username

> New username field to enter a new username string
>
> Submit button to save the new username to the user’s profile
>
> Reflects the changes on the user’s profile if validated or displays error messages if not

Update Profile Picture Form: Allows users to upload a new profile picture or change their current profile picture

> File upload field where users can select an image file from their device 
>
> Submit button to upload the image and update the user’s profile

*List and describe your routes/blueprints (2 blueprints, 2 routes for each):*

**Users**

Registration - /register

> Allows users to create an account
> 
> Renders the login page after saving the user if validated
> 
> If a user is already logged in, they are taken to the home page

Login - /login

> Allows registered users to log in to their accounts
>
> Renders the account page if the user’s credentials are correct
>
> If the user is already logged in, they are taken to the home page

**Recipes**

Home Page - /

> Landing page where users can browse a selection of random recipes

Recipe Details - /recipes/<recipe_id>

> Displays recipe information, including the image, description, ingredients and instructions
>
> Fetches recipe details from the Spoonacular API based on the recipe ID provided
>
> If the user is logged in, they can add a review

*Describe what will be stored/retrieved from MongoDB:*
Reviews and user information are stored and retrieved from MongoDB. The review document contains a comment, star rating, recipe ID, reference to the user, and a timestamp. The user document contains a username, email, password, and optional profile picture. 

*Describe what Python package or API you will use and how it will affect the user experience:*
We used Spoonacular API to create a dynamic and interactive recipe browsing and reviewing website. The Spoonacular API provides access to a comprehensive database of recipes, including titles, images, descriptions, ingredients and instructions. This integration allows users to discover recipes with clarity and ease. Combined with the user-submitted reviews, our website offers an engaging experience where users can explore recipes and contribute their own feedback.

## Website Deployment ##
Deployed on Vercel: https://cmsc388jfinal.vercel.app/ 
