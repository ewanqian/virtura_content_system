const contentStore = require('../contentStore');
const config = require('../config');
const { logger } = require('../logger');

function exportAsJSON(results) {
  return JSON.stringify(results, null, 2);
}

function exportAsCSV(results) {
  if (!results.length) {
    return '';
  }

  const headers = ['id', 'type', 'title', 'name', 'description', 'date'];
  const rows = results.map(obj => {
    return headers.map(header => {
      const value = obj[header] || '';
      return `"${String(value).replace(/"/g, '""')}"`;
    }).join(',');
  });

  return [headers.join(','), ...rows].join('\n');
}

function exportAsMarkdown(results) {
  if (!results.length) {
    return '# No Results\n';
  }

  const byType = {};
  results.forEach(obj => {
    if (!byType[obj.type]) {
      byType[obj.type] = [];
    }
    byType[obj.type].push(obj);
  });

  let markdown = '# Content Export\n\n';

  for (const [type, objects] of Object.entries(byType)) {
    markdown += `## ${type.charAt(0).toUpperCase() + type.slice(1)}s\n\n`;
    markdown += `Total: ${objects.length}\n\n`;

    objects.forEach(obj => {
      const title = obj.title || obj.name || 'Untitled';
      markdown += `### ${title}\n\n`;
      markdown += `- **ID:** ${obj.id}\n`;
      if (obj.description) {
        markdown += `\n${obj.description}\n`;
      }
      if (obj.tags && obj.tags.length) {
        markdown += `- **Tags:** ${obj.tags.join(', ')}\n`;
      }
      markdown += '\n---\n\n';
    });
  }

  return markdown;
}

module.exports = {
  name: 'content_system_export',
  description: 'Export content objects in various formats',
  async execute({ query, type, tags, ids, format = 'json', limit = 100 }) {
    logger.info('Exporting content', { query, type, tags, ids, format, limit });

    try {
      await contentStore.load();

      let results;

      if (ids && ids.length > 0) {
        results = ids
          .map(id => contentStore.getObjectWithRelations(id))
          .filter(obj => obj !== null);
      } else {
        const filters = {};
        if (type) filters.type = type;
        if (tags && tags.length > 0) filters.tags = tags;

        results = contentStore.searchObjects(query || '', filters);
      }

      results = results.slice(0, Math.min(limit, config.export.max_export_size));

      let content;
      const exportFormat = format.toLowerCase();

      switch (exportFormat) {
        case 'json':
          content = exportAsJSON(results);
          break;
        case 'csv':
          content = exportAsCSV(results);
          break;
        case 'markdown':
          content = exportAsMarkdown(results);
          break;
        default:
          throw new Error(`Unsupported export format: ${format}`);
      }

      logger.info('Export completed', { count: results.length, format: exportFormat });

      return {
        content,
        format: exportFormat,
        count: results.length
      };
    } catch (error) {
      logger.error('Export failed', { error: error.message });
      throw new Error(`Failed to export content: ${error.message}`);
    }
  }
};
