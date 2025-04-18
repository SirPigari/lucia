# Lucia 1.2.1

Lucia is a simple, lightweight, and fast programming language made in python.

___

## Currently working on:

- Fixing bugs
- Documentation
- Testing
- Adding more features

___

Documentation for Lucia 1.2 can be found [here](env/Docs/introduction.md).

## Installation

Follow the instructions in the [installation guide](env/Docs/installation-guide.md) to install Lucia.

## License

[GNU 3.0 LICENSE](LICENSE)


## Changelog:
### 1.2.1
- Changed the lucia logo, new logo: ![Lucia Logo](env/assets/lucia_logo_small.png)
- Fixed typos
- Fixed bugs:
  - Error when python function returned None, now it returns `null`
  - Fixed issues with REPL terminal mode
  - **IMPORTANT** Fixed `forget` statement
  - **IMPORTANT** Fixed problems with `or` and `and` operators
  - **IMPORTANT** Fixed issue with default values in function parameters
- Added function `getcwd` to `os` library
- Added functions to python library:
  - `pycall` - Calls a python function from a python file.
  - `pybool` - Converts a value to a boolean.
  - `pyversion` - Returns the python version.
- Fixed bugs with `random` library
- Added functions to `test` library:
  - `testIndex` - Tests indexes in lucia.
  - `testFunctionCalls` - Tests function calls in lucia.
  - `testLibs` - Tests libraries in lucia.
  - `testOperators` - Tests operators in lucia.
- Added [`update_version.py`](env/update_version.py)
### 1.2.0
- Added `flatten` function to `list` and `map` modules:
- Added `Exception` and `Warning` keywords:
  - `Exception` is used to create new exceptions.
  - `Warning` is used to create new warnings.
- Added `__type__` function to exceptions and warnings
- Fixed errors while importing modules
- Added more tests to `test` library
- Updated installer
- Added new operators:
  - `in` - Checks if a value is in a list or map.
  - `or` - Logical OR operator.
  - `and` - Logical AND operator.
  - `not` - Logical NOT operator.
  - `isnt` or `isn't` - Checks if two values are not equal.
  - `is` - Checks if two values are equal.
  - `xor` - Logical XOR operator.
  - `xnor` - Logical XNOR operator.
- Updated `lucia.py`
- Added error handling for missing `end` keyword
- Added `#config` predef
- Modified how try-catch works ([see here](env/Docs/language-syntax.md#try-and-catch))
### 1.1.2
- Fixed many bugs
- Added documentation
- Fixed installer
### 1.1.1
- Added predefs:
  - Syntax:
    - `#predef <name> -> <value>`
    - Predefs:
      - `#alias` - Aliases a function or variable (example: `#alias function -> fun`)
      - `#del` - Deletes an alias defined before (example: `#del function`)
- Added `test_all` function to `test` module.
- Fixed MANY bugs
- Added 'in' operator (`~`):
  - Syntax: `<value> ~ <list or map>`
  - Returns `true` if the value is in the list, `false` otherwise.
- Fixed float operations

---
### 1.1.0
- Added `try`-`catch` statements
- Added `console` library:
  - `overwrite`: Clears the current line in the terminal and prints new text.
  - `log`: Standard print function alias.
  - `supports_color`: Checks if the terminal supports colored output.
  - `debug`: Prints debug messages with configurable color.
  - `info`: Prints informational messages with configurable color.
  - `error`: Prints error messages with configurable color.
  - `fatal`: Prints fatal error messages with a darkened color.
  - `warn`: Prints warning messages with configurable color.
  - `progress_bar`: Displays a progress bar for an iterable.
  - `styled_print`: Prints styled text with foreground and background color options.
  - `clear`: Clears the terminal screen.
- Added more precision to floats
- Fixed bugs:
  - Fixed nested functions calls not working
  - Fixed issues with built-in functions calls
- Added built-in functions:
  - `wait` - waits for a certain amount of time in milliseconds
  - `declen` - returns the decimal length of a number
- Added `static` and `public` to variables
- Fixed issues with debugs
- Fixed issues with float operations
- Added operators:
  - `| number |` - returns the absolute value of a number
- Added debug logs to loops iterations
- Default precision for floats is now 28 but is set automatically