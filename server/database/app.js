const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(express.json()); // Change to use express.json()

// Load data from JSON files
let reviews_data, dealerships_data, car_records_data;

try {
  reviews_data = JSON.parse(fs.readFileSync('./data/reviews.json'));
  dealerships_data = JSON.parse(fs.readFileSync('./data/dealerships.json', 'utf8'));
  car_records_data = JSON.parse(fs.readFileSync('./data/car_records.json', 'utf8')); // Load car records
} catch (error) {
  console.error('Error reading JSON files:', error);
}

// Connect to MongoDB
mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' })
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Error connecting to MongoDB:', err));

// Models
const Reviews = require('./review');
const Dealerships = require('./dealership');

// Initialize data in the database
const initializeData = async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviews_data['reviews']);
    console.log("Reviews data initialized");

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealerships_data['dealerships']);
    console.log("Dealerships data initialized");
  } catch (error) {
    console.error('Error initializing data:', error);
  }
};

// Call the initialize function
initializeData();

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealers = await Dealerships.find();
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealers' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealersByState = await Dealerships.find({ state: req.params.state });
    res.json(dealersByState);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealers by state' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealer = await Dealerships.findById(req.params.id);
    if (!dealer) return res.status(404).json({ error: 'Dealer not found' });
    res.json(dealer);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer' });
  }
});

// Express route to fetch car makes and models
app.get('/api/car-makes', (req, res) => {
  try {
    const carMakes = car_records_data.cars.reduce((acc, car) => {
      const existingMake = acc.find(item => item.make === car.make);
      if (existingMake) {
        if (!existingMake.models.includes(car.model)) {
          existingMake.models.push(car.model);
        }
      } else {
        acc.push({ make: car.make, models: [car.model] });
      }
      return acc;
    }, []);
    
    res.json(carMakes);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching car makes' });
  }
});

// Express route to insert review
app.post('/insert_review', async (req, res) => {
  const data = req.body;
  const documents = await Reviews.find().sort({ id: -1 });
  let new_id = documents[0] ? documents[0]['id'] + 1 : 1; // Handle case if no reviews exist

  const review = new Reviews({
    "id": new_id,
    "name": data['name'],
    "dealership": data['dealership'],
    "review": data['review'],
    "purchase": data['purchase'],
    "purchase_date": data['purchase_date'],
    "car_make": data['car_make'],
    "car_model": data['car_model'],
    "car_year": data['car_year'],
  });

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
