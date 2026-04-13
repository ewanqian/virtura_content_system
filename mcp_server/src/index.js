#!/usr/bin/env node

const express = require('express');
const cors = require('cors');
const config = require('./config');
const contentStore = require('./contentStore');
const { logger, auditLog } = require('./logger');
const tools = require('./tools');

const app = express();

app.use(cors(config.cors));
app.use(express.json({ limit: '10mb' }));

app.use((req, res, next) => {
  const startTime = Date.now();

  res.on('finish', () => {
    const responseTime = Date.now() - startTime;
    logger.info(`${req.method} ${req.path} ${res.statusCode} ${responseTime}ms`);
  });

  next();
});

async function startServer() {
  logger.info('Starting Virtura Content System MCP Server...');

  try {
    await contentStore.load();
    logger.info('Content store loaded successfully');
  } catch (error) {
    logger.error('Failed to load content store on startup:', error);
  }

  app.get('/health', (req, res) => {
    res.json({
      status: 'ok',
      name: 'virtura-content-system',
      version: '1.0.0'
    });
  });

  app.post('/tools/search', async (req, res) => {
    try {
      const result = await tools.searchTool.execute(req.body);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  app.post('/tools/get', async (req, res) => {
    try {
      const result = await tools.getTool.execute(req.body);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  app.post('/tools/create', async (req, res) => {
    try {
      const result = await tools.createTool.execute(req.body);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  app.post('/tools/link', async (req, res) => {
    try {
      const result = await tools.linkTool.execute(req.body);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  app.post('/tools/export', async (req, res) => {
    try {
      const result = await tools.exportTool.execute(req.body);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  app.get('/tools/list-types', async (req, res) => {
    try {
      res.json({
        types: ['person', 'collective', 'work', 'node', 'asset', 'writing', 'venue', 'spec', 'relation']
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  app.get('/tools', (req, res) => {
    res.json({
      tools: [
        {
          name: 'content_system_search',
          description: tools.searchTool.description,
          endpoint: '/tools/search'
        },
        {
          name: 'content_system_get',
          description: tools.getTool.description,
          endpoint: '/tools/get'
        },
        {
          name: 'content_system_create',
          description: tools.createTool.description,
          endpoint: '/tools/create'
        },
        {
          name: 'content_system_link',
          description: tools.linkTool.description,
          endpoint: '/tools/link'
        },
        {
          name: 'content_system_export',
          description: tools.exportTool.description,
          endpoint: '/tools/export'
        },
        {
          name: 'content_system_list_types',
          description: 'List all available content types',
          endpoint: '/tools/list-types'
        }
      ]
    });
  });

  const port = config.server.port;
  const host = config.server.host;

  app.listen(port, host, () => {
    logger.info(`Virtura Content System MCP Server listening on http://${host}:${port}`);
    logger.info('Available endpoints:');
    logger.info('  GET  /health');
    logger.info('  GET  /tools');
    logger.info('  POST /tools/search');
    logger.info('  POST /tools/get');
    logger.info('  POST /tools/create');
    logger.info('  POST /tools/link');
    logger.info('  POST /tools/export');
    logger.info('  GET  /tools/list-types');
  });

  process.on('SIGINT', () => {
    logger.info('Received SIGINT, shutting down...');
    process.exit(0);
  });

  process.on('SIGTERM', () => {
    logger.info('Received SIGTERM, shutting down...');
    process.exit(0);
  });
}

startServer().catch((error) => {
  logger.error('Failed to start server:', error);
  process.exit(1);
});
