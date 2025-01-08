const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const { MongoClient } = require('mongodb');
const router = express.Router();

const url = process.env.MONGO_URI || "mongodb://mongo:27017/booking-service";
//const url = "mongodb://127.0.0.1:27017/booking-service";
const dbName = "booking-service";
const collectionName1 = "bookings";

router.post('/bookflight', async (req, res) => {
    const { name, dni, email, ticketNumber, flightDetails } = req.body;

    if (!name || !dni || !email || !ticketNumber || !flightDetails) {
        return res.status(400).send('Name, DNI, email, ticket number, and flight details are required');
    }

    try {
        const client = await MongoClient.connect(url);
        const db = client.db(dbName);
        const passengersCollection = db.collection(collectionName1);

        const flightInfo = {
            origin: flightDetails.origin,
            destination: flightDetails.destination,
            number: flightDetails.number,
            carrier: flightDetails.carrier,
            departure: flightDetails.departure,
            arrival: flightDetails.arrival,
            class: flightDetails.class,
            baggageCount: flightDetails.baggageCount,
            type: flightDetails.isDirect, 
        };

        const result = await passengersCollection.insertOne({
            name,
            dni,
            email, 
            ticketNumber,
            flight: flightInfo,
        });

        client.close();

        return res.status(201).send('Passenger registered successfully');
    } catch (err) {
        console.error(err);
        return res.status(500).send('Internal server error');
    }
});

module.exports = router;

router.get('/retrievebookings', async (req, res) => {
    const { email } = req.query;

    try {
        const client = await MongoClient.connect(url);
        const db = client.db(dbName);
        const passengersCollection = db.collection(collectionName1);

        const reservations = await passengersCollection.find({ email }).toArray();

        client.close();

        if (reservations.length === 0) {
            return res.status(404).send('No reservations found for this email');
        }

        return res.status(200).json(reservations);
    } catch (err) {
        console.error(err);
        return res.status(500).send('Internal server error');
    }
});
