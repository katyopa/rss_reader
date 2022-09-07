<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<h3 align="center">RSS Reader</h3>

  <p align="center">
        <br />
    <a href="https://github.com/katyopa/rss_reader"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>

  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


RSS reader is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable format.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/katyopa/rss_reader.git
   ```
2. Install package
   ```sh
   pip install
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Example of how a project can be used. 



Utility provides the following interface:

```shell
usage: rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [source]

This utility reads RSS feed & outputs to console

positional arguments:
  source         RSS URL

options:
  -h, --help     show this help message and exit
  --version      print version info
  --json         print result as JSON in stdout
  --verbose      output verbose status messages in stdout
  --limit LIMIT  limit news topics if this parameter provided
  --date DATE    print out the news from the specified day

```

###Optional arguments:

1. `--limit` option limits news topics if this parameter provided.

If `--limit` is not specified, then user gets _all_ available feed.

If `--limit` is larger than feed size then user should get _all_ available news.

```shell
>  python rss_reader.py 'https://news.yahoo.com/rss/'  --limit 1 

Feed: Yahoo News - Latest News & Headlines

Title: Palin urges Begich to drop House bid; Begich declines
Date: Mon, 05 Sep 2022 22:27:25 +0100
Image: https://s.yimg.com/uu/api/res/1.2/ZIeYNDAOshMjxXqdLwPegQ--~B/aD0zNDU2O3c9NTE4NDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/b5988684794bdc393ab87a3794bef1bb
Link: https://news.yahoo.com/palin-urges-begich-drop-house-222725117.html
------------------------
```

2. `--json` argument converts the news into [JSON](https://en.wikipedia.org/wiki/JSON) format and prints the result in stdout.

`--limit` argument also affects JSON generation.
```shell
> python rss_reader.py 'https://news.yahoo.com/rss/'  --limit 1 --json

Feed: Yahoo News - Latest News & Headlines

Title: Palin urges Begich to drop House bid; Begich declines
Date: Mon, 05 Sep 2022 22:27:25 +0100
Image: https://s.yimg.com/uu/api/res/1.2/ZIeYNDAOshMjxXqdLwPegQ--~B/aD0zNDU2O3c9NTE4NDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/b5988684794bdc393ab87a3794bef1bb
Link: https://news.yahoo.com/palin-urges-begich-drop-house-222725117.html
------------------------

[
  {
    "Title": "Palin urges Begich to drop House bid; Begich declines",
    "Date": "Mon, 05 Sep 2022 22:27:25 +0100",
    "Image": "https://s.yimg.com/uu/api/res/1.2/ZIeYNDAOshMjxXqdLwPegQ--~B/aD0zNDU2O3c9NTE4NDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/b5988684794bdc393ab87a3794bef1bb",
    "Link": "https://news.yahoo.com/palin-urges-begich-drop-house-222725117.html"
  }
]
```

3.  `--verbose` argument prints all logs in stdout.
```shell
> python rss_reader.py 'https://news.yahoo.com/rss/'  --limit 1 --json --verbose
[2022-09-06 13:47:14,856: DEBUG] Starting rss reader...
[2022-09-06 13:47:15,175: DEBUG] Loading news from https://news.yahoo.com/rss/...
[2022-09-06 13:47:15,185: DEBUG] Processing result...


Feed: Yahoo News - Latest News & Headlines

Title: Palin urges Begich to drop House bid; Begich declines
Date: Mon, 05 Sep 2022 22:27:25 +0100
Image: https://s.yimg.com/uu/api/res/1.2/ZIeYNDAOshMjxXqdLwPegQ--~B/aD0zNDU2O3c9NTE4NDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/b5988684794bdc393ab87a3794bef1bb
Link: https://news.yahoo.com/palin-urges-begich-drop-house-222725117.html
------------------------

[2022-09-06 13:47:15,188: DEBUG] Printing news in JSON format...

[
  {
    "Title": "Palin urges Begich to drop House bid; Begich declines",
    "Date": "Mon, 05 Sep 2022 22:27:25 +0100",
    "Image": "https://s.yimg.com/uu/api/res/1.2/ZIeYNDAOshMjxXqdLwPegQ--~B/aD0zNDU2O3c9NTE4NDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/b5988684794bdc393ab87a3794bef1bb",
    "Link": "https://news.yahoo.com/palin-urges-begich-drop-house-222725117.html"
  }
]
[2022-09-06 13:47:15,188: DEBUG] Exiting the program.
```

4. `--date` argument means actual *publishing date*.

It takes a date in `%Y%m%d` format. The cashed news can be read with it. 

The news from the specified day will be printed out.

If the news are not found an error is shown.

`--date` works with both `--json`, `--limit`, `--verbose` and their different combinations.

```shell
> python rss_reader.py 'https://news.yahoo.com/rss/'  --limit 1 --json --verbose --date 20220905
[2022-09-06 14:10:51,082: DEBUG] Printing the news from 20220905...

[2022-09-06 14:10:51,083: DEBUG] Starting rss reader...
[2022-09-06 14:10:51,382: DEBUG] Loading news from https://news.yahoo.com/rss/...

Feed: Yahoo News - Latest News & Headlines

Title: 'Flip or Flop's' Christina Hall wore a sheer, form-fitting dress covered in flowers to marry Josh Hall
Date: Mon, 05 Sep 2022 16:17:09 +0100
Image: https://s.yimg.com/uu/api/res/1.2/SiVL1FgDDDL3H1e.uCeJqg--~B/aD05MDA7dz0xMjAwO2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/insider_articles_922/c4a2b0adeef642f6d08e524fa91f7a7f
Link: https://news.yahoo.com/flip-flops-christina-hall-wore-161709762.html
------------------------

[2022-09-06 14:10:51,394: DEBUG] Printing news in JSON format...

[
  {
    "Title": "'Flip or Flop's' Christina Hall wore a sheer, form-fitting dress covered in flowers to marry Josh Hall",
    "Date": "Mon, 05 Sep 2022 16:17:09 +0100",
    "Image": "https://s.yimg.com/uu/api/res/1.2/SiVL1FgDDDL3H1e.uCeJqg--~B/aD05MDA7dz0xMjAwO2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/insider_articles_922/c4a2b0adeef642f6d08e524fa91
f7a7f",
    "Link": "https://news.yahoo.com/flip-flops-christina-hall-wore-161709762.html"
  }
]
[2022-09-06 14:10:51,395: DEBUG] Exiting the program.
```

`--date` does **not** require internet connection to fetch news from local cache.

User is able to use `--date` without specifying RSS source.
```
> python rss_reader.py --date 20191206
......
```
Or when installed using setuptools:
```
> rss_reader --date 20191206
......
```

5. If `--version` option is specified app _just prints its version_ and stops.

User is able to use `--version` option without specifying RSS URL.
```
> python rss_reader.py  --version                                                               
1.1
```

6. -h, --help  argument shows the help message and exits.


###Distribution
* Utility is wrapped into distribution package with `setuptools`.
* This package exports CLI utility named `rss-reader`.


User is able to run the application _both_ with and without installation of CLI utility,
meaning that this should work:

```
> python rss_reader.py ...
```

as well as this:  

```
> rss_reader ...
```

###News caching
The RSS news is stored in a local storage while reading. 

```pickledb``` module is used for storing the news.
The cashed news can be read with ```--date``` argument.


###Format converter

The conversion of news in at least two of the suggested format: `.mobi`, `.epub`, `.fb2`, `.html`, `.pdf`

New optional argument must be added to your utility. This argument receives the path where new file will be saved. The arguments should represents which format will be generated.

For example:  `--to-mobi` or `--to-fb2` or `--to-epub`

You can choose yourself the way in which the news will be displayed, but the final text result should contain pictures and links, if they exist in the original article and if the  format permits to store this type of data.



###Known issues:



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Katia Lastouskaya - katyopa@yandex.ru

Project Link: [https://github.com/katyopa/rss_reader](https://github.com/katyopa/rss_reader)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Python.org]: https://www.python.org/static/community_logos/python-powered-w-100x40.png
[Python-url]: https://python.org/

