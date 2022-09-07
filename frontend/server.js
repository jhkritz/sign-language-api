// Based on the code given in the Heroku Nodejs docs
// https://devcenter.heroku.com/articles/getting-started-with-nodejs#push-local-changes
// And the README.md linked below
// https://github.com/bripkens/connect-history-api-fallback
const express = require('express')
const path = require('path')
const midware = require('connect-history-api-fallback');
const PORT = process.env.PORT || 5000

const expressApp = express();
expressApp.use(midware);
expressApp.use(express.static(path.join(__dirname, 'dist')));
expressApp.get('*', (req, res) => res.sendFile(__dirname, '/dist/index.html'));
expressApp.listen(PORT, () => console.log(`Listening on port ${PORT}`));
