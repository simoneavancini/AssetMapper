const express = require("express");
const fetch = require("node-fetch");
const jwt = require("jsonwebtoken");

const app = express();
app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRET;

// Business logic services
const ATTACK_SURFACE = process.env.ATTACK_SURFACE;
const TECH_DETECTION = process.env.TECH_DETECTION;
const EMPLOYEE_ANALYSIS = process.env.EMPLOYEE_ANALYSIS;


// JWT Middleware
function authenticateJWT(req, res, next) {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
        return res.status(401).json({ error: "Missing or invalid Authorization header" });
    }

    const token = authHeader.split(" ")[1];

    try {
        const payload = jwt.verify(token, JWT_SECRET);
        req.user = payload;
        next();
    } catch (err) {
        return res.status(403).json({ error: "Invalid or expired token" });
    }
}

// Scan endpoint
app.get("/host", authenticateJWT, async(req, res) => {
    const { domain } = req.query;
    if (!domain) {
        return res.status(400).json({ error: "Missing domain" });
    }

  try {
    // Inline service calls
    const [attackSurface, technologies, employees] = await Promise.all([
      fetch(`${ATTACK_SURFACE}/?target=${domain}`)
            .then(r => r.json()),

      fetch(`${TECH_DETECTION}/?target=${domain}`)
            .then(r => r.json()),

      fetch(`${EMPLOYEE_ANALYSIS}/?domain=${domain}`)
            .then(r => r.json()),
    ]);

    res.json({
      domain,
      attack_surface: attackSurface,
      technologies,
      employees,
    });
  } catch (err) {
    console.error(err);
    res.status(502).json({ error: "Failed to aggregate results" });
  }
});


const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Scan host orchestrator running on port ${PORT}`);
});

