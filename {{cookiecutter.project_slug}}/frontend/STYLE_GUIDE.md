# Style Guide - {{ cookiecutter.project_name }}

## Design System Overview

This project uses a **DRY (Don't Repeat Yourself)** approach to styling with TailwindCSS. We've established a consistent design system with emerald-600 as our primary color and reusable component classes.

## Color Palette

### Primary Colors (Emerald)
- **Primary**: `emerald-600` / `dark:emerald-500`
- **Primary Hover**: `emerald-700` / `dark:emerald-600`
- **Primary Light**: `emerald-50` / `dark:emerald-900/20`
- **Primary Text**: `text-emerald-600` / `dark:text-emerald-400`

### Neutral Colors (Gray)
- **Background**: `white` / `dark:gray-900`
- **Surface**: `gray-50` / `dark:gray-800`
- **Border**: `gray-200` / `dark:gray-700`
- **Text Primary**: `gray-900` / `dark:gray-100`
- **Text Secondary**: `gray-600` / `dark:gray-400`
- **Text Muted**: `gray-500` / `dark:gray-500`

### Semantic Colors
- **Success**: `green-500` / `green-600`
- **Warning**: `amber-500` / `amber-600`
- **Danger**: `red-500` / `red-600`
- **Info**: `blue-500` / `blue-600`

## Component Classes

### Buttons

```html
<!-- Primary Button -->
<button class="btn btn-primary">Save Changes</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">Cancel</button>

<!-- Danger Button -->
<button class="btn btn-danger">Delete</button>

<!-- Ghost Button -->
<button class="btn btn-ghost">Learn More</button>

<!-- Size Variants -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Default</button>
<button class="btn btn-primary btn-lg">Large</button>
```

### Form Elements

```html
<!-- Form Label -->
<label class="form-label">Email Address</label>

<!-- Text Input -->
<input type="text" class="form-input" placeholder="Enter your email">

<!-- Select -->
<select class="form-select">
  <option>Option 1</option>
  <option>Option 2</option>
</select>

<!-- Textarea -->
<textarea class="form-textarea" rows="4"></textarea>

<!-- Checkbox -->
<input type="checkbox" class="form-checkbox">

<!-- Radio -->
<input type="radio" class="form-radio">

<!-- Error Message -->
<p class="form-error">This field is required</p>

<!-- Helper Text -->
<p class="form-helper">We'll never share your email</p>
```

### Cards

```html
<!-- Basic Card -->
<div class="card">
  <div class="card-body">
    Content goes here
  </div>
</div>

<!-- Card with Header and Footer -->
<div class="card">
  <div class="card-header">
    <h3>Card Title</h3>
  </div>
  <div class="card-body">
    Content goes here
  </div>
  <div class="card-footer">
    Footer content
  </div>
</div>
```

### Badges

```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-secondary">Secondary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-danger">Danger</span>
```

### Alerts

```html
<div class="alert alert-success">Success message</div>
<div class="alert alert-warning">Warning message</div>
<div class="alert alert-danger">Error message</div>
<div class="alert alert-info">Info message</div>
```

### Navigation

```html
<!-- Navigation Link -->
<a href="#" class="nav-link nav-link-active">Active</a>
<a href="#" class="nav-link nav-link-inactive">Inactive</a>

<!-- Tabs -->
<button class="tab tab-active">Active Tab</button>
<button class="tab tab-inactive">Inactive Tab</button>
```

### Modals

```html
<!-- Modal Structure -->
<div class="modal-backdrop"></div>
<div class="modal-content">
  <div class="modal-header">
    <h3>Modal Title</h3>
  </div>
  <div class="modal-body">
    Modal content
  </div>
  <div class="modal-footer">
    <button class="btn btn-secondary">Cancel</button>
    <button class="btn btn-primary">Confirm</button>
  </div>
</div>
```

### Tables

```html
<table class="table">
  <thead class="table-header">
    <tr>
      <th class="table-header-cell">Name</th>
      <th class="table-header-cell">Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="table-cell">John Doe</td>
      <td class="table-cell">john@example.com</td>
    </tr>
  </tbody>
</table>
```

## Utility Classes

### Text and Colors
```html
<p class="text-primary">Primary colored text</p>
<div class="bg-primary">Primary background</div>
<div class="border-primary">Primary border</div>
```

### Focus States
```html
<button class="focus-primary">Focused element</button>
```

### Hover Effects
```html
<div class="hover-lift">Lifts on hover</div>
<div class="hover-glow">Glows on hover</div>
```

### Loading States
```html
<div class="skeleton h-4 w-32"></div>
<div class="spinner"></div>
```

### Animations
```html
<div class="animate-fade-in">Fades in</div>
<div class="animate-slide-up">Slides up</div>
<div class="animate-slide-down">Slides down</div>
```

## Best Practices

### 1. Use Component Classes First
Instead of repeating long utility chains, use our predefined component classes:

```html
<!-- ❌ Don't do this -->
<button class="px-4 py-2 font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500">
  Click me
</button>

<!-- ✅ Do this -->
<button class="btn btn-primary">
  Click me
</button>
```

### 2. Maintain Consistency
Always use the emerald color palette for primary actions and branding elements:

```html
<!-- Primary actions -->
<button class="btn btn-primary">Save</button>
<a href="#" class="link">Learn more</a>

<!-- Secondary elements -->
<button class="btn btn-secondary">Cancel</button>
```

### 3. Dark Mode Support
Always include dark mode variants for better accessibility:

```html
<!-- Always pair light and dark variants -->
<div class="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
  Content
</div>
```

### 4. Responsive Design
Use responsive modifiers for different screen sizes:

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Grid items -->
</div>
```

### 5. Accessibility
- Always include focus states for interactive elements
- Use semantic HTML elements
- Include proper ARIA labels where needed
- Ensure sufficient color contrast

```html
<button 
  class="btn btn-primary focus-primary" 
  aria-label="Save changes"
>
  Save
</button>
```

## File Organization

```
frontend/src/
├── styles/
│   ├── components.css    # Component classes definitions
│   └── ...
├── assets/
│   └── tailwind.css      # Tailwind imports
└── components/
    └── ...               # Vue components using the classes
```

## Migration Guide

To migrate existing components to use our DRY system:

1. **Run the migration script**:
   ```bash
   python scripts/migrate_to_emerald.py
   ```

2. **Replace utility chains with component classes**:
   - Buttons: Use `btn btn-*` classes
   - Forms: Use `form-*` classes
   - Cards: Use `card` classes
   - Badges: Use `badge badge-*` classes

3. **Update color references**:
   - Replace `indigo-*` with `emerald-*`
   - Replace `blue-*` with `emerald-*` for primary actions

## Examples

### Login Form
```html
<form class="card">
  <div class="card-body">
    <div class="mb-4">
      <label class="form-label">Email</label>
      <input type="email" class="form-input" required>
    </div>
    <div class="mb-4">
      <label class="form-label">Password</label>
      <input type="password" class="form-input" required>
    </div>
    <button type="submit" class="btn btn-primary w-full">
      Sign In
    </button>
  </div>
</form>
```

### Data Table
```html
<div class="card">
  <div class="card-header">
    <h3 class="text-lg font-semibold">Users</h3>
  </div>
  <div class="card-body">
    <table class="table">
      <thead class="table-header">
        <tr>
          <th class="table-header-cell">Name</th>
          <th class="table-header-cell">Status</th>
          <th class="table-header-cell">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="table-cell">John Doe</td>
          <td class="table-cell">
            <span class="badge badge-success">Active</span>
          </td>
          <td class="table-cell">
            <button class="btn btn-sm btn-ghost">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

## Resources

- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Component Classes Reference](./src/styles/components.css)
- [Migration Script](../scripts/migrate_to_emerald.py)

---

*This style guide is a living document. Please update it as the design system evolves.*