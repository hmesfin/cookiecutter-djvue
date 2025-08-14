# Icon System Documentation

This project uses `unplugin-icons` for a flexible, tree-shakeable icon system. Icons are auto-imported on demand, meaning only the icons you use are included in your bundle.

## Available Icon Libraries

We've pre-configured three high-quality icon libraries:

### 1. Lucide Icons (Recommended - 1000+ icons)
- **Prefix**: `IconLucide`
- **Example**: `<IconLucideHome />`, `<IconLucideSettings />`, `<IconLucideUser />`
- **Browse**: https://lucide.dev/icons/

### 2. Tabler Icons (3000+ icons)
- **Prefix**: `IconTabler`
- **Example**: `<IconTablerHome />`, `<IconTablerSettings />`, `<IconTablerUser />`
- **Browse**: https://tabler-icons.io/

### 3. Heroicons (300+ icons)
- **Prefix**: `IconHeroicons`
- **Example**: `<IconHeroiconsHome />`, `<IconHeroiconsOutlineCog />`, `<IconHeroiconsSolidUser />`
- **Browse**: https://heroicons.com/

## Usage Examples

### Basic Usage
Icons are auto-imported, so you can use them directly in your templates:

```vue
<template>
  <!-- Lucide Icons (recommended) -->
  <IconLucideHome class="w-5 h-5" />
  <IconLucideSettings class="w-6 h-6 text-gray-600" />
  <IconLucideUser class="w-4 h-4 text-indigo-600" />
  
  <!-- Tabler Icons -->
  <IconTablerBrandGithub class="w-5 h-5" />
  <IconTablerMail class="w-6 h-6" />
  
  <!-- Heroicons -->
  <IconHeroiconsOutlineHome class="w-5 h-5" />
  <IconHeroiconsSolidCog class="w-6 h-6" />
</template>
```

### Common Icon Patterns

#### Navigation Icons
```vue
<RouterLink to="/dashboard" class="flex items-center gap-2">
  <IconLucideHome class="w-5 h-5" />
  <span>Dashboard</span>
</RouterLink>
```

#### Button with Icon
```vue
<button class="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg">
  <IconLucidePlus class="w-4 h-4" />
  <span>Add New</span>
</button>
```

#### Status Icons
```vue
<span v-if="status === 'success'" class="text-green-600">
  <IconLucideCheckCircle class="w-5 h-5" />
</span>
<span v-else-if="status === 'error'" class="text-red-600">
  <IconLucideXCircle class="w-5 h-5" />
</span>
<span v-else class="text-yellow-600">
  <IconLucideAlertCircle class="w-5 h-5" />
</span>
```

#### Loading Spinner
```vue
<IconLucideLoader2 class="w-5 h-5 animate-spin" />
```

## Icon Sizing Convention

Use Tailwind's width and height utilities:

- `w-3 h-3` - Extra small (12px)
- `w-4 h-4` - Small (16px)
- `w-5 h-5` - Medium (20px) - **Default for most use cases**
- `w-6 h-6` - Large (24px)
- `w-8 h-8` - Extra large (32px)

## Adding More Icon Libraries

To add additional icon collections:

1. Install the icon set:
```bash
npm install -D @iconify-json/mdi  # Material Design Icons
npm install -D @iconify-json/carbon  # IBM Carbon Icons
npm install -D @iconify-json/ph  # Phosphor Icons
```

2. Update `vite.config.js`:
```javascript
IconsResolver({
  prefix: 'Icon',
  enabledCollections: ['lucide', 'tabler', 'heroicons', 'mdi', 'carbon', 'ph']
})
```

3. Use the icons:
```vue
<IconMdiAccount />
<IconCarbonSettings />
<IconPhHouse />
```

## Icon Component Wrapper (Optional)

If you need dynamic icons, use the included `IconWrapper` component:

```vue
<template>
  <IconWrapper :name="dynamicIconName" size="md" collection="lucide" />
</template>

<script setup>
const dynamicIconName = computed(() => {
  return isOpen.value ? 'chevron-up' : 'chevron-down'
})
</script>
```

## Best Practices

1. **Consistency**: Stick to one icon library per feature/page for visual consistency
2. **Semantic naming**: Use descriptive icon names that match their purpose
3. **Accessibility**: Add `aria-label` or `title` attributes for icon-only buttons
4. **Performance**: Icons are auto tree-shaken, so don't worry about importing too many
5. **Dark mode**: Icons inherit text color, so use Tailwind's dark mode classes

## Common Icons Reference

| Purpose | Lucide | Tabler | Heroicons |
|---------|--------|--------|-----------|
| Home | `IconLucideHome` | `IconTablerHome` | `IconHeroiconsOutlineHome` |
| Settings | `IconLucideSettings` | `IconTablerSettings` | `IconHeroiconsOutlineCog` |
| User | `IconLucideUser` | `IconTablerUser` | `IconHeroiconsOutlineUser` |
| Search | `IconLucideSearch` | `IconTablerSearch` | `IconHeroiconsOutlineMagnifyingGlass` |
| Menu | `IconLucideMenu` | `IconTablerMenu2` | `IconHeroiconsOutlineBars3` |
| Close | `IconLucideX` | `IconTablerX` | `IconHeroiconsOutlineXMark` |
| Add | `IconLucidePlus` | `IconTablerPlus` | `IconHeroiconsOutlinePlus` |
| Edit | `IconLucideEdit` | `IconTablerEdit` | `IconHeroiconsOutlinePencil` |
| Delete | `IconLucideTrash2` | `IconTablerTrash` | `IconHeroiconsOutlineTrash` |
| Check | `IconLucideCheck` | `IconTablerCheck` | `IconHeroiconsOutlineCheck` |
| Error | `IconLucideXCircle` | `IconTablerCircleX` | `IconHeroiconsOutlineXCircle` |
| Warning | `IconLucideAlertTriangle` | `IconTablerAlertTriangle` | `IconHeroiconsOutlineExclamationTriangle` |
| Info | `IconLucideInfo` | `IconTablerInfoCircle` | `IconHeroiconsOutlineInformationCircle` |
| Download | `IconLucideDownload` | `IconTablerDownload` | `IconHeroiconsOutlineArrowDownTray` |
| Upload | `IconLucideUpload` | `IconTablerUpload` | `IconHeroiconsOutlineArrowUpTray` |

## TypeScript Support

Icons are fully typed. If using TypeScript, you'll get auto-completion for all available icons.

## Troubleshooting

If an icon doesn't appear:
1. Check the icon name in the library's documentation
2. Ensure the collection is enabled in `vite.config.js`
3. Restart the dev server after adding new icon libraries
4. Check the browser console for any import errors

## VS Code Extension

For better DX, install the "Iconify IntelliSense" VS Code extension for icon previews and auto-completion.