const express = require('express');
const registrationRoutes = require('./routes/registration');
const authenticationRoutes = require('./routes/authentication');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.use('/register', registrationRoutes);
app.use('/auth', authenticationRoutes);

app.listen(port, () => {
    console.log(`Authentication service running on http://localhost:${port}`);
});

