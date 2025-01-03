const { defineConfig } = require('@vue/cli-service');

module.exports = {
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      fallback: {
        stream: require.resolve('stream-browserify'),
        assert: require.resolve('assert'),
        util: require.resolve('util'),
        zlib: require.resolve('browserify-zlib'),
      },
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          loader: 'babel-loader',
          include: /node_modules\/@plotly\/mapbox-gl\/dist/,
          options: {
            compact: false, // Disable minification for large files
          },
        },
      ],
    },
  },
};

