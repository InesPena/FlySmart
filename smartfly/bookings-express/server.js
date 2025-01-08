const express = require('express');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const app = express();

app.use(express.json());
app.use(cors()); 

const authRoutes = require('./routes/auth-service');
const bookRoutes = require('./routes/booking-service');

app.use('/auth', authRoutes);  
app.use('/book', bookRoutes); 

// Iniciar el servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
