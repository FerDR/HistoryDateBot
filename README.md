# HistoryDateBot
Facebook bot that posts historic event that happened on the current date

Gets the current date on a random timezone (from UTC-12 to UTC+14) and fetchs the wikipedia page of the date.
Then picks a random line from the page with different odds: 65% for events, 15% for births and deaths and 5% for holidays.
Afterwards tries to find a related wikipedia page to obtain an image, it gets a random image (except svg because Facebook doesn't like those) from the related page and posts it.
