const contentStore = require('../contentStore');
const { logger } = require('../logger');

module.exports = {
  name: 'content_system_get',
  description: 'Get a specific content object by its Typed ID',
  async execute({ id, include_relations = true }) {
    logger.info('Getting content object', { id, include_relations });

    try {
      await contentStore.load();

      let obj;

      if (include_relations) {
        obj = contentStore.getObjectWithRelations(id);
      } else {
        obj = contentStore.getObject(id);
      }

      if (!obj) {
        throw new Error(`Content object not found: ${id}`);
      }

      return obj;
    } catch (error) {
      logger.error('Get object failed', { id, error: error.message });
      throw new Error(`Failed to get object: ${error.message}`);
    }
  }
};
