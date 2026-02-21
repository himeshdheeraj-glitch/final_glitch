const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;
const DB_FILE = path.join(__dirname, 'database.json');

app.use(cors());
app.use(bodyParser.json());

// Initialize empty DB if it doesn't exist
if (!fs.existsSync(DB_FILE)) {
    fs.writeFileSync(DB_FILE, JSON.stringify({ users: [] }, null, 2));
}

const readDB = () => JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
const writeDB = (data) => fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));

// Registration Endpoint
app.post('/register', (req, res) => {
    const { username, email, blood_type, password } = req.body;

    if (!username || !email || !password) {
        return res.status(400).json({ error: "Missing required fields" });
    }

    const db = readDB();

    // Check if user already exists (by email or username)
    if (db.users.some(u => u.username === username || u.email === email)) {
        return res.status(409).json({ error: "User or Email already exists" });
    }

    const newUser = {
        id: Date.now().toString(),
        username,
        email,
        blood_type: blood_type || "Unknown",
        password // Storing plaintext for the hackathon prototype per user request ease
    };

    db.users.push(newUser);
    writeDB(db);

    res.status(201).json({ message: "Registration successful", user: newUser });
});

// Login Endpoint
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: "Username and password required" });
    }

    const db = readDB();
    const user = db.users.find(u => u.username === username && u.password === password);

    if (user) {
        res.status(200).json({ message: "Login successful", user });
    } else {
        res.status(401).json({ error: "Invalid credentials. Have you registered?" });
    }
});

// Get All Users Endpoint (For Community Page)
app.get('/users', (req, res) => {
    const db = readDB();
    // Return users without their passwords
    const safeUsers = db.users.map(u => ({
        id: u.id,
        username: u.username,
        email: u.email,
        blood_type: u.blood_type
    }));
    res.status(200).json(safeUsers);
});

app.listen(PORT, () => {
    console.log(`✅ Authentication Server running gracefully on http://localhost:${PORT}`);
});
