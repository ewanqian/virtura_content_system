const contentStore = require('../contentStore');
const { logger } = require('../logger');

module.exports = {
  name: 'content_system_search',
  description: 'Search for content objects in the Virtura Content System',
  async execute({ query, type, tags, year, limit = 50, offset = 0 }) {
    logger.info('Searching for content', { query, type, tags, year, limit, offset });

    try {
      await contentStore.load();

      const filters = {};
      if (type) {
        filters.type = type;
      }
      if (tags && tags.length > 0) {
        filters.tags = tags;
      }
      if (year) {
        filters.year = year;
      }

      const results = contentStore.searchObjects(query || '', filters);
      const total = results.length;

      const paginatedResults = results.slice(offset, offset + limit);

      return {
        results: paginatedResults,
        total,
        offset,
        limit: paginatedResults.length
      };
    } catch (error) {
      logger.error('Search failed', { error: error.message });
      throw new Error(`Search failed: ${error.message}`);
    }
  }
};
