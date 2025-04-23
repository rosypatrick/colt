# Colt Wayfinder Tool - User Journey Specification

This document outlines the user journey for the Colt Wayfinder Tool, focusing on the input form structure, required vs. optional fields, and the overall flow from input to output.

## Input Form Structure

### Project Attributes

| Field | Status | Description | Options |
|-------|--------|-------------|---------|
| **Industry** | Required | The industry sector for the project | Commercial Real Estate, Healthcare, Education, Industrial, Retail, Data Centers, Other (with text input) |
| **Size of Project** | Optional | Total size of the project area | Numeric input with unit selection (sq meters/sq feet) |
| **Application** | Required | Where the solution will be applied | Roof, Wall, Ceiling, Window/glazing system, Screens/partitions |
| **Glazing Type** | Optional | Type of glazing if applicable | Single glazed, Double glazed, Triple glazed, Fire-rated, Acoustic, Solar control, Not applicable |
| **Usage Location** | Required | Whether for interior or exterior use | Interior, Exterior, Both |

### Performance Attributes

| Field | Status | Description | Input Type |
|-------|--------|-------------|------------|
| **Cv Value** | Optional | Coefficient of flow - how much air can flow through at a given pressure drop | Numeric input with tooltip explanation |
| **U-Value** | Optional | Thermal transmittance - measure of heat transfer rate | Numeric input with tooltip explanation |
| **Acoustics Value** | Optional | Sound reduction index in dB | Numeric input with tooltip explanation |

## User Journey Flow

### 1. Landing Page
- Users land on the homepage featuring a prominent search bar
- Options to "Search Products" or "Get Guided Recommendations"
- Featured solutions and case studies displayed below

### 2. Guided Search Journey

#### Step 1: Project Attributes Form
- Form with the fields listed in the Project Attributes table above
- Clear indication of which fields are required (*) and which are optional
- "Next" button to proceed to Performance Attributes

#### Step 2: Performance Attributes Form
- Form with the fields listed in the Performance Attributes table above
- All fields optional with helpful tooltips explaining each value
- "Find Solutions" button to submit the form

#### Step 3: Results Page
- Results displayed in a grid or list format
- Each result includes:
  - Product/solution name
  - Brief description
  - Key specifications matching user criteria
  - Thumbnail image
  - "Learn More" button
- Filter panel on the side to refine results
- Option to save or share results

#### Step 4: Detailed Product/Solution Page
- Comprehensive information about the selected solution
- Technical specifications with emphasis on the criteria the user specified
- Related products/solutions
- Downloadable technical documentation
- Request for quote/contact form

### 3. Direct Search Journey

#### Step 1: Search Input
- User enters keywords in the search bar
- Autocomplete suggestions appear as user types

#### Step 2: Search Results
- Similar to the Guided Search results page
- Additional categorization of results (Products, Solutions, Documentation)
- Filter options specific to search queries

## Form Validation and Error Handling

### Validation Rules
- Required fields: Show error if left empty on form submission
- Numeric inputs: Accept only valid numbers within reasonable ranges
- Other validation as appropriate for specific fields

### Error Messages
- Inline validation errors appear below respective fields
- Clear guidance on how to correct errors
- Non-blocking warnings for potentially unusual values

## Progressive Disclosure

To simplify the user experience, we'll implement progressive disclosure:

1. Start with essential fields only (Industry, Application, Usage Location)
2. "Advanced Options" toggle reveals additional fields:
   - Size of Project
   - Glazing Type
   - Performance Attributes

## Responsive Design Considerations

The form adapts to different screen sizes:

- **Desktop**: Two-column layout with contextual help on the right
- **Tablet**: Single column with expandable help sections
- **Mobile**: Streamlined single column with simplified controls

## Sample UI Mockup

```
┌─────────────────────────────────────────────────────┐
│ Colt Wayfinder Tool                                 │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────┐ │
│ │ Find the perfect solution for your building     │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Project Attributes                              │ │
│ │                                                 │ │
│ │ Industry*                                       │ │
│ │ ┌─────────────────────────────────────────────┐ │ │
│ │ │ Commercial Real Estate                    ▼ │ │ │
│ │ └─────────────────────────────────────────────┘ │ │
│ │                                                 │ │
│ │ Size of Project                                 │ │
│ │ ┌───────────────────────┐ ┌─────────────────┐   │ │
│ │ │ 1000                  │ │ sq meters     ▼ │   │ │
│ │ └───────────────────────┘ └─────────────────┘   │ │
│ │ Optional                                        │ │
│ │                                                 │ │
│ │ Application*                                    │ │
│ │ ┌─────────────────────────────────────────────┐ │ │
│ │ │ Roof                                      ▼ │ │ │
│ │ └─────────────────────────────────────────────┘ │ │
│ │                                                 │ │
│ │ Glazing Type                                    │ │
│ │ ┌─────────────────────────────────────────────┐ │ │
│ │ │ Not applicable                            ▼ │ │ │
│ │ └─────────────────────────────────────────────┘ │ │
│ │ Optional                                        │ │
│ │                                                 │ │
│ │ Usage Location*                                 │ │
│ │ ┌─────────────────────────────────────────────┐ │ │
│ │ │ Exterior                                  ▼ │ │ │
│ │ └─────────────────────────────────────────────┘ │ │
│ │                                                 │ │
│ │ ┌─────────────────────────────────────────────┐ │ │
│ │ │ Advanced Options                      [+]   │ │ │
│ │ └─────────────────────────────────────────────┘ │ │
│ │                                                 │ │
│ │ ┌─────────────────────────────────────────────┐ │ │
│ │ │ Next                                        │ │ │
│ │ └─────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## User Input to Result Mapping Logic

This section outlines how user inputs connect to product recommendations:

### Primary Mapping Factors

1. **Industry + Application**: Primary filter for product categories
   - Example: "Commercial Real Estate" + "Roof" → Smoke ventilators, climate control systems
   
2. **Usage Location**: Narrows down to interior or exterior products
   - Example: "Exterior" → Weather-resistant louvres, external ventilation systems

3. **Size + Performance Values**: Used for sizing and specific product selection
   - Example: Large project + High Cv Value requirement → Industrial-scale ventilation systems

### Secondary Refinement Factors

1. **Glazing Type**: Influences window/façade recommendations
   - Example: "Fire-rated" → Fire-resistant ventilation products

2. **Acoustic Value**: Prioritizes sound-attenuated products
   - Example: High acoustic value → Acoustically-treated ventilation systems

## Default Values and Smart Suggestions

To help users who are unsure about technical specifications:

1. **Default Industry Values**: Common ranges for each industry
   - Example: Education buildings typically need U-Values between X and Y

2. **Smart Suggestions**: As users select certain options, suggest typical values
   - Example: When "Data Center" is selected, suggest high Cv values

3. **Value Range Indicators**: Visual sliders with industry benchmarks
   - Example: Slider for U-Value shows "Energy Efficient" to "Standard" range

## Implementation Details

### Data Structure

```json
{
  "project": {
    "attributes": {
      "industry": "Commercial Real Estate",
      "size": {
        "value": 1000,
        "unit": "sqm"
      },
      "application": "Roof",
      "glazing": "Not applicable",
      "location": "Exterior"
    },
    "performance": {
      "cv_value": 0.65,
      "u_value": 1.2,
      "acoustics_value": 35
    }
  }
}
```

### API Endpoints

```
POST /api/guided-search
Body: {project object above}
Returns: List of matched products/solutions
```

## A/B Testing Strategy

To optimize the user journey, we'll conduct A/B testing on:

1. Form layout (single page vs. multi-step wizard)
2. Field ordering and grouping
3. Default values vs. blank inputs
4. Required vs. optional field configurations

## Future Enhancements

- **Project History**: Save previous searches for quick reference
- **Similar Projects**: Suggest configurations based on similar buildings
- **3D Visualization**: Show how products would look in the specified application
- **Real-time Calculation**: Display estimated performance metrics as options are selected
- **Environmental Impact**: Add sustainability metrics to the performance attributes
