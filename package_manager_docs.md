# NajaScript Package Manager

This package manager allows you to install, manage, and use external packages in your NajaScript projects, similar to how npm or yarn works for JavaScript.

## Installation

The package manager is included with the NajaScript installation. The main tools are:

- `naja_package_manager.py` - Core package manager functionality
- `naja_add.py` - Helper script for quickly adding packages
- `naja_add.bat` - Windows batch file wrapper

## Commands

### Adding Packages

```
naja_add <package_name> [version] [--dev/-d]
```

Example:
```
naja_add MathUtils 1.0.0
naja_add TestingLibrary --dev
```

### Using Package Manager Directly

For more advanced operations, you can use the package manager script directly:

```
python naja_package_manager.py add <package_name> [--version VERSION] [--dev]
python naja_package_manager.py remove <package_name> [--dev]
python naja_package_manager.py list
python naja_package_manager.py install
```

## Project Structure

When you add packages, they are stored in the `naja_modules` directory in your project root:

```
my_project/
├── main.naja
├── naja_packages.json    # Package configuration file
└── naja_modules/         # Installed packages
    ├── MathUtils/
    │   └── index.naja
    └── AnotherPackage/
        └── index.naja
```

## Using Packages in Your Code

To use a package in your code, import it using the standard import statement:

```
import "MathUtils";

fun main() {
    println(MathUtils.info());  // Prints package information
    // Use other functions from the package
}

main();
```

## Package Format

Each package should have an `index.naja` file that exports functions and variables:

```
// Example package file: naja_modules/MathUtils/index.naja

export fun add(int a, int b) {
    return a + b;
}

export fun subtract(int a, int b) {
    return a - b;
}

export fun info() {
    return "MathUtils package v1.0.0";
}
```

## Creating Your Own Packages

To create a package that others can use, create a directory with your package name and add an `index.naja` file that exports your functions and variables.

## Future Enhancements

- Remote package registry for downloading packages
- Version resolution and dependency management
- Package publishing functionality 