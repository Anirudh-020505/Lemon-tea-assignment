import forms from '@tailwindcss/forms';
import containerQueries from '@tailwindcss/container-queries';


export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      "colors": {
        "background": "#111319",
        "secondary-fixed": "#6ffbbe",
        "inverse-surface": "#e2e2eb",
        "surface-elevated": "#161922",
        "on-secondary": "#003824",
        "on-primary-fixed": "#07006c",
        "primary-fixed": "#e1e0ff",
        "surface-container-high": "#282a30",
        "tertiary-fixed-dim": "#ffb783",
        "surface-bright": "#373940",
        "surface-tint": "#c0c1ff",
        "surface-container-low": "#191b22",
        "on-tertiary": "#4f2500",
        "surface-dim": "#111319",
        "on-tertiary-fixed-variant": "#703700",
        "inverse-on-surface": "#2e3037",
        "text-muted": "#94A3B8",
        "on-primary-fixed-variant": "#2f2ebe",
        "on-primary": "#1000a9",
        "on-error": "#690005",
        "secondary-fixed-dim": "#4edea3",
        "tertiary-container": "#d97721",
        "secondary-container": "#00a572",
        "on-surface-variant": "#c7c4d7",
        "on-secondary-container": "#00311f",
        "on-surface": "#e2e2eb",
        "primary-container": "#8083ff",
        "border-low-opacity": "rgba(255, 255, 255, 0.08)",
        "on-primary-container": "#0d0096",
        "surface-container-lowest": "#0c0e14",
        "secondary": "#4edea3",
        "on-background": "#e2e2eb",
        "primary": "#c0c1ff",
        "on-tertiary-container": "#452000",
        "on-secondary-fixed": "#002113",
        "tertiary": "#ffb783",
        "inverse-primary": "#494bd6",
        "surface-container-highest": "#33343b",
        "outline": "#908fa0",
        "tertiary-fixed": "#ffdcc5",
        "surface": "#111319",
        "warning-amber": "#F59E0B",
        "on-error-container": "#ffdad6",
        "error": "#ffb4ab",
        "on-tertiary-fixed": "#301400",
        "surface-variant": "#33343b",
        "outline-variant": "#464554",
        "on-secondary-fixed-variant": "#005236",
        "primary-fixed-dim": "#c0c1ff",
        "error-container": "#93000a",
        "surface-container": "#1e1f26"
      },
      "borderRadius": {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      "spacing": {
        "gutter": "16px",
        "section-padding": "24px",
        "max-content-width": "900px",
        "sidebar-width": "280px",
        "stack-gap": "12px"
      },
      "fontFamily": {
        "body-sm": ["Inter"],
        "headline-md": ["Inter"],
        "headline-lg": ["Inter"],
        "body-md": ["Inter"],
        "label-caps": ["JetBrains Mono"],
        "code-snippet": ["JetBrains Mono"]
      },
      "fontSize": {
        "body-sm": ["13px", { "lineHeight": "20px", "fontWeight": "400" }],
        "headline-md": ["18px", { "lineHeight": "24px", "letterSpacing": "-0.01em", "fontWeight": "600" }],
        "headline-lg": ["24px", { "lineHeight": "32px", "letterSpacing": "-0.02em", "fontWeight": "600" }],
        "body-md": ["14px", { "lineHeight": "22px", "fontWeight": "400" }],
        "label-caps": ["11px", { "lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "500" }],
        "code-snippet": ["13px", { "lineHeight": "20px", "fontWeight": "400" }]
      }
    }
  },
  plugins: [
    forms,
    containerQueries
  ]
};
