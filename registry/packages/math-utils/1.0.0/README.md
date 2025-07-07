# Math Utils Library

A comprehensive mathematical utilities library for NajaScript providing advanced mathematical functions and operations in English.

## Installation

```bash
python naja_pkg install math-utils
```

## Quick Start

```naja
// Import specific functions you need
import { pi, sqrt, abs, factorial } from "math-utils";

fun main() {
    // Use mathematical constants
    float circleArea = pi() * pow(5.0, 2);
    println("Circle area: " + circleArea);
    
    // Calculate square root
    float result = sqrt(16.0);
    println("Square root of 16: " + result);
    
    // Get absolute value
    float absValue = abs(-10.5);
    println("Absolute value: " + absValue);
    
    // Calculate factorial
    int fact = factorial(5);
    println("5! = " + fact);
}

main();
```

## Available Functions (24 total)

### Mathematical Constants
- `pi()` - Returns π (3.14159...)
- `e()` - Returns Euler's number (2.71828...)
- `phi()` - Returns golden ratio (1.61803...)

### Basic Functions
- `abs(num)` - Absolute value
- `max(a, b)` - Maximum of two numbers
- `min(a, b)` - Minimum of two numbers
- `pow(base, exp)` - Power function (base^exp)
- `sqrt(num)` - Square root using Newton's method

### Trigonometric Functions
- `sin(angle)` - Sine (angle in radians, Taylor series approximation)
- `cos(angle)` - Cosine (angle in radians)
- `tan(angle)` - Tangent (angle in radians)

### Conversion Functions
- `deg2rad(degrees)` - Convert degrees to radians
- `rad2deg(radians)` - Convert radians to degrees

### Rounding Functions
- `round(num, places)` - Round to specified decimal places
- `floor(num)` - Round down to nearest integer
- `ceil(num)` - Round up to nearest integer

### Special Functions
- `factorial(n)` - Factorial function (n!)
- `fibonacci(n)` - Fibonacci sequence value at position n
- `gcd(a, b)` - Greatest common divisor
- `lcm(a, b)` - Least common multiple
- `isPrime(num)` - Check if number is prime

### Statistical Functions
- `mean(numbers)` - Average of a list of numbers
- `sum(numbers)` - Sum of all numbers in a list

### Information
- `mathUtilsInfo()` - Get library metadata

## Usage Examples

### Circle Calculations
```naja
import { pi, pow } from "math-utils";

fun calculateCircle(radius) {
    float area = pi() * pow(radius, 2);
    float circumference = 2.0 * pi() * radius;
    
    println("Radius: " + radius);
    println("Area: " + area);
    println("Circumference: " + circumference);
}

calculateCircle(5.0);
```

### Distance Between Points
```naja
import { sqrt, pow } from "math-utils";

fun distance(x1, y1, x2, y2) {
    float dx = x2 - x1;
    float dy = y2 - y1;
    return sqrt(pow(dx, 2) + pow(dy, 2));
}

float dist = distance(1.0, 1.0, 4.0, 5.0);
println("Distance: " + dist); // Output: 5.0
```

### Prime Number Finder
```naja
import { isPrime } from "math-utils";

fun findPrimes(limit) {
    lista primes = [];
    int num = 2;
    
    while (num <= limit) {
        if (isPrime(num)) {
            primes.add(num);
        }
        num = num + 1;
    }
    
    return primes;
}

lista primes = findPrimes(30);
println("Primes up to 30: " + primes);
```

### Statistical Analysis
```naja
import { mean, sum, max, min } from "math-utils";

fun analyzeData(data) {
    println("Data: " + data);
    println("Mean: " + mean(data));
    println("Sum: " + sum(data));
    
    // Find max and min manually since we work with lists
    float maxVal = data.obter(0);
    float minVal = data.obter(0);
    int i = 1;
    while (i < data.length()) {
        maxVal = max(maxVal, data.obter(i));
        minVal = min(minVal, data.obter(i));
        i = i + 1;
    }
    
    println("Max: " + maxVal);
    println("Min: " + minVal);
}

analyzeData([1.0, 2.0, 3.0, 4.0, 5.0]);
```

### Trigonometry Example
```naja
import { sin, cos, tan, deg2rad, rad2deg } from "math-utils";

fun trigExample() {
    float angle = deg2rad(45.0); // Convert 45° to radians
    
    println("Angle: 45° = " + angle + " radians");
    println("sin(45°): " + sin(angle));
    println("cos(45°): " + cos(angle));
    println("tan(45°): " + tan(angle));
    
    float radians = 1.5707963267948966; // π/2
    println("π/2 radians = " + rad2deg(radians) + "°");
}

trigExample();
```

## Import Patterns

### Import specific functions (recommended)
```naja
import { pi, sqrt, abs } from "math-utils";
```

### Import all functions at once
```naja
import "math-utils";
// Then access via module name (if supported)
```

## Technical Details

- **Language**: English function names for international compatibility
- **Implementation**: Pure NajaScript with no external dependencies
- **Algorithms**: 
  - Square root: Newton's method (10 iterations)
  - Trigonometry: Taylor series approximation (8 terms)
  - Prime checking: Optimized trial division
  - Statistical functions: Efficient single-pass algorithms

## Requirements

- NajaScript 1.0.0 or higher
- No external dependencies

## Version History

### v1.0.0 (Current)
- Initial release
- 24 mathematical functions
- Complete test coverage
- English function names
- Comprehensive documentation

## License

MIT License

## Contributing

This library is part of the NajaScript ecosystem. To contribute:

1. Fork the [NajaScript/Naja](https://github.com/NajaScript/Naja) repository
2. Make your changes to the math-utils package
3. Test your changes thoroughly
4. Submit a Pull Request

## Support

- **Issues**: [GitHub Issues](https://github.com/NajaScript/Naja/issues)
- **Documentation**: [NajaScript Docs](https://najascript.github.io)
- **Community**: [GitHub Discussions](https://github.com/NajaScript/Naja/discussions)

## Performance Notes

- Most functions execute in O(1) constant time
- `isPrime()` runs in O(√n) time
- `factorial()` and `fibonacci()` run in O(n) time
- Statistical functions run in O(n) time where n is list length

---

**Math Utils v1.0.0** - Made with ❤️ by the NajaScript Community

*Complete mathematical toolkit for your NajaScript projects!* 🚀📚 