const express = require('express');
const router = express.Router();
const fetch = require("node-fetch");
const jwt = require('jsonwebtoken'); // used to create, sign, and verify tokens
const bcrypt = require('bcrypt'); // used for password hashing

/*
 * Authenticate the user and generate a new token
 */
router.post('', async function(req, res) {
    if (!req.body.username) {
        return res.status(403).json({ success: false, message: 'Username is required' });
    }

    if (!req.body.password) {
        return res.status(403).json({ success: false, message: 'Password is required' });
    }

    // Search the user
    const response = await fetch(`http://${process.env.DB_ADAPTER_HOST}:${process.env.DB_ADAPTER_PORT}/user/${req.body.username}`);

    // User not found
    if (!response.body.success) {
        return res.status(404).json({ success: false, message: 'User not found' });
    }

    const user = response.body.user;

    // Check password
    const passwordCorrect = await bcrypt.compare(req.body.password, user.password);
    if (!passwordCorrect) {
        return res.status(403).json({ success: false, message: 'Wrong password' });
    }

    // User authenticated -> create a token
    var payload = {
        username: user.username,
        email: user.email
    }
    var options = { expiresIn: 86400 } // expires in 24 hours
    var token = jwt.sign(payload, process.env.JWT_SECRET, options);

    res.json({
        success: true,
        message: 'Enjoy your token!',
        token: token
    });
});

module.exports = router;
