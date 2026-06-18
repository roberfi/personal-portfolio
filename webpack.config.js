const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

module.exports = {
  entry: "./src/frontend/index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "./src/static"),
    library: {
      type: "module",
    },
  },
  experiments: {
    outputModule: true,
  },
  optimization: {
    minimizer: [
      "...", // Keep webpack's default JS minimizer (Terser) and add CSS minification.
      new CssMinimizerPlugin(),
    ],
  },
  plugins: [new MiniCssExtractPlugin({ filename: "bundle.css" })],
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: [
          MiniCssExtractPlugin.loader,
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
