#Devin Brown 01/01/2019
##Work done for County of Sonoma PRMD
This project was created during an internship for the County of Sonoma Informations Systems Department and was intended for use by the counties PRMD division. The project was created to help clean up a publicly facing table used by PRMD. An entry in the table contains name and address information in varying formats. The goal of this project is to parse and move information stored in bulk single columns to their properly labeled column. An example of the would be breaking up an entire mailing address stored as a single entry into its street, city, and zip components and storing each value in its properly labeled column.  

This project is using Python3 and takes advantage of the following open source advancced natural language procesing libraries https://github.com/datamade/usaddress and https://github.com/GreenBuildingRegistry/usaddress-scourgify both of which can be installed using pip install with the names usadress and usadress-scourgify.





