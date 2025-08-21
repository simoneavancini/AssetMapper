const express = require('express');
const mongoose = require('mongoose');
const objectRoutes = require('./routes/objects.js');

const app = express();
app.use(express.json());

// MongoDB connection
const uri = `mongodb://${process.env.DB_HOST}:27017/autorecon`;
mongoose.connect(uri)
  .then(() => console.log("Connected to MongoDB"))
  .catch(err => console.error("MongoDB connection error:", err));

// Routes
app.use('/', objectRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Mongoose DB Adapter running on port ${PORT}`));

