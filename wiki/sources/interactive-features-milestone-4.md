---
title: "Interactive Features - Milestone 4: Campaign Wizard, Enhanced Modals, Search/Filter"
type: source
tags: [css, campaign-wizard, ui-components, modern-mode, milestone-4, modal, search, filter]
source_file: "raw/interactive-features-milestone-4.md"
sources: []
last_updated: 2026-04-08
---

## Summary
CSS styles for Milestone 4 interactive features including the Campaign Wizard multi-step flow, enhanced modal components, and search/filter UI elements. All styles are feature-flag controlled via `.modern-mode` or `body[data-interface-mode='modern']` selector.

## Key Claims
- **Campaign Wizard**: Multi-step form with progress bar, step indicators, and animated transitions between steps
- **Wizard Progress**: Visual progress bar with gradient fill and smooth width transitions
- **Step Indicators**: Interactive step circles with active/completed states, labels, and hover effects
- **Personality Cards**: Selectable cards for campaign personality selection with hover lift and selection highlighting
- **Campaign Type Cards**: Radio-button backed cards for campaign type selection with icon, title, and description
- **Option Cards**: Generic option selection cards with icons and descriptions
- **Campaign Preview**: Gradient background card showing campaign configuration summary
- **Feature Gating**: All styles gated on `.modern-mode` or `data-interface-mode='modern'` attribute

## Key CSS Patterns
- **Transitions**: 0.3s ease transitions on interactive elements
- **Animations**: fadeInUp keyframe for wizard step transitions
- **Gradients**: Linear gradient progress bars (#007bff to #0056b3)
- **Backdrop Filter**: blur(10px) for frosted glass effect
- **Transforms**: Scale and translate transforms for hover/active states
- **Box Shadows**: Layered shadows for depth on hover states

## Connections
- [[ModernCSSFoundationDesignSystem]] — foundation design tokens used here
- [[ArcaneScholarTheme]] — fantasy theme integration for modern mode
- [[EnhancedComponentsCSS]] — related enhanced component styles

## Contradictions
- None identified
