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
        return res.status(400).json({ success: false, message: 'The field "email" must be a non-empty string, in email format' });
    }

    if (!req.body.username) {
        return res.status(400).json({ success: false, message: 'Username can not be empty' });
    }
    // Check if user already exists
    var user = await User.findOne({ username: req.body.username });
    if (user) {
        return res.status(400).json({ success: false, message: 'Username already registered' });
    }

    // Check password
    if (!req.body.password || typeof req.body.password !== 'string') {
        return res.status(400).json({ success: false, message: 'Password must be a non-empty string' });
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
    res.status(201).json({ success: true, message: 'User successfully created' });
});

/*
 * Return users list
 */
router.get('', async (req, res) => {
    const users = await User.find({}, '-password -__v -_id');
    return res.json(users);
});

/*
 * Return user info
 */
router.get('/:username', async (req, res) => {
    const user = await User.findOne({ username: req.params.username }, '-password -__v -_id');

    if (!user) {
        return res.status(404).json({ success: false, message: 'User not found' })
    }

    return res.status(200).json(user);
});

/*
 * Verify user's password
 */
router.post('/verify/:username', async (req, res) => {
    const user = await User.findOne({ username: req.params.username });

    if (!user) {
		return res.status(404).json({ success: false, message: 'User not found' });
    }

    if (!req.body.password) {
        return res.status(400).json({ success: false, message: 'Password must be a non-empty string' });
	}

	const isValid = await bcrypt.compare(req.body.password, user.password);
	if (isValid) {
		return res.status(200).json({ success: true, message: 'Login successful!' });
	} else {
		return res.status(401).json({ success: false, message: 'Invalid password' });
	}

    return res.status(200).json(user);
});

function isValidEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}


module.exports = router;
