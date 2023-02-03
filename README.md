# Owl Dependencies

This project only aims to gather all dependencies for the Owl Engine

## Rebuild Package

Regenerate all the dependencies by running python script:

```bash
python3 PyUtils/regenerate.py
```

A cmake target `regenerate` will do the same or with the `all` target.

## header-only

### DebugBreak

Version: 1.0
Depends: None
Source: [github](https://github.com/scottt/debugbreak)

## Libraries

### FMT

Version: 9.1.0
Depends: None
Source : [github](https://github.com/fmtlib/fmt)

### SPDLOG

Version: 1.11.0
Depends: fmt
Source : [github](https://github.com/gabime/spdlog)
