const contentStore = require('../contentStore');
const { logger } = require('../logger');

module.exports = {
  name: 'content_system_create',
  description: 'Create a new content object in the Virtura Content System',
  async execute({ type, fields }) {
    logger.info('Creating content object', { type, fields });

    try {
      await contentStore.load();

      const id = contentStore.createObject(type, fields);
      const createdObject = contentStore.getObject(id);

      logger.info('Content object created', { id });

      return {
        id,
        object: createdObject
      };
    } catch (error) {
      logger.error('Create failed', { error: error.message });
      throw new Error(`Failed to create object: ${error.message}`);
    }
  }
};
