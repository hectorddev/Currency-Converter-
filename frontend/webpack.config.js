const path = require('path');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: './src/index.js', //Punto de entrada
  output: {
    path: path.resolve(__dirname, 'dist'), //Creamos una carpeta dist en la raiz
    filename: 'bundle.js', //Llamamos al archivo así
    publicPath: '/'
  }, //Hacia donde se va a enviar nuestro proyecto
  resolve: {
    extensions: ['.js', 'jsx'],
  }, //Que extensiones va a leer. Que vamos a utilizar.
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.html$/,
        use: [
          {
            loader: 'html-loader',
          },
        ],
      },
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader',
          },
        ],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: './index.html',
    }),
    new MiniCssExtractPlugin({
      filename: 'assets/[name].css',
    })
  ],

  devServer: {
    static: path.join(__dirname, 'dist'), //Cambio de contentBase a static en la versión 4.0
    compress: true,
		port: 3005,
    historyApiFallback: true,
    open: true,
  }, //Permite crear un servidor de manera local para poder trabajar
}