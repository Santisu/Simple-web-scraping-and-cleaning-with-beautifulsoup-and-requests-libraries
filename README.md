# Simple web scraping and cleaning with beautifulsoup and requests libraries
A brief example script of web scraping using requests and beautifulsoup libraries and data cleaning.

# About

This is a brief example of data scraping. For this example we are going to scrap the One Piece spanish wikia site.

Using requests library we are going the get the wiki site of each chapter, then, using beautifulsoup4 library, we are going to scrap the data that we want to store on a CSV file. Saving the desired info of each chapter on a new row of our CSV, and making sure that the errors are catched to be handled after.

Once our data is stored, we are going to check that the dates have our standarized date format and clean the dirty dates.
