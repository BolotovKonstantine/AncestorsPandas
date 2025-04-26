# Surname Normalization Guide

## Overview

Surname normalization is a key feature in AncestorsPandas that standardizes surname variations to improve data consistency and analysis accuracy. This guide provides detailed information about how surname normalization works, how to use it, and how to customize it for your specific needs.

## Table of Contents

- [Introduction](#introduction)
- [How Surname Normalization Works](#how-surname-normalization-works)
  - [Transformation Steps](#transformation-steps)
  - [Russian Surname Handling](#russian-surname-handling)
  - [Prefix Handling](#prefix-handling)
  - [Hyphenated Surnames](#hyphenated-surnames)
- [Using Surname Normalization](#using-surname-normalization)
  - [In Python Code](#in-python-code)
  - [In the Web Interface](#in-the-web-interface)
- [Configuration and Customization](#configuration-and-customization)
  - [Default Configuration](#default-configuration)
  - [Customizing Normalization Rules](#customizing-normalization-rules)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Introduction

Surname normalization helps standardize surname variations that might occur due to:
- Gender-specific forms (especially in Slavic languages)
- Capitalization differences
- Special characters and numbers
- Different prefix formats (e.g., "McDonald" vs "Mcdonald")
- Hyphenated surnames

By normalizing surnames, you can:
- Improve data quality and consistency
- Enhance search and matching capabilities
- Generate more accurate statistics and visualizations
- Identify family relationships more effectively

## How Surname Normalization Works

### Transformation Steps

The surname normalization process applies the following transformations in sequence:

1. **Input Validation**: Non-string values and empty strings are returned unchanged
2. **Lowercase Conversion**: All text is converted to lowercase
3. **Special Character Removal**: Special characters and numbers are removed
4. **Hyphenated Surname Handling**: For hyphenated surnames, each part is normalized separately
5. **Surname Ending Normalization**: Gender-specific endings (particularly for Russian surnames) are standardized
6. **Prefix Standardization**: Common surname prefixes are standardized

### Russian Surname Handling

Russian surnames often have gender-specific forms. The normalization process converts feminine forms to masculine forms:

1. **Simple Feminine Suffix**: Removes the trailing "а" (e.g., "Петрова" → "петров")
2. **Complex Feminine Endings**: Converts specific feminine endings to their masculine counterparts:
   - "ова" → "ов" (e.g., "Соколова" → "соколов")
   - "ева" → "ев" (e.g., "Королева" → "королев")
   - "ина" → "ин" (e.g., "Пушкина" → "пушкин")
   - "ская" → "ский" (e.g., "Достоевская" → "достоевский")

### Prefix Handling

The normalization process standardizes common surname prefixes:

- "mc" (e.g., "McDonald" → "mcdonald")
- "mac" (e.g., "MacArthur" → "macarthur")
- "van" (e.g., "VanDyke" → "vandyke")
- "von" (e.g., "VonTrapp" → "vontrapp")
- "de" (e.g., "DeNiro" → "deniro")
- "di" (e.g., "DiCaprio" → "dicaprio")
- "la" (e.g., "LaForge" → "laforge")
- "le" (e.g., "LeBlanc" → "leblanc")

### Hyphenated Surnames

For hyphenated surnames (e.g., "Иванова-Петрова"), each part is normalized separately, and the hyphen is preserved. This ensures that both parts of the surname are standardized consistently.

## Using Surname Normalization

### In Python Code

You can use the surname normalization functions directly in your Python code:

```python
from ancestors_pandas.processing.normalizations import normalize_surname, apply_surname_normalization
import pandas as pd

# Normalize a single surname
normalized = normalize_surname("Петрова")  # Returns "петров"

# Normalize surnames in a DataFrame
df = pd.DataFrame({"Surname": ["Иванова", "Петров", "Королева"]})
df = apply_surname_normalization(df, "Surname", "normalized_surname")
# Result: df now has a "normalized_surname" column with ["иванов", "петров", "королев"]
```

### In the Web Interface

To normalize surnames using the web interface:

1. Navigate to the **Data Sources** page
2. Find the data source you want to normalize and click the **Normalize** button
3. Select the surname column you want to normalize
4. Choose "Surname" as the normalization type
5. Click **Apply Normalization** to normalize the data

The normalization will create a new column in your data source with the prefix "normalized_" followed by the original column name.

## Configuration and Customization

### Default Configuration

The default configuration for surname normalization is defined in `config.py`:

```python
# Surname normalization
FEMALE_SURNAME_SUFFIX = "а"
FEMALE_SURNAME_ENDINGS = ["ова", "ева", "ина", "ская"]
MALE_SURNAME_ENDINGS = ["ов", "ев", "ин", "ский"]
SURNAME_PREFIXES = ["mc", "mac", "van", "von", "de", "di", "la", "le"]
```

### Customizing Normalization Rules

You can customize the normalization rules by modifying the constants in `config.py`:

1. **Adding New Feminine Endings**: Add new endings to `FEMALE_SURNAME_ENDINGS` and their corresponding masculine forms to `MALE_SURNAME_ENDINGS` (ensure they have the same index)
2. **Adding New Prefixes**: Add new prefixes to `SURNAME_PREFIXES`

For example, to add support for the feminine ending "ая" with masculine form "ый":

```python
FEMALE_SURNAME_ENDINGS = ["ова", "ева", "ина", "ская", "ая"]
MALE_SURNAME_ENDINGS = ["ов", "ев", "ин", "ский", "ый"]
```

## Examples

Here are examples of how different surnames are normalized:

| Original Surname | Normalized Surname | Transformation Applied |
|------------------|-------------------|------------------------|
| "Петрова"        | "петров"          | Feminine suffix removal |
| "Иванов"         | "иванов"          | Lowercase conversion |
| "Королева"       | "королев"         | Complex feminine ending |
| "Достоевская"    | "достоевский"     | Complex feminine ending |
| "McDonald"       | "mcdonald"        | Prefix standardization |
| "Иванова-Петрова" | "иванов-петров"   | Hyphenated surname handling |
| "Смит123"        | "смит"            | Special character removal |

## Best Practices

1. **Always normalize before analysis**: Apply surname normalization before performing any analysis that involves comparing or grouping surnames
2. **Keep original data**: Always maintain the original surname data alongside the normalized version
3. **Validate results**: Check the normalization results to ensure they meet your expectations
4. **Consider language context**: The default rules are optimized for Russian surnames, but you may need to customize them for other languages
5. **Handle edge cases**: Be aware that some surnames may not normalize as expected, especially those with unusual patterns

## Troubleshooting

Common issues and solutions:

1. **Unexpected normalization results**: Check if the surname follows a pattern not covered by the current rules. You may need to customize the configuration.
2. **Performance issues with large datasets**: Consider normalizing surnames in batches or using parallel processing.
3. **Missing normalizations**: Ensure that the surname column is correctly specified and contains string values.
4. **Error during normalization**: Check for invalid characters or encoding issues in the original surnames.

If you encounter persistent issues, consider examining the specific surnames causing problems and adjusting the normalization rules accordingly.