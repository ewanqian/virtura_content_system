const winston = require('winston');
const fs = require('fs');
const path = require('path');
const config = require('./config');

const logDir = path.dirname(config.logging.file);

if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

const logger = winston.createLogger({
  level: config.logging.level,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    new winston.transports.File({
      filename: config.logging.file,
      maxsize: config.logging.max_size,
      maxFiles: config.logging.max_files
    })
  ]
});

const auditLogger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({
      filename: config.audit.log_file,
      maxsize: config.logging.max_size,
      maxFiles: config.logging.max_files
    })
  ]
});

function auditLog(request, response = null) {
  if (!config.audit.enabled) return;

  const logData = {
    timestamp: new Date().toISOString(),
    method: request.method,
    path: request.originalUrl,
    ip: request.ip,
    userAgent: request.headers['user-agent'],
    requestId: request.headers['x-request-id'] || Math.random().toString(36).substr(2, 9)
  };

  if (config.audit.log_requests && Object.keys(request.body).length > 0) {
    logData.requestBody = request.body;
  }

  if (config.audit.log_responses && response) {
    logData.responseStatus = response.statusCode;
    if (response.body) {
      logData.responseBody = response.body;
    }
  }

  auditLogger.info(logData);
}

module.exports = {
  logger,
  auditLogger,
  auditLog
};
