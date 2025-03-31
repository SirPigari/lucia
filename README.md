# Lucia 1.1

Lucia is a simple, lightweight, and fast programming language made in python.

___

## Currently working on:

- Fixing bugs
- Documentation
- Testing
- Adding more features
- Fixing issues with Objects

___

Documentation for Lucia 1.1 can be found [here](env/Docs/language-syntax.md).

## Installation

Follow the instructions in the [installation guide](env/Docs/installation-guide.md) to install Lucia.

## License

[GNU 3.0 LICENSE](LICENSE)


## Changelog:
### 1.1.1
- Added predefs:
  - Syntax:
    - `#predef <name> -> <value>`
    - Predefs:
      - `#alias` - Aliases a function or variable (example: `#alias function -> fun`)
      - `#del` - Deletes a alias defined before (example: `#del function`)
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