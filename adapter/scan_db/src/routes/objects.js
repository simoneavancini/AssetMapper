const express = require('express');
const StoredObject = require('../models/storedObject');

const router = express.Router();

// Store JSON object
router.post("/scans", async (req, res) => {
  try {
    const doc = new StoredObject(req.body);
    const saved = await doc.save();
    res.json({ success: true, id: saved._id });
  } catch (err) {
    res.status(400).json({ success: false, error: err.message });
  }
});

// Get by ID
router.get("/scans/:id", async (req, res) => {
  try {
    const doc = await StoredObject.findById(req.params.id);
    if (!doc) return res.status(404).json({ success: false, message: "Not found" });
    res.json({ success: true, doc });
  } catch (err) {
    res.status(400).json({ success: false, error: err.message });
  }
});

// List all
router.get("/scans", async (req, res) => {
  try {
    const docs = await StoredObject.find({}, "domain createdAt");
    res.json(docs);
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;

