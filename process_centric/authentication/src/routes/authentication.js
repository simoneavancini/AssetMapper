const express = require('express');
const router = express.Router();
const fetch = require("node-fetch");
const jwt = require('jsonwebtoken'); // used to create, sign, and verify tokens
const JWT_SECRET = process.env.JWT_SECRET;

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
    const response = await fetch(`${process.env.DB_ADAPTER_URL}/users/verify/${req.body.username}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                password: req.body.password
            })
        });
    if (response.status === 401 || response.status === 404) {
        return res.status(403).json({ success: false, message: 'Invalid username or password' });
    }

    if (response.status !== 200) {
        return res.status(500).json({ success: false, message: 'Someting went wrong' });
    }

    const userdata = await fetch(`${process.env.DB_ADAPTER_URL}/users/${req.body.username}`);
    const responseData = await userdata.json();
    const email = responseData.email;

    // User authenticated -> create a token
    var payload = {
        username: req.body.username,
        email: email
    }
    var options = { algorithm: 'HS256', expiresIn: 86400 } // expires in 24 hours
    try {
        var token = jwt.sign(payload, JWT_SECRET, options);
    } catch (error) {
        console.error("JWT Generation Error:", error);
        return res.status(500).json({
            success: false,
            message: 'Error generating JWT token'
        });
    }

    res.json({
        success: true,
        message: 'Token successfully generated',
        token: token
    });
});

module.exports = router;
