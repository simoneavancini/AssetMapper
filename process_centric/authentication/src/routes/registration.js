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
    const userexists = await fetch(`http://${process.env.DB_ADAPTER_HOST}:${process.env.DB_ADAPTER_PORT}/user/${req.body.username}`);
    if (userexists.body.success) {
        return res.status(400).json({ success: false, message: 'Username already registered' });
    }

    // Check password
    if (!req.body.password || typeof req.body.password !== 'string') {
        return res.status(400).json({ success: false, message: 'Password must be a non-empty string' });
    }

    // Create new user
    const response = await fetch(`http://${process.env.DB_ADAPTER_HOST}:${process.env.DB_ADAPTER_PORT}/user/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json" // Specify the content type as JSON
        },
        body: JSON.stringify({
            username: req.body.username,
            email: req.body.email,
            password: req.body.password
        })
    });

    response.json().then(data => { console.log(data) })
    if (response.body.success) {
        return res.json({ success: true, message: 'Registration successful' });
    }
    return res.status(500).json({ success: false, message: 'Something went wrong' });
});

function isValidEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}


module.exports = router;
