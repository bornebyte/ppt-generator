# Enhanced PPT Generator Features Documentation

## Overview
The PPT Generator now supports rich formatting and visual elements beyond basic bullet points. This document provides a comprehensive guide to all available features.

## New Features Added

### 1. **Headings** 📝
Create section headings with different sizes and colors.

```json
{
  "kind": "heading",
  "text": "Section Title",
  "level": 1,          // 1=large (28pt), 2=medium (24pt), 3=small (20pt)
  "color": "blue",     // Optional: any color format
  "align": "center"    // Optional: left, center, right, justify
}
```

### 2. **Styled Paragraphs** 📄
Enhanced paragraphs with full formatting control.

```json
{
  "kind": "paragraph",
  "text": "Your detailed text here",
  "size": 16,          // Optional: font size in points
  "color": "black",    // Optional: text color
  "bold": false,       // Optional: bold text
  "italic": false,     // Optional: italic text
  "align": "left"      // Optional: text alignment
}
```

### 3. **Enhanced Bullets** 🔹
Bullets with colors, styling, and nested sub-points.

```json
{
  "kind": "bullets",
  "color": "black",    // Optional: default color for all items
  "items": [
    "Simple bullet point",
    {
      "text": "Styled bullet",
      "bold": true,
      "color": "red",
      "subpoints": [
        "Sub-point text",
        {
          "text": "Colored sub-point",
          "color": "green"
        }
      ]
    }
  ]
}
```

### 4. **Numbered Lists** 🔢
Sequential numbered lists with custom styling.

```json
{
  "kind": "numbered_list",
  "items": [
    "First item",
    "Second item",
    {
      "text": "Colored item",
      "color": "blue"
    }
  ],
  "start": 1,          // Optional: starting number
  "color": "black"     // Optional: default color
}
```

### 5. **Tables** 📊
Professional data tables with headers and custom styling.

```json
{
  "kind": "table",
  "rows": [
    ["Header 1", "Header 2", "Header 3"],
    ["Data 1", "Data 2", "Data 3"],
    ["Data 4", "Data 5", "Data 6"]
  ],
  "header": true,                    // First row is header
  "header_color": [68, 114, 196],   // RGB array for header background
  "header_text_color": "white",     // Header text color
  "font_size": 11,                  // Table font size
  "left": 1,                        // Position from left (inches)
  "top": 3,                         // Position from top (inches)
  "width": 8,                       // Table width (inches)
  "height": 2,                      // Table height (inches)
  "col_widths": [2.5, 2.5, 3]      // Optional: custom column widths
}
```

**Advanced Table Features:**
- Cells can be objects with custom colors:
```json
{
  "rows": [
    ["Header"],
    [{"text": "Red cell", "color": "red", "bg_color": "#FFF59D"}]
  ]
}
```

### 6. **Text Boxes** 📦
Positioned text boxes with backgrounds and custom styling.

```json
{
  "kind": "text_box",
  "text": "Highlighted important text",
  "left": 2,           // Position from left (inches)
  "top": 5,            // Position from top (inches)
  "width": 5,          // Box width (inches)
  "height": 0.8,       // Box height (inches)
  "font_size": 14,     // Text size
  "bold": true,        // Bold text
  "italic": false,     // Italic text
  "color": "white",    // Text color
  "bg_color": "#4472C4",  // Background color (hex)
  "align": "center"    // Text alignment
}
```

**Use Cases:**
- ⚠️ Warnings: Red background, white text
- ✓ Success messages: Green background
- ℹ️ Information boxes: Blue background
- 💡 Tips: Yellow background, black text

### 7. **Images** 🖼️
Multiple layout options for images (unchanged from original).

```json
{
  "kind": "images",
  "layout": "row",     // row, column, or grid
  "items": [
    {"path": "image1.png"},
    {"path": "image2.png"}
  ]
}
```

## Color Formats

You can specify colors in three ways:

### Named Colors
```json
"color": "red"
"color": "blue"
"color": "green"
```

**Available names:** red, blue, green, yellow, orange, purple, pink, brown, gray, black, white

### Hexadecimal
```json
"color": "#FF0000"    // Red
"color": "#0000FF"    // Blue
"bg_color": "#FFF59D" // Light yellow
```

### RGB Array
```json
"color": [255, 0, 0]      // Red
"header_color": [68, 114, 196]  // Blue
```

## Alignment Options

All text elements support alignment:
- `"left"` - Left aligned (default)
- `"center"` - Centered
- `"right"` - Right aligned
- `"justify"` - Justified (full width)

## Optional vs Required Properties

### Always Required:
- `"kind"` - The block type
- Type-specific required fields (e.g., "text" for paragraphs, "rows" for tables)

### Always Optional:
- Colors, sizes, formatting (bold, italic)
- Positioning (left, top, width, height)
- Alignment
- Custom styling options

## Best Practices

### 1. Visual Hierarchy
```json
[
  {"kind": "heading", "text": "Main Topic", "level": 1, "color": "blue"},
  {"kind": "paragraph", "text": "Explanation..."},
  {"kind": "bullets", "items": ["Point 1", "Point 2"]}
]
```

### 2. Data Presentation
Use tables for comparing data:
```json
{"kind": "table", "rows": [...], "header": true}
```

### 3. Emphasis
Use text boxes for key takeaways:
```json
{
  "kind": "text_box",
  "text": "💡 Key Takeaway",
  "bg_color": "#FFF59D",
  "bold": true
}
```

### 4. Color Strategy
- **Blue**: Informational, professional
- **Red**: Warnings, important items
- **Green**: Success, positive outcomes
- **Orange**: Highlights, attention
- **Purple**: Special emphasis

### 5. Mixed Content
Combine multiple block types on one slide:
```json
"blocks": [
  {"kind": "heading", "text": "Overview", "level": 1},
  {"kind": "paragraph", "text": "Introduction..."},
  {"kind": "bullets", "items": ["Point 1", "Point 2"]},
  {"kind": "table", "rows": [...]},
  {"kind": "text_box", "text": "Summary"}
]
```

## Example Slides

### Professional Data Slide
```json
{
  "type": "content",
  "title": "Quarterly Results",
  "blocks": [
    {
      "kind": "heading",
      "text": "Q4 2024 Performance",
      "level": 2,
      "color": "blue"
    },
    {
      "kind": "table",
      "rows": [
        ["Metric", "Q3", "Q4", "Change"],
        ["Revenue", "$10M", "$12M", "+20%"],
        ["Profit", "$2M", "$3M", "+50%"]
      ],
      "header": true,
      "header_color": [68, 114, 196]
    },
    {
      "kind": "text_box",
      "text": "✓ Best quarter in company history!",
      "bg_color": "#27AE60",
      "color": "white",
      "align": "center"
    }
  ]
}
```

### Educational Slide
```json
{
  "type": "content",
  "title": "Key Concepts",
  "blocks": [
    {
      "kind": "heading",
      "text": "Three Main Principles",
      "level": 2,
      "color": "purple"
    },
    {
      "kind": "numbered_list",
      "items": [
        "First principle with explanation",
        "Second principle with details",
        "Third principle with examples"
      ],
      "color": "black"
    },
    {
      "kind": "text_box",
      "text": "💡 Remember: Practice makes perfect!",
      "bg_color": "#FFF59D",
      "left": 2,
      "top": 5
    }
  ]
}
```

## Troubleshooting

### Issue: Text not appearing
- Check that required fields are present ("kind", "text")
- Verify JSON is valid

### Issue: Colors not working
- Check color format (named, hex, or RGB)
- Ensure hex codes start with #
- RGB arrays must have exactly 3 numbers [R, G, B]

### Issue: Table layout problems
- Verify all rows have the same number of columns
- Check positioning values are reasonable (in inches)
- Ensure col_widths array length matches number of columns

### Issue: Text box not visible
- Check positioning (left, top) - should be within slide bounds
- Verify width and height are reasonable
- Check if text color contrasts with background

## Complete Example

See `example_enhanced.json` in the project root for a complete working example showcasing all features.

## Migration from Old Format

Old format (still supported):
```json
{
  "kind": "paragraph",
  "text": "Simple text"
}
```

Enhanced format:
```json
{
  "kind": "paragraph",
  "text": "Styled text",
  "size": 18,
  "color": "blue",
  "bold": true
}
```

**Note:** All old JSON files will continue to work. Simply add optional properties to enhance them.

## Support

For issues or questions:
- GitHub: [@bornebyte](https://github.com/bornebyte)
- Email: shahshubham1888@gmail.com

---

**Version:** 2.0.0 (Enhanced Edition)  
**Created by:** Shubham Shah
