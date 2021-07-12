# Omnilytics

Data Mining Challenge

Description:
Scrape all shoe items under https://www.zalora.com.my/ 
website and for the brand “Aldo” under the filter “Occasion” “Casual”.

https://www.zalora.com.my/women/shoes/?from=header&occasion=Casual&brand=aldo

Note1: The output should be a JSON file with the following fields:
Brand, Actual price, Discounted price, link to the image of the product.

Note2: Products in all pages should be scraped (paginated pages).

Note3: Use python Requests module to do this only. (Selenium is not accepted).

Note4: Create a docker image (yml file) which performs this task upon launch and save the output in the host machine (not inside the docker image itself).

Note5: Host the whole project in a GitHub repository and share the link.
