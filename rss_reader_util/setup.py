from setuptools import setup, find_packages
import pathlib
import rss_reader.version as ver
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.txt").read_text(encoding="utf-8")

setup(name='rss_reader',
      version=ver.__version__,
      description="One-shot command-line RSS reader",
      long_description=long_description,
      packages=find_packages(),
      entry_points={
                  "console_scripts": [
                  "rss_reader = rss_reader.rss_reader:main", #название для консоли,после двоеточия название ф-ции (main)
        ]
      },
      install_requires=[
                         "bs4 == 0.0.1",
                         "requests == 2.28.1",
                         "lxml == 4.9.1",
                         "pickledb == 0.9.2",             # чтобы устанавливало автоматически нужные пакеты
                         "json2html == 1.3.0",
                         "pdfkit == 1.0.0",
                         "wkhtmltopdf == 0.2"   # проверить, надо ли

                   ]
      )
