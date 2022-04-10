
module.exports = {
    module: {
      rules: [
        {
          test: /\.py$/,
          loader: 'py-loader',
          options: {
            compiler: 'transcrypt'
          }
        }
      ]
    }
  }