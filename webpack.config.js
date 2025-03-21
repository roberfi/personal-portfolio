const path = require("path");

module.exports = {
  entry: "./src/frontend/index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "./src/static"),
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
                plugins: [
                  [require("@tailwindcss/postcss"), require("autoprefixer")],
                ],
              },
            },
          },
        ],
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        type: "asset/resource",
      },
    ],
  },
};
