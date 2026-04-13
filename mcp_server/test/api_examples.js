#!/usr/bin/env node

/**
 * API 调用示例
 * 演示如何通过 HTTP API 调用 Virtura Content System MCP 服务
 */

const http = require('http');

const BASE_URL = 'http://127.0.0.1:8000';

function makeRequest(method, path, data = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(BASE_URL + path);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let body = '';

      res.on('data', (chunk) => {
        body += chunk;
      });

      res.on('end', () => {
        try {
          const response = JSON.parse(body);
          resolve(response);
        } catch (e) {
          resolve(body);
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    if (data) {
      req.write(JSON.stringify(data));
    }

    req.end();
  });
}

async function runExamples() {
  console.log('Virtura Content System MCP API 示例\n');
  console.log('=' .repeat(50) + '\n');

  try {
    // 1. 健康检查
    console.log('1. 健康检查');
    console.log('-' .repeat(30));
    const health = await makeRequest('GET', '/health');
    console.log('✓ 健康状态:', health.status);
    console.log('  服务名称:', health.name);
    console.log('  版本:', health.version);
    console.log();

    // 2. 列出工具
    console.log('2. 列出可用工具');
    console.log('-' .repeat(30));
    const tools = await makeRequest('GET', '/tools');
    console.log('✓ 可用工具:');
    tools.tools.forEach(tool => {
      console.log(`  - ${tool.name}`);
      console.log(`    ${tool.description}`);
    });
    console.log();

    // 3. 列出内容类型
    console.log('3. 列出内容类型');
    console.log('-' .repeat(30));
    const types = await makeRequest('GET', '/tools/list-types');
    console.log('✓ 内容类型:', types.types.join(', '));
    console.log();

    // 4. 创建一个测试节点
    console.log('4. 创建测试节点');
    console.log('-' .repeat(30));
    const created = await makeRequest('POST', '/tools/create', {
      type: 'node',
      fields: {
        title: 'API 测试展览',
        description: '通过 API 创建的测试展览节点',
        summary: 'API 创建示例',
        tags: ['test', 'api', 'example'],
        date: '2026',
        status: 'published'
      }
    });
    console.log('✓ 创建成功!');
    console.log('  ID:', created.id);
    console.log('  标题:', created.object.title);
    console.log();

    // 5. 创建一个测试作品
    console.log('5. 创建测试作品');
    console.log('-' .repeat(30));
    const work = await makeRequest('POST', '/tools/create', {
      type: 'work',
      fields: {
        title: '数字艺术作品',
        description: '一个交互式数字艺术装置',
        tags: ['digital', 'art', 'interactive'],
        date: '2026'
      }
    });
    console.log('✓ 作品创建成功!');
    console.log('  ID:', work.id);
    console.log();

    // 6. 链接作品和节点
    console.log('6. 建立作品与节点的关联');
    console.log('-' .repeat(30));
    const linked = await makeRequest('POST', '/tools/link', {
      source_id: work.id,
      target_id: created.id,
      relation_type: 'featured_in',
      fields: {
        description: '在展览中展出'
      }
    });
    console.log('✓ 关联创建成功!');
    console.log('  关系 ID:', linked.relation_id);
    console.log();

    // 7. 搜索内容
    console.log('7. 搜索内容');
    console.log('-' .repeat(30));
    const searchResults = await makeRequest('POST', '/tools/search', {
      type: 'node',
      tags: ['test'],
      limit: 5
    });
    console.log(`✓ 找到 ${searchResults.total} 个结果:`);
    searchResults.results.forEach(result => {
      console.log(`  - ${result.id}: ${result.title}`);
    });
    console.log();

    // 8. 获取对象详情
    console.log('8. 获取对象详情（含关联）');
    console.log('-' .repeat(30));
    const detail = await makeRequest('POST', '/tools/get', {
      id: created.id,
      include_relations: true
    });
    console.log('✓ 对象详情:');
    console.log('  ID:', detail.id);
    console.log('  标题:', detail.title);
    console.log('  关联数量:', detail.relations ? detail.relations.length : 0);
    if (detail.relations) {
      detail.relations.forEach(rel => {
        console.log(`    - ${rel.source} -> ${rel.target} (${rel.relationType})`);
      });
    }
    console.log();

    // 9. 导出内容为 JSON
    console.log('9. 导出内容为 JSON');
    console.log('-' .repeat(30));
    const exported = await makeRequest('POST', '/tools/export', {
      type: 'node',
      tags: ['test'],
      format: 'json',
      limit: 10
    });
    console.log(`✓ 导出了 ${exported.count} 个对象 (${exported.format} 格式)`);
    console.log('  内容长度:', exported.content.length, '字符');
    console.log();

    // 10. 导出内容为 Markdown
    console.log('10. 导出内容为 Markdown');
    console.log('-' .repeat(30));
    const mdExport = await makeRequest('POST', '/tools/export', {
      ids: [work.id, created.id],
      format: 'markdown'
    });
    console.log(`✓ Markdown 导出成功 (${mdExport.count} 个对象)`);
    console.log();
    console.log('--- Markdown 预览 ---');
    console.log(mdExport.content.substring(0, 500) + '...');
    console.log();

    console.log('=' .repeat(50));
    console.log('✓ 所有示例运行成功!');
    console.log('\n提示: 要运行这些示例，请先启动服务器:');
    console.log('  cd mcp_server && npm start');

  } catch (error) {
    console.error('✗ 错误:', error.message);
    console.error('\n请确保服务器正在运行:');
    console.error('  cd mcp_server && npm start');
  }
}

// 如果直接运行此文件，则执行示例
if (require.main === module) {
  runExamples();
}

module.exports = {
  makeRequest,
  runExamples
};
