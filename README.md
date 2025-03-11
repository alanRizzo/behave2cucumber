# Pepyno 🥒

<!-- Pytest Coverage Comment:Begin -->
<a href="https://github.com/alanRizzo/behave2cucumber/blob/main/README.md"><img alt="Coverage" src="https://img.shields.io/badge/Coverage-88%25-green.svg" /></a><details><summary>Coverage Report </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td colspan="5"><b>src/pepyno</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/cli.py">cli.py</a></td><td>37</td><td>2</td><td>95%</td><td><a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/cli.py#L84">84</a>, <a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/cli.py#L97">97</a></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/converter.py">converter.py</a></td><td>57</td><td>11</td><td>81%</td><td><a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/converter.py#L50">50</a>, <a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/converter.py#L58-L65">58&ndash;65</a>, <a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/converter.py#L82-L84">82&ndash;84</a>, <a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/converter.py#L101">101</a></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/tools.py">tools.py</a></td><td>42</td><td>5</td><td>88%</td><td><a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/tools.py#L40-L41">40&ndash;41</a>, <a href="https://github.com/alanRizzo/behave2cucumber/blob/main/src/pepyno/tools.py#L73-L75">73&ndash;75</a></td></tr><tr><td><b>TOTAL</b></td><td><b>156</b></td><td><b>18</b></td><td><b>88%</b></td><td>&nbsp;</td></tr></tbody></table></details>
<!-- Pytest Coverage Comment:End -->

pepyno is a tool designed to resolve the incompatibility between Behave's generated JSON reports and tools that require Cucumber JSON reports. It efficiently reformats Behave JSON into a Cucumber-compatible format.

This modified version has been adapted for improved compatibility with modern Python versions and includes enhancements for easier integration and usability. The original script was developed by Behalf Inc.'s automation team and was tested on Python 2.7. This version has been updated to support Python 3.x.


## Installation
For easy installation, use the following command:

```bash
pip install pepyno
```

## Running
Run these command to get some help:

```bash
pepyno --help
```

## Development
The build.sh script is used to automate common development tasks.

```bash
./build.sh
```
This will set up your development environment and check the status of your code.


## License
This project is licensed under the MIT License. The original software was created by Behalf Inc. and is provided "as is," without warranty of any kind. This modified version retains the original MIT License and attribution.

For more details, see the included `LICENSE` file.
