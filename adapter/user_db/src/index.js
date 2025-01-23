require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const User = require('./models/user');
const userRoutes = require('./routes/user');

const app = express();
const port = process.env.PORT || 3000;
process.env.SECRET = process.env.SECRET || 'd2e2633f018a73b66297cf8be9ee002a';

app.use(express.json());

mongoose.connect(`mongodb://${process.env.DB_HOST}:27017/autorecon`)
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('Failed to connect to MongoDB', err));

app.use('/user', userRoutes);

app.listen(port, () => {
    console.log(`User_db adapter service running on http://localhost:${port}`);
});

