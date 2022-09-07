You should come up with the JSON structure on you own and describe it in the README.md file for your repository or in a separate documentation file.


The RSS news should be stored in a local storage while reading. The way and format of this storage you can choose yourself.
Please describe it in a separate section of README.md or in the documentation.

New optional argument `--date` must be added to your utility. It should take a date in `%Y%m%d` format.
For example: `--date 20191020`
Here date means actual *publishing date* not the date when you fetched the news.


Update main functionality
 * Wrapping utility into distribution package using 'setuptools';
 * Adding versioning;
 * Updating errors to be human-readable;
 * Adding images parsing in read_rss();
 * Updating parsing in read_rss() using find()


Add news caching
 * Adding optional argument `--date`
 * Separating logic of parsing rss feed and adding to database (get_articles()) and printing articles (print_articles())
 * Adding local storage using pickledb
 * Adding functions add_to_db, update_db, print_from_db, error if the news are not found
 * Updating date format for printing in stdout: '%a, %d %b %Y %X %z'
 * Adding info to README.md


