Okay Howdy ya'll this here is Jimbos Robot, Imagine me as that paperclip that used to pop up on desktops to help users, but with a cowboy hat!

**********Purpose of program**********
miami_lakes is currently a command line tool that can help migrate the content of a large number of pages onto one of the DI Dev sites.

With specific commands that will be listed later in this file, the user can migrate, and store content from a large number of links all at once.
Most of the content is added via REST api but the Yoast Meta info cannot be added that way.
That's where Selenium comes in but you can see that more clearly in the Program Flow section below


------------Prerequisites:
Create the Google Sheet and getting the ID :
1.) Create a new google sheet, name it "Luther [site name], paste the links into column A. Make sure that there are no empty rows.
2.) Highlight all of the rows, right click and select "Remove link"
3.) Click "Share" at the top right. Under "Get Link", click "change", select "Anyone with the link". Click "Done"

4.) Copy the file ID from the spreadsheet URL. It is located between '/d/' and '/edit#....'
  For example, in this hyperlink, https://docs.google.com/spreadsheets/d/1ZLZGZACl0kw5GmsDXDXgFtTGrn9X2RQgnH6odhNc3vI/edit#gid=0,
  the file id is '1ZLZGZACl0kw5GmsDXDXgFtTGrn9X2RQgnH6odhNc3vI'

---
Download Python 3.7.3 - that's the one I use at least
#use `python3 --version' to see if you are using python 3 or not
#using 'python --version' should show you the 2.7.16 or whatever version came by default on your mac
---

A devsite

-------
make sure the metaHousing.sqlite file is blank

---------
an ID or classname to target
#if there are classnames within that element that you want to exclude we can account for that as well.
`



  ------------Program Flow:
  - during each iteration, we get the page ID within the "page" Method and return that as the value
  - which we then add to the metaData table in metaHousing.sqlite (which was created when we run main.py)







------Sidenotes:
- I changed my default shell on my Mac at one point today, I don't know if that's a big deal or not.
- https://support.apple.com/en-us/HT208050 <- there is more info there and the command line stuff is the same ¯\_(ツ)_/¯

Current Github Token: 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


**********NOTES FOR EXPANSION**************
#TODO: Error Handling:
# 1.) Need something to handle exceptions for when we can't target everything
#     i.e. using this command from main.py "scrape.livePage(url, 'content1', devsite, db)"
#     if the pages in the list don't all have "content1" as something that can be selected
#     we need to be able to handle that and either audible to a list of potential targets
#     or skip it and move on to the next iteration


#TODO: Turn into GUI that can download all the needed modules and even update them
#   display error messages in the GUI so user knows if issues occur
#   have a "restart" or "clear" button that can reset the tool (i.e. delete database, etc...(idk what else))

#TODO: Change Yoast Meta https://developer.yoast.com/blog/yoast-seo-rest-api-endpoint/
#       1. Scrape meta
#       2. getPostID of page
#       3. send edits to rest endpoint

#TODO: Make this work for blogs. It should basically function the same but you'll need to scrape
#      date-of-publish, categrory, & tags
