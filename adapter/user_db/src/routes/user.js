const express = require('express');
const router = express.Router();
const User = require('../models/user'); // get our mongoose model
const bcrypt = require('bcrypt'); // used for password hashing


/*
 * Register a new user
 */
router.post('', async function(req, res) {
    // Check email
    if (!isValidEmail(req.body.email)) {
        return res.status(400).json({ error: 'The field "email" must be a non-empty string, in email format' });
    }

    // Check if user already exists
    if (!req.body.username) {
        return res.status(400).json({ error: 'Username can not be empty' });
    }
    var user = await User.findOne({ username: req.body.username });
    if (user) {
        return res.status(400).json({ error: 'Username already registered' });
    }

    // Check password
    if (!req.body.password || typeof req.body.password !== 'string') {
        return res.status(400).json({ error: 'Password must be a non-empty string' });
    }

    // Create new user
    user = new User({
        username: req.body.username,
        email: req.body.email
    });

    // Create password hash
    const hash = await bcrypt.hash(req.body.password, 10)
    if (hash) {
        user.password = hash;
        user = await user.save();
    } else {
        res.status(500).json({ success: false, message: 'Something went wrong' });
    }

    // Send the link of the new resource
    res.status(201).json({ message: "user created" });
});

/*
 * Return users list
 */
router.get('', async (req, res) => {
    const users = await User.find({}, '-password -__v');
    return res.json(users);
});

/*
 * Return user info
 */
router.get('/:userId', async (req, res) => {
    const user = await User.findById(req.params.userId);

    if (!user) {
        return res.status(404).json({ success: false, message: 'User not found' })
    }

    return res.status(200).json(user);
});

function isValidEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}


module.exports = router;
