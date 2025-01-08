const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const { MongoClient } = require('mongodb');
const router = express.Router();
const url = "mongodb://mongo:27017/booking-service";
//const url = process.env.MONGO_URI || "mongodb://mongo:27017/booking-service";
//const url = "mongodb://127.0.0.1:27017/booking-service";
const dbName = "booking-service";
const collectionName1 = "users";

router.post('/register', async (req, res) => {
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
        return res.status(400).send('Username, email, and password are required');
    }

    try {
        const client = await MongoClient.connect(url);
        const db = client.db(dbName);
        const usersCollection = db.collection(collectionName1);

        const existingUser = await usersCollection.findOne({ email });
        if (existingUser) {
            console.log('Email is already registered');
            client.close();
        }

        const result = await usersCollection.insertOne({
            username,
            email,
            password,  
        });

        client.close();

        return res.status(201).send('User registered successfully');
    } catch (err) {
        console.error(err);
        return res.status(500).send('Internal server error');
    }
});

router.get('/login', async (req, res) => {
    const { username, password } = req.query;

    if (!username || !password) {
        return res.status(400).send('Username and password are required');
    }

    try {
        const client = await MongoClient.connect(url);
        const db = client.db(dbName);
        const usersCollection = db.collection(collectionName1);

        const existingUser = await usersCollection.findOne({ username });
        if (!existingUser) {
            return res.status(400).send('Invalid username or password');
        }

        if (existingUser.password !== password) {
            return res.status(400).send('Invalid username or password');
        }

        const token = jwt.sign({ userId: existingUser._id }, 'your_secret_key', { expiresIn: '1h' });

        client.close();

        return res.status(200).send({ message: 'Login successful', token, email: existingUser.email  });
    } catch (err) {
        console.error(err);
        return res.status(500).send('Internal server error');
    }
});

module.exports = router;
