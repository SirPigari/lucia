# Lucia 1.3.1

Lucia is a simple and lightweight programming language made in python.

## Switching to Rust
Check out [SirPigari/lucia-rust](https://github.com/SirPigari/lucia-rust)

___

## Currently working on:

- Converting the entire codebase to <a href="https://www.rust-lang.org/" target="_blank">Rust</a>... god what have I done this is gonna take forever
- At least its gonna be **BLAZINGLY FAST**
- And rust is a <a href="https://www.reddit.com/r/feminineboys/comments/j91rv7/comment/g8gk0fy/?context=3" target="_blank">femboy lang</a>
---

Documentation for Lucia 1.3.1 can be found [here](env/Docs/introduction.md).  
About [versioning](env/Docs/versioning.md)

## Installation

Follow the instructions in the [installation guide](env/Docs/installation-guide.md) to install Lucia.

## License

[GNU 3.0 LICENSE](LICENSE)


## Changelog:
### 1.3.1
- Updated [CREDITS.md](env/CREDITS.md)
- Added `fetch` function to builtins
- Added `requests` library
- Added `time` library
- Added `goldenRatio` variable to `math` library
- Updated [config.json](env/config.json) (see [here](env/Docs/config-guide.md#9-allow_fetch) and [here](env/Docs/config-guide.md#10-execute_code_blocks))
- Updated [fibonacci.lc](env/Docs/examples/fibonnaci.lc) example to use Binet's formula
- Added [requestsExample.lc](env/Docs/examples/requestsExample.lc) example
- Updated testSuiteVersion to 0.0.3b
- Fixed typos
- Added `flattenToList` function to `map` type
- Added `finilize` built-in function to finalize a function (`mutable` -> `final`)
- Fixed bugs:
  - Issues with `config` library
  - Issues with [activate.py](env/activate.py) file
  - Issues with REPL terminal mode
  - Many bugs in [pparser.py](pparser.py)
  - Issues with importing modules (again)
- Added `__json__` method to built-in types
- Fixed skill issue on `print` function
- Added `expect` function to built-ins
- Removed unused `exports.json` file
- Added support for `_` variable in REPL mode (last result)
- Updated [LuciaInstaller.nsi](installer/LuciaInstaller.nsi) file
### 1.3.0
- Added `f-strings`
- Added `code blocks`, see [here](env/Docs/language-syntax.md#code-blocks)
- Fixed `help` function
- Minor changes to some error messages
- Added C library (system lib, cannot be imported)
- Updated `test` library for more tests
- Included TCC in [`env/bin/tcc/`](env/bin/tcc)
- Added more options to installer
- Added `setprec` built-in function to set the precision of floats
- Added `getprec` built-in function to get the precision of floats
- Fixed minor bugs and issues
- Added minor updates, I don't remember them myself
- Modified `lexer.py` to include `WHITESPACE` token and then be removed in `pparser.py`
- Variables now cannot be named one of these: ASM, C, PY
- Added support for single-quote strings (`'`)
### 1.2.1
- Changed the lucia logo, new logo: ![Lucia Logo](env/assets/lucia_logo_small.png "Lucia Logo")
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
- Added [`update_version.py`](env/helpers/update_version.py)
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
