# NajaScript Syntax Summary

Based on our tests, here's a summary of the working syntax in NajaScript:

## Basic Types
- `int`: Integer values
- `float`: Floating-point values
- `string`: Text strings
- `bool`: Boolean values (true/false)

## Variable Declarations
```
int a = 10;
float b = 3.14;
string c = "Hello";
bool d = true;
var e = 42;  // Generic variable
```

## Basic Operations
```
// Arithmetic
int sum = a + b;
int difference = a - b;
int product = a * b;
float quotient = a / b;
int remainder = a % b;

// Logical
bool and_result = true && false;
bool or_result = true || false;

// Comparison
bool equal = a == b;
bool not_equal = a != b;
bool less_than = a < b;
bool greater_than = a > b;
bool less_than_equal = a <= b;
bool greater_than_equal = a >= b;
```

## Control Structures
### Conditionals
```
if (condition) {
    // code
} else if (another_condition) {
    // code
} else {
    // code
}
```

### Loops
```
// While loop
while (condition) {
    // code
}

// For loop
for (int i = 0; i < 10; i = i + 1) {
    // code
}
```

## Data Structures
### Lists
```
list numbers = [1, 2, 3, 4, 5];
numbers.add(6);
numbers.length();
numbers.get(2);  // Get element at index 2
```

### Dictionaries
```
dict person = {};
person.add("name", "Maria");
person.add("age", 30);
person.get("name");
```

## Functions
```
fun add(int a, int b) {
    return a + b;
}

fun greet(string name) {
    return "Hello, " + name + "!";
}
```

## Classes (Basic)
```
class Test {
    constructor() {
        println("Constructor called");
    }
    
    public void sayHello() {
        println("Hello from Test class");
    }
}

var obj = new Test();
obj.sayHello();
```

## Input/Output
```
println("Output text");
string input = input("Prompt: ");
```

## Notes
- Property declarations in classes don't seem to work correctly with the parser
- The NOT operator (`!`) syntax is not fully working in our tests
- Power operator (`^`) is not supported

This summary represents the working syntax elements we were able to confirm through our testing. 