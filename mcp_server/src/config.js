const fs = require('fs');
const path = require('path');
const yaml = require('yaml');

const DEFAULT_CONFIG = {
  server: {
    port: 8000,
    host: "127.0.0.1",
    timeout: 30000
  },
  content: {
    base_dir: path.resolve(__dirname, '../../archive/VIRTURA-Content'),
    schemas_dir: "schemas",
    content_dir: "content",
    generated_dir: "generated",
    manifests_dir: "manifests"
  },
  security: {
    default_permission: "public",
    sensitive_fields: [
      "email",
      "phone",
      "address",
      "private_notes",
      "internal_comments"
    ],
    api_keys: []
  },
  logging: {
    level: "info",
    file: path.resolve(__dirname, '../logs/mcp_server.log'),
    max_size: 10485760,
    max_files: 5,
    format: "json"
  },
  export: {
    default_format: "json",
    supported_formats: ["json", "csv", "markdown"],
    max_export_size: 1000
  },
  audit: {
    enabled: true,
    log_file: path.resolve(__dirname, '../logs/audit.log'),
    log_requests: true,
    log_responses: false
  },
  cors: {
    enabled: true,
    origin: "*",
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowed_headers: ["Content-Type", "Authorization"]
  }
};

function loadConfig() {
  const configPaths = [
    path.resolve(__dirname, '../../config/mcp_config.yaml'),
    path.resolve(__dirname, '../../config/mcp_config.example.yaml')
  ];

  for (const configPath of configPaths) {
    if (fs.existsSync(configPath)) {
      try {
        const configContent = fs.readFileSync(configPath, 'utf8');
        const userConfig = yaml.parse(configContent);
        return mergeConfig(DEFAULT_CONFIG, userConfig);
      } catch (error) {
        console.error(`Error loading config from ${configPath}:`, error);
      }
    }
  }

  return DEFAULT_CONFIG;
}

function mergeConfig(defaultConfig, userConfig) {
  if (typeof userConfig !== 'object') return defaultConfig;

  const merged = { ...defaultConfig };

  for (const [key, value] of Object.entries(userConfig)) {
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      if (typeof merged[key] === 'object' && merged[key] !== null) {
        merged[key] = mergeConfig(merged[key], value);
      } else {
        merged[key] = value;
      }
    } else {
      merged[key] = value;
    }
  }

  return merged;
}

module.exports = loadConfig();
