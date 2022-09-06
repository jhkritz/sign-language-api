const express = require('express')
const path = require('path')
const PORT = process.env.PORT || 5000

const expressApp = express();
expressApp.use(express.static(path.join(__dirname, 'dist')));
expressApp.get('*', (req, res) => res.sendFile(__dirname, '/dist/index.html'));
expressApp.listen(PORT, () => console.log(`Listening on port ${PORT}`));
/*
	.set('views', path.join(__dirname, 'views'))
	.set('view engine', 'ejs')
	.get('/', (req, res) => res.render('pages/index'))
	.listen(PORT, () => console.log(`Listening on ${ PORT }`))
		 */
