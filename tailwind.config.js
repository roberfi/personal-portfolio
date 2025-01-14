/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "src/templates/**/*.html",
    "src/frontend/**/*.js",
    "src/*/templates/**/*.html",
  ],
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: [
      {
        portfolio: {
          primary: "#fdba74",
          secondary: "#93c5fd",
          accent: "#f97316",
          neutral: "#111827",
          "base-100": "#4b5563",
          info: "#08638b",
          success: "#96c283",
          warning: "#fef08a",
          error: "#f87171",
        },
      },
    ],
  },
};
