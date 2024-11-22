const path = require("path");

module.exports = {
  entry: "./cv_personal_page/frontend/index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "./cv_personal_page/static"),
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: [
          "style-loader",
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: [[require("tailwindcss"), require("autoprefixer")]],
              },
            },
          },
        ],
      },
    ],
  },
};
