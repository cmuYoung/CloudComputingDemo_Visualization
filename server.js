const express = require('express');
const httpProxy = require('http-proxy');
const path = require('path');
const app = express();

// Create a new HTTP proxy instance
const proxy = httpProxy.createProxyServer({ changeOrigin: true });

// Serve static files from the public directory
app.use(express.static('public'));

// Endpoint at the root
app.get('/', (req, res) => {
  res.send('Hello World!');
});


// Route to serve the HTML file
app.get('/gr', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/index_gr.html'));
});

// Route to serve the HTML file
app.get('/gr2', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/index_gr2.html'));
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

