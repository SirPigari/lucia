Lucia Language Syntax
=====================

Content
---------------

- [Getting Started](#getting-started)
  - [1\. Install Lucia](#1-install-lucia)
  - [2\. Create a "Hello, World!" Program](#2-create-a-hello-world-program)
  - [3\. Run the Program](#3-run-the-program)
- [Variables & Data Types](#variables--data-types)
  - [Supported Data Types:](#supported-data-types)
  - [F-Strings](#f-strings)
    - [Basic Usage](#basic-usage)
    - [Including Expressions](#including-expressions)
  - [Operators](#operators)
    - [Arithmetic Operators](#arithmetic-operators)
    - [Comparison Operators](#comparison-operators)
    - [Logical Operators](#logical-operators)
    - [Assignment Operators](#assignment-operators)
    - [Supported Operators](#supported-operators)
- [Blocks in Lucia](#blocks-in-lucia)
  - [Block Syntax](#block-syntax)
  - [Example of a Block](#example-of-a-block)
  - [Why Use Blocks?](#why-use-blocks)
- [Indentation](#indentation)
  - [Example](#example)
  - [Summary](#summary)
- [Control Flow](#control-flow)
  - [If Statements](#if-statements)
    - [Basic example](#basic-example)
    - [Example breakdown](#example-breakdown)
  - [Functions](#functions)
    - [Basic Function Declaration](#basic-function-declaration)
    - [Modifiers](#modifiers)
    - [Using Modifiers](#using-modifiers)
    - [Empty Functions](#empty-functions)
    - [Example Function with Default Parameters](#example-function-with-default-parameters)
    - [Calling Functions](#calling-functions)
  - [Loops](#loops)
    - [For Loop](#for-loop)
    - [List Patterns](#list-patterns)
    - [While Loop](#while-loop)
- [Error Handling](#error-handling)
  - [Function with Error Throwing](#function-with-error-throwing)
  - [Try and Catch](#try-and-catch)
  - [Default Error Type](#default-error-type)
  - [Defining a new Exception](#defining-a-new-exception)
  - [Defining a new Warning](#defining-a-new-warning)
- [Comments](#comments)
  - [Single-line Comment](#single-line-comment)
  - [Multi-line Comment](#multi-line-comment)
  - [In-line Comment](#in-line-comment)
- [Basic Input/Output](#basic-inputoutput)
  - [Output](#output)
  - [Input](#input)
- [Other Statements](#other-statements)
  - [Import](#import)
  - [With](#with)
  - [Forget](#forget)
  - [Objects](#objects)
    - [Object Declaration](#object-declaration)
    - [Object Usage](#object-usage)
    - [Property](#property)
- [Predefs](#predefs)
  - [Predef Types](#predef-types)
    - [1\. #alias](#1-alias)
    - [2\. #del](#2-del)
    - [3\. #config](#3-config)
- [Code Blocks](#code-blocks)
  - [Syntax](#syntax)
    - [C Example](#c-example)
    - [ASM Example](#asm-example)
    - [Python Example](#python-example)
  - [Exporting Variables from C Blocks](#exporting-variables-from-c-blocks)
  - [Export Functions](#export-functions)
- [Conclusion](#conclusion)


Getting Started
---------------

To write your first program in Lucia, follow the steps below:

### 1\. Install Lucia

First, you need to install the Lucia language. Follow the [installation guide](installation-guide.md) to set it up on your system.

You can also customize your Lucia preferences by modifying the [config.json](../config.json) file. For details on how to configure the file, refer to the [Guide to `config.json`](config-guide.md).

### 2\. Create a "Hello, World!" Program

Create a new file named `hello.lucia` and write the following code:

```lucia
print("Hello, World!")
```

### 3\. Run the Program

Once the program is saved, you can run it by executing the following command in your terminal:

```bash
lucia hello.lucia
```

Output:

```
Hello, World!
```

Variables & Data Types
----------------------

In Lucia, variables are declared using a type annotation followed by the `=` assignment operator. Here's how you define variables and assign values:

```lucia
x: int = 10                                 // Integer
name: str = "Lucia"                         // String
pi: float = 3.14                            // Float
isActive: bool = true                       // Boolean
result: void = null                         // Void (no value)
data: any = "This can be anything"          // Any type
numbers: list = [1, 2, 3, 4]                // List
person: map = {"name": "Lucia", "age": 20}  // Map
```

### Supported Data Types:

*   **int**: Whole numbers (e.g., 10, -5).
*   **str**: Text values (e.g., "Hello, World!").
*   **bool**: Logical values (`true`, `false` or `null`).
*   **void**: Represents the absence of a value (`null`).
*   **float**: Decimal numbers (e.g., 3.14, -0.001). The default precision for floating-point numbers is 28 decimal places.
*   **any**: A type that can hold any value (e.g., can be a string, number, list, etc.).
*   **list**: Ordered collection of values (e.g., `[1, 2, 3]`).
*   **map**: Key-value pairs (e.g., `{"name": "Lucia", "age": 25}`).

## F-Strings
Lucia supports f-strings for string interpolation, allowing you to embed variables or expressions directly within strings using curly braces `{}`.

### Basic Usage
```lucia
name: str = "Lucia"
version: str = "1.3"
greeting: str = f"Hello, {name}! Welcome to Lucia version {version}."
print(greeting)
// Output: Hello, Lucia! Welcome to Lucia version 1.2.1.

```

### Including Expressions
You can also include expressions inside f-strings:

```lucia
x: int = 5
y: int = 10
result: str = f"The sum of {x} and {y} is {x + y}."
print(result)
// Output: The sum of 5 and 10 is 15.
```

Operators
---------

Lucia supports a variety of operators that can be used for arithmetic, comparison, logical operations, and more. Below are the categories of supported operators:

### Arithmetic Operators

Lucia supports the basic arithmetic operators for mathematical calculations:

```lucia
x: int = 10 + 5             // 15
product: int = 4 * 2        // 8
division: float = 10 / 2    // 5
exponent: float = 2 ^ 3     // 8
remainder: int = 10 % 3     // 1
```

### Comparison Operators

These operators allow you to compare two values:

```lucia
isEqual: bool = (5 == 5)            // true
isGreater: bool = (10 > 3)          // true
isLessThan: bool = (5 < 10)         // true
isGreaterOrEqual: bool = (5 >= 5)   // true
isNotEqual: bool = (5 != 3)         // true
```

### Logical Operators

Logical operators are used to perform logical operations:

```lucia
isTrue: bool = (true && false)          // false
isNotTrue: bool = !true                 // false
isEitherTrue: bool = (true || false)    // true
isMember: bool = (3 ~ [1, 2, 3])        // true
```

### Assignment Operators

Lucia also supports shorthand assignment operators for modifying variable values:

```lucia
x: int = 10  // x = 10
x += 5       // x = 15
x -= 3       // x = 12
x *= 2       // x = 24
x /= 4       // x = 6
```

### Supported Operators

In addition to the standard arithmetic, comparison, and logical operators, Lucia includes several other operators:

*   `+`: Addition
*   `-`: Subtraction
*   `*`: Multiplication
*   `/`: Division
*   `^`: Exponentiation
*   `%`: Modulo (remainder of division)
*   `==`: Equality comparison
*   `>`: Greater than
*   `<`: Less than
*   `>=`: Greater than or equal to
*   `<=`: Less than or equal to
*   `!=`: Not equal to
*   `&&`: Logical AND
*   `||`: Logical OR
*   `!`: Logical NOT
*   `~`: In operator (checks if left value exists in a list or map)
*   `+=`: Add and assign
*   `-=`: Subtract and assign
*   `*=`: Multiply and assign
*   `/=`: Divide and assign
*   `abs`: Absolute value, used as `|x|`

Blocks in Lucia
---------------

In Lucia, blocks of code are used to group statements together. This can be seen in control structures like `if` statements, loops, functions, and more. Lucia uses the `end` keyword to mark the end of a block, which is similar to using braces in C or indentation in Python.

### Block Syntax

Blocks in Lucia start with a statement that is followed by a `:`, and the body of the block is indented (optional, but recommended for readability). The block is terminated using the `end` keyword.

### Example of a Block

Here’s an example of a block used with an `if` statement:

```lucia
age: int = 18

if (age >= 18):
    print("You are an adult.")
end
```

The code within the block (in this case, the `print()` function) is indented, and the block is terminated with `end`.

### Why Use Blocks?

Blocks help organize code into logical groups. By using the `end` keyword, Lucia ensures that the boundaries of each block are clearly defined, which reduces errors and improves readability.

Indentation
-----------

Unlike Python, Lucia does not rely on indentation to define blocks. Blocks are explicitly marked using the `:` after a statement and are terminated with the `end` keyword. While indentation is not required, it is recommended for better readability.

### Example

Both of the following examples are valid in Lucia:

```lucia
age: int = 18

if (age >= 18):
    print("You are an adult.")  
end
```

```lucia
age: int = 18

if (age >= 18): 
print("You are an adult.")  
end
```

Since blocks in Lucia are clearly defined by `:` and `end`, indentation does not affect how the code runs. However, using consistent indentation is recommended to improve readability.
### Summary

*   A block in Lucia is created by using a statement followed by a colon (`:`) and indented code.
*   Blocks are terminated with the `end` keyword.
*   Indentation is important in Lucia, and the code inside a block must be consistently indented.
*   Blocks improve code organization and readability, ensuring that related code is grouped together.

Control Flow
------------


If Statements
-------------

Control the flow of your program using `if` statements. An `if` statement evaluates a condition and executes the code block based on whether the condition is true or false.

### Basic Example

Here’s an example of how an `if` statement works in Lucia:

```lucia
age: int = 18

if (age >= 18):
    print("You are an adult.")
end

if (age == 69):
    print("Nice!")
end else:
    print("You are not 69.")
end
```

### Example Breakdown

In the above example:

*   The condition `if (age >= 18):` checks if the `age` variable is greater than or equal to 18.
*   If the condition is true, the block under the `if` statement is executed, printing "You are an adult."
*   If the condition `age == 69` is true, it prints "Nice!". If not, the `else` block is executed, printing "You are not 69."

Functions
---------

In Lucia, functions are defined using the `fun` keyword, but if any modifiers are used, the `fun` keyword is not required.

### Basic Function Declaration

A function can be defined with parameters and an optional return type:

```lucia
fun add(a: int, b: int) -> int:
    return a + b
end
```

### Modifiers

Functions can have different modifiers that change their behavior:

*   `public` – The function is accessible from other modules (default).
*   `private` – The function is only accessible within the same module.
*   `static` – The function belongs to the class itself rather than an instance.
*   `non-static` – The function belongs to an instance of the class (default behavior).
*   `final` – The function cannot be redefined later.
*   `mutable` – Explicitly states that the function can be redefined (default behavior).

By default, every function is `public non-static mutable`.

### Using Modifiers

When using modifiers, the `fun` keyword is not required:

```lucia
public non-static final main() -> int:
    return 0
end
```

The above function is equivalent to:

```lucia
fun main() -> int:
    return 0
end
```

### Empty Functions

If a function has no body, the colon `:` is not required:

```lucia
fun main() -> void end
```

However, if the function has a body, the colon must be included:

```lucia
fun main() -> void:
    print("Hello, World!")
end
```

### Example Function with Default Parameters

Functions can have default parameter values:

```lucia
public static final fun name(arg1, arg2: int, arg3 = 10, arg4: int = 10) -> int:
    return 0
end
```
### Calling Functions

To call a function, use the function name followed by parentheses and any required arguments:

```lucia
result: int = add(5, 10)
```

To call a function with a named parameter, use the parameter name followed by a `=` and the value:

```lucia
result: int = add(b = 10, a = 5)
```

Loops
-----

### For Loop

Lucia provides a `for` loop for iterating over lists. A valid range must be enclosed in parentheses:

```lucia
for (i in [1...10]):
    print(i)  // Output: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
end
```

### List Patterns

Lucia allows pattern-based list generation inside ranges:

```lucia
[1, 3, 5...101]     // Generates: [1, 3, 5, 7, ..., 101]
[0, 2, 4, 6...100]  // Generates: [0, 2, 4, 6, ..., 100]
```

If the pattern is not recognized, a `ListPatternRecognitionWarning` is raised, and the list remains unchanged:

```lucia
[1, 2, 6...14]      // Warning: Unrecognized pattern, returns [1, 2, 6, 14]
```

### While Loop

Lucia also supports a `while` loop:

```lucia
while (count < max):
    print(count)
    count += 1
end
```

Error Handling
--------------

Lucia handles errors using `try` and `catch` blocks. Functions can throw errors using the `throw` keyword, and you can specify an error type if needed.

### Function with Error Throwing

In Lucia, errors can be thrown using `throw` and caught with `try` and `catch`:

```lucia
fun divide(a: int, b: int) -> int:
    if (b == 0):
        throw "Cannot divide by zero!" from ZeroDivisionError
    end
    return a / b
end
```

### Try and Catch

The `try` block is used to attempt the operation that might throw an error, and the `catch` block handles the error:

```lucia
try:
    result = divide(10, 0)
end catch (e):
    print("Error: ", e)
end
```

Also, you don't need to use the `catch` block if you don't want to handle the error:

```lucia
try:
    result = divide(10, 0)
end
```

### Default Error Type

If no specific error type is mentioned, Lucia will raise an error from `LuciaException` by default:

```lucia
fun divide(a: int, b: int) -> int:
    if (b == 0):
        throw "Cannot divide by zero!"
    end
    return a / b
end
```

In the example above, if `throw` is used without a specified error type, the system will raise a `LuciaException` by default.

### Defining a new Exception

You can define a new exception type by using the `Exception` keyword:

```lucia
Exception CustomError
throw "Error message" from CustomError
```

### Defining a new Warning

You can define a new warning type by using the `Warning` keyword:

```lucia
Warning CustomWarning
throw "Warning message" from CustomWarning
```


Comments
--------

Lucia supports single-line and multi-line comments:

### Single-line Comment

```lucia
// This is a single-line comment
```

### Multi-line Comment

```lucia
/*
This is a multi-line comment
spanning multiple lines.
*/
```

### In-line Comment

The in-line comment is used to add comments inside the code.
It's defined by <# and #>:

```lucia
print("Hello world" <# This is an in-line comment #>)
```

Basic Input/Output
------------------

### Output

Use the `print()` function to display output:

```lucia
print("Hello, Lucia!")  // Output: Hello, Lucia!
```

### Input

Use the `input()` function to get user input:

```lucia
name: str = input("Enter your name: ")
print("Hello, ", name, "!")  // Output: Hello, [name]!
```

Other Statements
----------------

### Import

Lucia allows flexible importing of modules. The `import` statement can use modifiers such as `as` and `from`, and they can appear in any order or be omitted entirely:

```lucia
import math                 // imports math module
import math as m            // imports math module and renames it as 'm'
import math from "math/"    // imports math from the specified directory
```

The modifiers `as` and `from` can be stacked in any order or omitted:

```lucia
import math
import math as m
import math from "math/"
import math from "math/" as m
```

### With

The `with` statement is used for context management:

```lucia
with (TestContext()) as tc:
end
```

```lucia
with (File()) as f:
    print(f.open("test.txt"))
end
```

### Forget

The `forget` statement removes a variable from memory:

```lucia
i: int = 10
forget i
```

After using `forget`, the variable `i` is no longer available:

```lucia
i: any = "str"
```

Objects
-------

### Object Declaration

In Lucia, objects can be declared using the `object` keyword. Here's an example:

```lucia
object O:
    init():
        i: int = 10
    end
    
    fun main() -> void: 
        print(i)
    end
end
```

### Object Usage

Once declared, you can create an instance of an object and call its methods:

```lucia
o = O()
o.main()
```

### Property

A property is any variable, function, or object that is called inside another. For example, `math.pi` is a variable property of the `math` module.

Predefs
----------------

Predefs are special commands in Lucia that allow you to modify or define certain tokens before they are sent to the interpreter. They are processed during the pre-interpretation phase of your code. All predefs start with the # symbol.

### Predef Types
#### 1\. `#alias`
The `#alias` predef allows you to create an alias, which means defining the first argument to be equivalent to the second argument.

*Example:*

```lucia
#alias true -> false
```

This command makes `true` behave as `false` throughout the code. After this alias, any reference to `true` will be treated as `false`.

#### 2\. `#del`
The `#del` predef removes an alias that has been previously defined with `#alias`. It restores the original meaning of the token.

*Example:*

```lucia
#del true
```

This command removes the alias for `true`, making it behave as it originally did, i.e., `true` again.

#### 3\. `#config`
The `#config` predef allows you to modify the configuration of the interpreter. It can be used to set various options or preferences.
*Example:*

```lucia
#config debug = true
```

Can be reset to default by:

```lucia
#config debug reset
```

This command sets the debug mode to true, enabling additional debugging features in the interpreter.
It's the same as using the [`config.json`](../config.json) file. (See [Config guide](config-guide.md))

--------------

You can use predefs to modify the behavior of built-in tokens and tailor the language to your specific needs before the interpreter executes your code.

# Code Blocks

Lucia supports **code blocks**, which allow you to execute code written in other languages directly within Lucia scripts. Supported languages include:

- **C**
- **ASM**
- **Python**

> **Configuration Requirement**  
> Code blocks require the `execute_code_blocks` option to be set to `true` in your [`config.json`](../config.json) file:
>  ```
>  {
>    ...
>    "execute_code_blocks": {
>      "C": true,
>      "ASM": true,
>      "PY": true
>    },
>    ...
>  }
> ```

---

## Syntax

Code blocks are written using a language prefix followed by an `end` keyword to mark the end of the block.

### C Example

```lucia
C:
    #include <stdio.h>
    int main() {
        printf("Hello, World!");
        return 0;
    }
end
```

### ASM Example

```lucia
ASM:
    mov eax, 1
    mov ebx, 0
    int 0x80
end
```

### Python Example

```lucia
PY:
    print("Hello, World!")
end
```

---

## Exporting Variables from C Blocks

To retrieve values from C code, use the **export functions** provided by the [`export.h`](../Lib/C/include/export.h) library. This library is automatically included when executing C code blocks.

### Example: Exporting an Integer

```lucia
C:
    #include <stdio.h>
    int main() {
        int a = 10;
        export_int("a", a);
        export_flush();
        return 0;
    }
end

print(a)  // Output: 10
```

### Export Functions

| Function                                  | Description                         |
|-------------------------------------------|-------------------------------------|
| `export_int(name: str, value: int)`       | Export an integer variable.         |
| `export_float(name: str, value: float)`   | Export a float variable.            |
| `export_double(name: str, value: double)` | Export a double variable.           |
| `export_str(name: str, value: str)`       | Export a string variable.           |
| `export_bool(name: str, value: bool)`     | Export a boolean variable.          |
| `export_list(...)`                        | Export a list.                      |
| `export_map(...)`                         | Export a map.                       |
| `export_flush()`                          | Save exports to `export.json`.      |
| `export_clear()`                          | Clear all previously exported data. |


-----------


# Conclusion
Lucia is a straightforward language designed for ease of use and flexibility. You’ve covered essential topics like variable declaration, control flow, functions, error handling, and objects. The syntax promotes clarity, and the use of blocks and indentation improves code organization.

To move forward, continue practicing with more complex projects, experiment with its features, and explore how to structure programs using Lucia’s modular capabilities. (See [Examples](examples))

Happy coding with Lucia.