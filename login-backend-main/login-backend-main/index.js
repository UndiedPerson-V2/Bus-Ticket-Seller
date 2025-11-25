// index.js (Backend Server)
const express = require('express');
const cors = require('cors');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg'); // ตัวเชื่อม PostgreSQL

const app = express();
app.use(cors());
app.use(express.json()); // ให้เซิร์ฟเวอร์อ่าน JSON ได้

// ----------------------------------------------------
// ** สำคัญ: แก้ไขข้อมูลการเชื่อมต่อ DB ของคุณตรงนี้ **
// ----------------------------------------------------
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'postgres', // หรือชื่อ DB ที่คุณสร้าง (ถ้าใช้ 'postgres' ก็ได้)
    password: 'YOUR_PASSWORD_GOES_HERE', // << ใส่รหัสผ่าน PostgreSQL ของคุณตรงนี้!
    port: 5432,
});

const JWT_SECRET = "YOUR_SUPER_SECRET_KEY_12345"; // ห้ามใช้คีย์นี้จริง

// --- สร้าง Endpoint สำหรับ "สมัครสมาชิก" (จำเป็นต้องมี) ---
// แอปจะยิงมาที่ /register
app.post('/register', async (req, res) => {
    try {
        const { username, password, fullName } = req.body;

        // 1. เข้ารหัส (Hash) รหัสผ่านก่อนเก็บ
        const salt = await bcrypt.genSalt(10);
        const passwordHash = await bcrypt.hash(password, salt);

        // 2. เก็บลง DB
        const newUser = await pool.query(
            "INSERT INTO users (username, password_hash, full_name) VALUES ($1, $2, $3) RETURNING id, username, full_name",
            [username, passwordHash, fullName]
        );

        res.status(201).json(newUser.rows[0]);
    } catch (err) {
        console.error(err.message);
        res.status(500).json({ message: "Server error" });
    }
});

// --- นี่คือ Endpoint ที่ทำตามรูปของคุณ! ---
// แอปจะยิงมาที่ /login
app.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        // 1. (ตามรูป) เช็คว่ามี Username นี้ใน DB มั๊ย?
        const userResult = await pool.query("SELECT * FROM users WHERE username = $1", [username]);

        if (userResult.rows.length === 0) {
            // (ตามรูป) ถ้าไม่มี -> ไม่ต้องไปต่อ
            return res.status(401).json({ message: "ไม่พบผู้ใช้นี้ (Invalid Credentials)" });
        }

        const user = userResult.rows[0]; // ข้อมูลผู้ใช้จาก DB

        // 2. (ตามรูป) เช็ค Password ... โดยใช้ bcrypt เทียบ
        const isMatch = await bcrypt.compare(password, user.password_hash);

        if (!isMatch) {
            // (ตามรูป) ถ้าไม่ถูก -> ไม่ต้องไปต่อ
            return res.status(401).json({ message: "รหัสผ่านไม่ถูกต้อง (Invalid Credentials)" });
        }

        // 3. (ตามรูป) ถ้า Login ถูกต้อง -> ดึงข้อมูล + ส่งไปหน้าถัดไป
        // เราจะสร้าง "Token" (บัตรผ่าน) และส่งกลับไป
        const token = jwt.sign(
            { id: user.id, username: user.username },
            JWT_SECRET,
            { expiresIn: '1h' } // Token มีอายุ 1 ชั่วโมง
        );

        // ส่ง Token และ "ชื่อคนขับ" กลับไปให้แอป
        res.json({
            token,
            user: {
                id: user.id,
                username: user.username,
                fullName: user.full_name // (ตามรูป) ดึงชื่อคนขับ
            }
        });

    } catch (err) {
        console.error(err.message);
        res.status(500).json({ message: "Server error" });
    }
});


// สั่งให้เซิร์ฟเวอร์เริ่มทำงาน
const PORT = 4000;
app.listen(PORT, () => {
    console.log(`Backend server กำลังทำงานที่ http://localhost:${PORT}`);
});