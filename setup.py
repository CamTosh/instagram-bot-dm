from setuptools import find_packages, setup
from io import open
import os
import re

_version_re = re.compile(r"__version__\s=\s'(.*)'")

install_requires = ['webdriver_manager', 'selenium']
with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "__about__.py"), 'r') as f:
    version = _version_re.search(f.read()).group(1)

setup(
    name="instadm",
    version=version,
    author="Toche Camille",
    author_email="tochecamille@gmail.com",
    url="https://github.com/CamTosh/instagram-bot-dm",
    description="Instagram bot to send direct messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "docs"]),
    zip_safe=False,
    license="GPLv3",
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
)
