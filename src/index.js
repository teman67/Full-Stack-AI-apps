const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');
require('dotenv').config();

const { AWSService } = require('./services/aws');
const { GCPService } = require('./services/gcp');
const { AzureService } = require('./services/azure');
const { MCPService } = require('./mcp/client');

// Initialize logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  defaultMeta: { service: 'full-stack-ai' },
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Initialize services
const awsService = new AWSService();
const gcpService = new GCPService();
const azureService = new AzureService();
const mcpService = new MCPService();

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development'
  });
});

// AI/ML endpoints
app.use('/api/aws', require('./routes/aws'));
app.use('/api/gcp', require('./routes/gcp'));
app.use('/api/azure', require('./routes/azure'));
app.use('/api/rag', require('./routes/rag'));
app.use('/api/agents', require('./routes/agents'));
app.use('/api/mcp', require('./routes/mcp'));

// Error handling middleware
app.use((error, req, res, next) => {
  logger.error('Application error:', error);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? error.message : 'Something went wrong'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.originalUrl
  });
});

// Start server
app.listen(PORT, () => {
  logger.info(`Full-Stack AI Apps server running on port ${PORT}`);
  console.log(`🚀 Server is running on http://localhost:${PORT}`);
  console.log(`📖 Health check: http://localhost:${PORT}/health`);
});

module.exports = app;