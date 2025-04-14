Guide to `config.json`
======================

The `config.json` file contains various configurable options that control the behavior and appearance of the Lucia programming environment. Below is a comprehensive guide explaining each setting in the [config.json](../config.json) file.

Location of `config.json`
-------------------------

The `config.json` file is located in the root directory of your Lucia environment. You can access and edit this file to adjust the settings to your preferences.

Structure of `config.json`
--------------------------

```json
{
  "moded": false,
  "debug": false,
  "debug_mode": "normal",
  "supports_color": true,
  "use_lucia_traceback": true,
  "warnings": true,
  "use_predefs": true,
  "print_comments": false,
  "lucia_file_extensions": [
    ".lucia",
    ".luc",
    ".lc",
    ".l"
  ],
  "home_dir": "C:\\Users\\sirpigari\\AppData\\Local\\Programs\\LuciaAPL\\env",
  "recursion_limit": 9999,
  "version": "1.1.2",
  "color_scheme": {
    "exception": "#F44350",
    "warning": "#FFC107",
    "debug": "#434343",
    "comment": "#757575",
    "input_arrows": "#136163",
    "input_text": "#BCBEC4",
    "output_text": "#BCBEC4",
    "info": "#9209B3"
  }
}
```

Configuration Options
---------------------

### 1\. `moded`

*   **Type:** `bool`
*   **Description:** Activates or deactivates mode functionality in Lucia. When set to `true`, the "mode" feature is enabled.
*   **Note:** If `moded` is `true`, the `activate` function cannot override it.

### 2\. `debug`

*   **Type:** `bool`
*   **Description:** Enables or disables the debugging mode. Set to `true` to turn on debugging.
*   **Note:** Enabling this will slow down the program due to the additional print statements. You can turn it on if performance is not a concern.

### 3\. `debug_mode`

*   **Type:** `string`
*   **Values:** `"full"`, `"normal"`, `"minimal"`
*   **Description:** Specifies the level of debug information to be provided:
    *   **full:** Provides tokens, AST, and interpreter information.
    *   **normal:** Provides only interpreter information.
    *   **minimal:** Provides only tokens and AST information.

### 4\. `supports_color`

*   **Type:** `bool`
*   **Description:** If `true`, Lucia will use ANSI escape codes to display color in the terminal for different output types (e.g., error, debug, info).

### 5\. `use_lucia_traceback`

*   **Type:** `bool`
*   **Description:** If `false`, Lucia will use the default Python traceback instead of the Lucia traceback format for errors.

### 6\. `warnings`

*   **Type:** `bool`
*   **Description:** If `false`, warnings will be disabled.

### 7\. `use_predefs`

*   **Type:** `bool`
*   **Description:** If `true`, predefs are enabled. Predefs are special functions, such as `#alias` and `#del`, which can override Lucia's default tokens (see the [language-syntax.md](language-syntax.md#predefs) file for more details).

### 8\. `print_comments`

*   **Type:** `bool`
*   **Description:** If `true`, comments will be printed during execution.

### 9\. `lucia_file_extensions`

*   **Type:** `array` of `string`
*   **Description:** Specifies the file extensions that Lucia will accept for code files. Default extensions include `.lucia`, `.luc`, `.lc`, and `.l`.

### 10\. `home_dir`

*   **Type:** `string`
*   **Description:** The directory where the Lucia environment is located. This path is used by the Lucia interpreter to find environment-specific resources.

### 11\. `recursion_limit`

*   **Type:** `int`
*   **Description:** Specifies the maximum depth of recursion allowed in Lucia programs. The default value is 9999.

### 12\. `version`

*   **Type:** `string`
*   **Description:** Specifies the current version of Lucia. This field should be updated with every new release of Lucia.

### 13\. `color_scheme`

*   **Type:** `object`
*   **Description:** Defines the color scheme used for various elements in the terminal. Each property within the `color_scheme` object corresponds to a different output type and specifies the color for that output.

*   `exception:` Color for exception messages.
*   `warning:` Color for warning messages.
*   `debug:` Color for debug output.
*   `comment:` Color for comments in the code.
*   `input_arrows:` Color for input prompt arrows.
*   `input_text:` Color for input text.
*   `output_text:` Color for output text.
*   `info:` Color for informational messages.