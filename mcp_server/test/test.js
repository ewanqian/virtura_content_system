#!/usr/bin/env node

const contentStore = require('../src/contentStore');
const { logger } = require('../src/logger');

async function runTests() {
  logger.info('Running Virtura Content System MCP Server tests...');

  try {
    await contentStore.load();
    console.log('✅ Content store loaded successfully');

    const types = contentStore.getAllObjectTypes();
    console.log(`✅ Available content types: ${types.join(', ')}`);

    console.log('\n--- Search Test ---');
    const searchResults = contentStore.searchObjects('', { limit: 5 });
    console.log(`✅ Search returned ${searchResults.length} results`);

    if (searchResults.length > 0) {
      searchResults.slice(0, 3).forEach(obj => {
        console.log(`  - ${obj.id}: ${obj.title || obj.name || 'Untitled'}`);
      });
    }

    if (searchResults.length > 0) {
      console.log('\n--- Get Object Test ---');
      const firstId = searchResults[0].id;
      const obj = contentStore.getObject(firstId);
      console.log(`✅ Retrieved object: ${obj.id}`);

      const objWithRelations = contentStore.getObjectWithRelations(firstId);
      console.log(`✅ Object has ${objWithRelations.relations ? objWithRelations.relations.length : 0} relations`);
    }

    console.log('\n--- Create Object Test ---');
    const newId = contentStore.createObject('node', {
      title: 'Test Node (MCP)',
      description: 'This is a test node created by the MCP server test suite',
      tags: ['test', 'mcp'],
      date: '2026'
    });
    console.log(`✅ Created new object: ${newId}`);

    const createdObj = contentStore.getObject(newId);
    console.log(`✅ Verified created object: ${createdObj.title}`);

    if (searchResults.length > 0) {
      console.log('\n--- Link Objects Test ---');
      const secondId = searchResults[0].id;
      const relationId = contentStore.linkObjects(
        newId,
        secondId,
        'related_to'
      );
      console.log(`✅ Created relation: ${relationId}`);

      const testObjRelations = contentStore.getObjectRelations(newId);
      console.log(`✅ Test object now has ${testObjRelations.length} relations`);
    }

    console.log('\n✅ All tests passed!');

  } catch (error) {
    logger.error('Test failed:', error);
    console.error('❌ Test failed:', error.message);
    process.exit(1);
  }
}

runTests();
