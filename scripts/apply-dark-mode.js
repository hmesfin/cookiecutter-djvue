#!/usr/bin/env node

/**
 * Script to automatically apply dark mode classes to Vue components
 * Usage: node scripts/apply-dark-mode.js [options]
 * 
 * Options:
 *   --dir <path>     Directory to process (default: src)
 *   --dry-run        Show what would be changed without modifying files
 *   --verbose        Show detailed processing information
 *   --backup         Create backup files before modifying
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Parse command line arguments
const args = process.argv.slice(2);
const options = {
  dir: 'src',
  dryRun: args.includes('--dry-run'),
  verbose: args.includes('--verbose'),
  backup: args.includes('--backup'),
};

// Override directory if specified
const dirIndex = args.indexOf('--dir');
if (dirIndex !== -1 && args[dirIndex + 1]) {
  options.dir = args[dirIndex + 1];
}

// Color mappings for automatic dark mode conversion
const COLOR_MAPPINGS = {
  // Backgrounds
  'bg-white': 'dark:bg-gray-900',
  'bg-gray-50': 'dark:bg-gray-900',
  'bg-gray-100': 'dark:bg-gray-800',
  'bg-gray-200': 'dark:bg-gray-700',
  'bg-gray-300': 'dark:bg-gray-600',
  'bg-red-50': 'dark:bg-red-900/20',
  'bg-green-50': 'dark:bg-green-900/20',
  'bg-blue-50': 'dark:bg-blue-900/20',
  'bg-yellow-50': 'dark:bg-yellow-900/20',
  'bg-indigo-50': 'dark:bg-indigo-900/20',
  
  // Text colors
  'text-gray-900': 'dark:text-gray-100',
  'text-gray-800': 'dark:text-gray-200',
  'text-gray-700': 'dark:text-gray-300',
  'text-gray-600': 'dark:text-gray-400',
  'text-gray-500': 'dark:text-gray-500',
  'text-gray-400': 'dark:text-gray-600',
  'text-black': 'dark:text-white',
  
  // Borders
  'border-gray-200': 'dark:border-gray-700',
  'border-gray-300': 'dark:border-gray-600',
  'border-gray-400': 'dark:border-gray-500',
  
  // Divide colors (for borders between elements)
  'divide-gray-200': 'dark:divide-gray-700',
  'divide-gray-300': 'dark:divide-gray-600',
  
  // Ring colors (for focus states)
  'ring-gray-200': 'dark:ring-gray-700',
  'ring-gray-300': 'dark:ring-gray-600',
  
  // Placeholder colors
  'placeholder-gray-400': 'dark:placeholder-gray-600',
  'placeholder-gray-500': 'dark:placeholder-gray-500',
};

// Hover state mappings
const HOVER_MAPPINGS = {
  'hover:bg-gray-50': 'dark:hover:bg-gray-800',
  'hover:bg-gray-100': 'dark:hover:bg-gray-700',
  'hover:bg-gray-200': 'dark:hover:bg-gray-600',
  'hover:text-gray-900': 'dark:hover:text-gray-100',
  'hover:text-gray-800': 'dark:hover:text-gray-200',
  'hover:text-gray-700': 'dark:hover:text-gray-300',
  'hover:border-gray-300': 'dark:hover:border-gray-600',
};

// Focus state mappings
const FOCUS_MAPPINGS = {
  'focus:border-indigo-500': 'dark:focus:border-indigo-400',
  'focus:ring-indigo-500': 'dark:focus:ring-indigo-400',
};

// Shadow adjustments for dark mode
const SHADOW_MAPPINGS = {
  'shadow-sm': 'dark:shadow-lg dark:shadow-gray-900/30',
  'shadow': 'dark:shadow-xl dark:shadow-gray-900/30',
  'shadow-md': 'dark:shadow-xl dark:shadow-gray-900/40',
  'shadow-lg': 'dark:shadow-2xl dark:shadow-gray-900/50',
  'shadow-xl': 'dark:shadow-2xl dark:shadow-gray-900/60',
};

// Combine all mappings
const ALL_MAPPINGS = {
  ...COLOR_MAPPINGS,
  ...HOVER_MAPPINGS,
  ...FOCUS_MAPPINGS,
  ...SHADOW_MAPPINGS,
};

// Statistics tracking
let stats = {
  filesProcessed: 0,
  filesModified: 0,
  classesAdded: 0,
  errors: [],
};

/**
 * Process a single Vue file
 */
function processVueFile(filePath) {
  if (options.verbose) {
    console.log(`Processing: ${filePath}`);
  }

  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let originalContent = content;
    let modified = false;
    let fileClassesAdded = 0;

    // Find all class attributes in the template section
    const templateMatch = content.match(/<template>([\s\S]*?)<\/template>/);
    if (!templateMatch) {
      if (options.verbose) {
        console.log(`  No template section found in ${filePath}`);
      }
      return;
    }

    let template = templateMatch[1];
    let originalTemplate = template;

    // Process class attributes
    template = template.replace(
      /class="([^"]*)"/g,
      (match, classes) => {
        let updatedClasses = classes;
        let classesChanged = false;

        // Split classes and process each one
        let classList = classes.split(/\s+/);
        let newClasses = [];

        for (let className of classList) {
          // Check if this class needs a dark mode variant
          if (ALL_MAPPINGS[className]) {
            const darkClass = ALL_MAPPINGS[className];
            // Check if dark class is not already present
            if (!classes.includes(darkClass)) {
              newClasses.push(darkClass);
              classesChanged = true;
              fileClassesAdded++;
            }
          }
        }

        if (classesChanged) {
          updatedClasses = classes + ' ' + newClasses.join(' ');
          modified = true;
        }

        return `class="${updatedClasses}"`;
      }
    );

    // Process :class bindings (dynamic classes)
    template = template.replace(
      /:class="([^"]*)"/g,
      (match, binding) => {
        // For dynamic classes, add a comment suggesting dark mode classes
        if (binding.includes('?') && !binding.includes('dark:')) {
          // This is a conditional class, add a comment
          const comment = '<!-- TODO: Add dark mode variant for conditional classes -->';
          if (!template.includes(comment)) {
            return match + ' ' + comment;
          }
        }
        return match;
      }
    );

    if (modified) {
      // Backup original file if requested
      if (options.backup && !options.dryRun) {
        fs.writeFileSync(filePath + '.backup', originalContent);
      }

      // Replace template in content
      content = content.replace(
        /<template>[\s\S]*?<\/template>/,
        `<template>${template}</template>`
      );

      if (options.dryRun) {
        console.log(`Would modify: ${filePath}`);
        console.log(`  Classes to add: ${fileClassesAdded}`);
        if (options.verbose) {
          console.log('  Changes:');
          // Show a diff-like output
          const originalLines = originalTemplate.split('\n');
          const newLines = template.split('\n');
          for (let i = 0; i < Math.max(originalLines.length, newLines.length); i++) {
            if (originalLines[i] !== newLines[i]) {
              if (originalLines[i]) console.log(`  - ${originalLines[i]}`);
              if (newLines[i]) console.log(`  + ${newLines[i]}`);
            }
          }
        }
      } else {
        fs.writeFileSync(filePath, content);
        console.log(`✓ Modified: ${filePath} (${fileClassesAdded} dark classes added)`);
      }

      stats.filesModified++;
      stats.classesAdded += fileClassesAdded;
    } else if (options.verbose) {
      console.log(`  No changes needed for ${filePath}`);
    }

    stats.filesProcessed++;
  } catch (error) {
    console.error(`✗ Error processing ${filePath}: ${error.message}`);
    stats.errors.push({ file: filePath, error: error.message });
  }
}

/**
 * Process all Vue files in a directory
 */
function processDirectory(dir) {
  const pattern = path.join(dir, '**/*.vue');
  const files = glob.sync(pattern, { ignore: ['**/node_modules/**', '**/*.backup'] });

  console.log(`\n🌙 Dark Mode Class Application Tool`);
  console.log(`${'='.repeat(50)}`);
  console.log(`Directory: ${dir}`);
  console.log(`Mode: ${options.dryRun ? 'DRY RUN' : 'LIVE'}`);
  console.log(`Files found: ${files.length}`);
  console.log(`${'='.repeat(50)}\n`);

  if (files.length === 0) {
    console.log('No Vue files found in the specified directory.');
    return;
  }

  // Process each file
  files.forEach(file => processVueFile(file));

  // Print summary
  console.log(`\n${'='.repeat(50)}`);
  console.log('📊 Summary');
  console.log(`${'='.repeat(50)}`);
  console.log(`Files processed: ${stats.filesProcessed}`);
  console.log(`Files modified: ${stats.filesModified}`);
  console.log(`Dark classes added: ${stats.classesAdded}`);
  
  if (stats.errors.length > 0) {
    console.log(`\n⚠️  Errors: ${stats.errors.length}`);
    stats.errors.forEach(err => {
      console.log(`  - ${err.file}: ${err.error}`);
    });
  }

  if (options.dryRun) {
    console.log('\n📝 This was a dry run. No files were actually modified.');
    console.log('Remove --dry-run flag to apply changes.');
  }

  if (options.backup && !options.dryRun && stats.filesModified > 0) {
    console.log('\n💾 Backup files created with .backup extension');
  }
}

/**
 * Create an analysis report without modifying files
 */
function analyzeDirectory(dir) {
  const pattern = path.join(dir, '**/*.vue');
  const files = glob.sync(pattern, { ignore: ['**/node_modules/**', '**/*.backup'] });
  
  let report = {
    totalFiles: files.length,
    filesNeedingDarkMode: [],
    classesFound: {},
    suggestions: [],
  };

  files.forEach(file => {
    const content = fs.readFileSync(file, 'utf8');
    const templateMatch = content.match(/<template>([\s\S]*?)<\/template>/);
    
    if (templateMatch) {
      const template = templateMatch[1];
      let needsDarkMode = false;
      
      // Check for classes that could have dark variants
      Object.keys(COLOR_MAPPINGS).forEach(className => {
        const regex = new RegExp(`\\b${className}\\b`, 'g');
        const matches = template.match(regex);
        if (matches) {
          needsDarkMode = true;
          if (!report.classesFound[className]) {
            report.classesFound[className] = 0;
          }
          report.classesFound[className] += matches.length;
        }
      });
      
      if (needsDarkMode) {
        // Check if file already has any dark: classes
        const hasDarkClasses = /dark:/.test(template);
        report.filesNeedingDarkMode.push({
          file: file,
          hasDarkClasses: hasDarkClasses,
          priority: hasDarkClasses ? 'partial' : 'full',
        });
      }
    }
  });

  // Generate report
  console.log('\n📊 Dark Mode Analysis Report');
  console.log(`${'='.repeat(50)}`);
  console.log(`Total Vue files: ${report.totalFiles}`);
  console.log(`Files needing dark mode: ${report.filesNeedingDarkMode.length}`);
  
  console.log('\n📈 Most Common Classes Needing Dark Variants:');
  const sortedClasses = Object.entries(report.classesFound)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);
  
  sortedClasses.forEach(([className, count]) => {
    console.log(`  ${className}: ${count} occurrences → ${COLOR_MAPPINGS[className]}`);
  });
  
  console.log('\n📁 Priority Files (no dark classes yet):');
  report.filesNeedingDarkMode
    .filter(f => f.priority === 'full')
    .slice(0, 10)
    .forEach(f => {
      console.log(`  - ${f.file}`);
    });

  return report;
}

// Main execution
if (require.main === module) {
  // Check if analysis mode
  if (args.includes('--analyze')) {
    analyzeDirectory(options.dir);
  } else {
    processDirectory(options.dir);
  }
}

module.exports = { processVueFile, processDirectory, analyzeDirectory };