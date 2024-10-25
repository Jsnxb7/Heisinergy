const express = require('express');
const path = require('path');

const app = express();
const PORT = 5000;

// Serve static files from the css and img folders
app.use(express.static(path.join(__dirname)));

// Route for the index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
