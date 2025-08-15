const express = require('express');
const router = express.Router();
const fetch = require("node-fetch");

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
    const userexists = await fetch(`${process.env.DB_ADAPTER_URL}/users/${req.body.username}`);
    if (userexists.status === 200) {
        const userData = await userResp.json();
        if (userData.username) {
            return res.status(400).json({ success: false, message: 'Username already registered' });
        }
    }

    // Check password
    if (!req.body.password || typeof req.body.password !== 'string') {
        return res.status(400).json({ success: false, message: 'Password must be a non-empty string' });
    }

    // Create new user
    const response = await fetch(`${process.env.DB_ADAPTER_URL}/users/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: req.body.username,
            email: req.body.email,
            password: req.body.password
        })
    });

    const responseData = await response.json();
    if (responseData.success) {
        return res.json({ success: true, message: 'Registration successful' });
    } else {
        return res.status(500).json(responseData);
    }
});

function isValidEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}


module.exports = router;
