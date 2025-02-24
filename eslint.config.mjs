import globals from "globals";
import pluginJs from "@eslint/js";

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    ignores: ["src/static/"],
  },
  {
    languageOptions: { globals: globals.browser },
  },
  {
    files: ["tailwind.config.js", "webpack.config.js"],
    languageOptions: {
      globals: globals.node,
    },
  },
  pluginJs.configs.recommended,
];
