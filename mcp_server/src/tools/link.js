const contentStore = require('../contentStore');
const { logger } = require('../logger');

module.exports = {
  name: 'content_system_link',
  description: 'Create a bidirectional relation between two content objects',
  async execute({ source_id, target_id, relation_type, fields = {} }) {
    logger.info('Linking objects', { source_id, target_id, relation_type });

    try {
      await contentStore.load();

      const source = contentStore.getObject(source_id);
      const target = contentStore.getObject(target_id);

      if (!source) {
        throw new Error(`Source object not found: ${source_id}`);
      }
      if (!target) {
        throw new Error(`Target object not found: ${target_id}`);
      }

      const relationId = contentStore.linkObjects(
        source_id,
        target_id,
        relation_type || 'related'
      );

      const relation = contentStore.getObject(relationId);

      logger.info('Relation created', { relationId, source_id, target_id });

      return {
        relation_id: relationId,
        relation
      };
    } catch (error) {
      logger.error('Link failed', { error: error.message });
      throw new Error(`Failed to link objects: ${error.message}`);
    }
  }
};
