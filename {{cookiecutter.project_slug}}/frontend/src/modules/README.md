# Frontend Modules Architecture

## Overview

This application uses a module-based architecture for better organization and scalability. Each module encapsulates a specific feature area with its own views, components, stores, and routing.

## Module Structure

Each module follows this structure:

```
module-name/
├── router.js          # Module routes
├── views/            # Page components for this module
├── components/       # Reusable components specific to this module
├── stores/           # Pinia stores for this module (if needed)
├── services/         # API services for this module (if needed)
└── types/            # TypeScript types for this module (if using TS)
```

## Current Modules

### 1. Auth Module (`/auth`)
Handles authentication-related functionality:
- Login page
- Registration page
- Password reset
- Uses `AuthLayout` for consistent auth UI

### 2. Dashboard Module (`/dashboard`)
Provides authenticated user functionality:
- Main dashboard view
- User profile management
- Settings
- Analytics
- Uses `DashboardLayout` with sidebar navigation

### 3. Home Module (`/`)
Public-facing pages:
- Homepage
- Features
- Pricing
- About
- Contact
- Uses `MainLayout` for public pages

## Creating a New Module

1. Create a new directory under `src/modules/`:
```bash
mkdir src/modules/my-module
mkdir src/modules/my-module/views
```

2. Create the module router:
```javascript
// src/modules/my-module/router.js
import MyLayout from '@/layouts/MyLayout.vue'
import MyView from './views/MyView.vue'

export default [
  {
    path: '/my-module',
    component: MyLayout,
    children: [
      {
        path: '',
        name: 'MyModule',
        component: MyView,
      },
    ],
  },
]
```

3. Import and register in main router:
```javascript
// src/router/index.js
import myModuleRoutes from '@/modules/my-module/router'

const routes = [
  ...existingRoutes,
  ...myModuleRoutes,
]
```

## Benefits of Module Architecture

1. **Scalability**: Easy to add new features without cluttering the main structure
2. **Maintainability**: Related code is grouped together
3. **Code Splitting**: Each module can be lazy-loaded for better performance
4. **Team Collaboration**: Different teams can work on different modules
5. **Reusability**: Modules can be shared across projects

## Best Practices

1. **Keep modules focused**: Each module should handle one feature area
2. **Use layouts consistently**: Group pages with similar layouts
3. **Lazy load routes**: Use dynamic imports for better performance
4. **Module independence**: Minimize dependencies between modules
5. **Shared code**: Put truly shared components in `/src/components`

## Navigation Between Modules

Use Vue Router for navigation:

```javascript
// In components
<RouterLink to="/dashboard">Dashboard</RouterLink>

// In scripts
import { useRouter } from 'vue-router'
const router = useRouter()
router.push('/dashboard')
```

## Module Communication

For cross-module communication:
1. Use Pinia stores for shared state
2. Use event bus for decoupled communication
3. Use props/events for parent-child communication

## File Organization Tips

- **Views**: Full page components that are routed to
- **Components**: Reusable pieces within the module
- **Services**: API calls and business logic
- **Stores**: State management for the module
- **Utils**: Helper functions specific to the module