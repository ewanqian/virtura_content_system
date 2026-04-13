const fs = require('fs');
const path = require('path');
const config = require('./config');
const { logger } = require('./logger');

const CONTENT_TYPES = ['person', 'collective', 'work', 'node', 'asset', 'writing', 'venue', 'spec', 'relation'];

class ContentStore {
  constructor() {
    this.contentCache = new Map();
    this.schemas = new Map();
    this.relations = new Map();
    this.loaded = false;
  }

  async load() {
    if (this.loaded) return;

    try {
      await this.loadSchemas();
      await this.loadContent();
      await this.loadRelations();
      this.loaded = true;
      logger.info('Content store loaded successfully');
    } catch (error) {
      logger.error('Failed to load content store:', error);
      throw error;
    }
  }

  async loadSchemas() {
    const schemasDir = path.join(config.content.base_dir, config.content.schemas_dir);

    for (const contentType of CONTENT_TYPES) {
      const schemaFile = path.join(schemasDir, `${contentType}.schema.json`);

      if (fs.existsSync(schemaFile)) {
        try {
          const schemaContent = fs.readFileSync(schemaFile, 'utf8');
          const schema = JSON.parse(schemaContent);
          this.schemas.set(contentType, schema);
        } catch (error) {
          logger.error(`Failed to load schema for ${contentType}:`, error);
        }
      }
    }
  }

  async loadContent() {
    const contentDir = path.join(config.content.base_dir, config.content.content_dir);

    for (const contentType of CONTENT_TYPES) {
      const typeDir = path.join(contentDir, contentType + 's');

      if (fs.existsSync(typeDir)) {
        const files = fs.readdirSync(typeDir).filter(file =>
          file.endsWith('.json') || file.endsWith('.yaml') || file.endsWith('.yml')
        );

        for (const file of files) {
          try {
            const content = this.loadContentFile(path.join(typeDir, file));
            const id = content.id || this.generateId(contentType, content.title || content.name);
            const typedId = `${contentType}:${id}`;

            this.contentCache.set(typedId, {
              ...content,
              id: typedId,
              type: contentType,
              _raw_file: file
            });
          } catch (error) {
            logger.error(`Failed to load content from ${file}:`, error);
          }
        }
      }
    }
  }

  async loadRelations() {
    const relationDir = path.join(config.content.base_dir, config.content.content_dir, 'relations');

    if (fs.existsSync(relationDir)) {
      const files = fs.readdirSync(relationDir).filter(file =>
        file.endsWith('.json') || file.endsWith('.yaml') || file.endsWith('.yml')
      );

      for (const file of files) {
        try {
          const content = this.loadContentFile(path.join(relationDir, file));

          if (content.source && content.target) {
            const relationId = this.generateId('relation', `${content.source}-${content.target}`);
            const typedId = `relation:${relationId}`;

            this.contentCache.set(typedId, {
              ...content,
              id: typedId,
              type: 'relation'
            });
          }
        } catch (error) {
          logger.error(`Failed to load relation from ${file}:`, error);
        }
      }
    }
  }

  loadContentFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');

    if (filePath.endsWith('.json')) {
      return JSON.parse(content);
    } else {
      const yaml = require('yaml');
      return yaml.parse(content);
    }
  }

  generateId(type, name) {
    const slug = name
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-')
      .trim()
      .slice(0, 30);
    return `${type}-${slug}-${Date.now().toString(36)}`;
  }

  getObject(typedId) {
    return this.contentCache.get(typedId);
  }

  searchObjects(query = '', filters = {}) {
    const results = [];

    for (const [id, obj] of this.contentCache.entries()) {
      if (this.matchQuery(obj, query) && this.matchFilters(obj, filters)) {
        results.push(this.filterSensitiveFields(obj));
      }
    }

    return results;
  }

  matchQuery(obj, query) {
    if (!query) return true;

    const queryStr = query.toLowerCase();
    const searchFields = ['title', 'name', 'description', 'summary', 'tags'];

    return searchFields.some(field => {
      const value = obj[field];
      return value && String(value).toLowerCase().includes(queryStr);
    });
  }

  matchFilters(obj, filters) {
    for (const [key, value] of Object.entries(filters)) {
      if (key === 'type') {
        if (obj.type !== value) return false;
      } else if (key === 'tags') {
        if (!obj.tags || !value.some(tag => obj.tags.includes(tag))) {
          return false;
        }
      } else if (key === 'year') {
        const objYear = this.getYear(obj);
        if (objYear !== value) return false;
      } else if (obj[key] !== value) {
        return false;
      }
    }

    return true;
  }

  getYear(obj) {
    if (obj.date) {
      const dateStr = String(obj.date);
      if (dateStr.length === 4 && !isNaN(dateStr)) {
        return parseInt(dateStr);
      }
      if (dateStr.includes('-')) {
        return parseInt(dateStr.split('-')[0]);
      }
    }
    return null;
  }

  filterSensitiveFields(obj) {
    const filtered = { ...obj };

    for (const field of config.security.sensitive_fields) {
      if (filtered[field]) {
        delete filtered[field];
      }
    }

    return filtered;
  }

  createObject(contentType, fields) {
    const id = fields.id || this.generateId(contentType, fields.title || fields.name || 'new-object');
    const typedId = `${contentType}:${id}`;

    const newObject = {
      ...fields,
      id: typedId,
      type: contentType,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.contentCache.set(typedId, this.filterSensitiveFields(newObject));
    return typedId;
  }

  linkObjects(sourceId, targetId, relationType) {
    const relationId = this.generateId('relation', `${sourceId}-${targetId}`);
    const typedId = `relation:${relationId}`;

    const relation = {
      id: typedId,
      type: 'relation',
      source: sourceId,
      target: targetId,
      relationType: relationType || 'related',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.contentCache.set(typedId, relation);
    return typedId;
  }

  getObjectRelations(typedId) {
    const relations = [];

    for (const [id, obj] of this.contentCache.entries()) {
      if (obj.type === 'relation') {
        if (obj.source === typedId || obj.target === typedId) {
          relations.push(obj);
        }
      }
    }

    return relations;
  }

  getObjectWithRelations(typedId) {
    const obj = this.getObject(typedId);

    if (!obj) {
      return null;
    }

    return {
      ...obj,
      relations: this.getObjectRelations(typedId)
    };
  }

  getAllObjectTypes() {
    return [...new Set([...this.contentCache.values()].map(obj => obj.type))];
  }
}

module.exports = new ContentStore();
