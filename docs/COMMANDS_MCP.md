# Virtura Content System MCP 命令文档

## 目录

- [content_system_search](#content_system_search)
- [content_system_get](#content_system_get)
- [content_system_create](#content_system_create)
- [content_system_link](#content_system_link)
- [content_system_export](#content_system_export)
- [content_system_list_types](#content_system_list_types)

---

## content_system_search

搜索内容系统中的对象。

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `query` | string | 否 | 搜索关键词，匹配标题、描述、标签等 |
| `type` | string | 否 | 按内容类型过滤 |
| `tags` | string[] | 否 | 按标签过滤 |
| `year` | integer | 否 | 按年份过滤 |
| `limit` | integer | 否 | 返回结果数量限制，默认 50 |
| `offset` | integer | 否 | 分页偏移量，默认 0 |

### 返回值

```json
{
  "results": [ /* 匹配的对象列表 */ ],
  "total": 42,
  "offset": 0,
  "limit": 50
}
```

### 使用示例

#### 搜索所有对象
```javascript
content_system_search({})
```

#### 搜索包含 "art" 的作品
```javascript
content_system_search({
  "query": "art",
  "type": "work",
  "limit": 10
})
```

#### 搜索 2025 年的展览节点
```javascript
content_system_search({
  "type": "node",
  "year": 2025,
  "tags": ["exhibition"]
})
```

---

## content_system_get

通过 Typed ID 获取单个对象的详细信息。

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `id` | string | 是 | Typed ID（格式：type:id） |
| `include_relations` | boolean | 否 | 是否包含关联关系，默认 true |

### 返回值

完整的对象，包含所有字段和关联关系。

### 使用示例

#### 获取对象及其关联
```javascript
content_system_get({
  "id": "work:drop-flow"
})
```

#### 仅获取对象不包含关联
```javascript
content_system_get({
  "id": "person:ewan-qian",
  "include_relations": false
})
```

---

## content_system_create

创建新的内容对象。

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `type` | string | 是 | 内容类型 |
| `fields` | object | 是 | 对象字段 |

### fields 对象

| 字段 | 类型 | 描述 |
|------|------|------|
| `id` | string | 可选自定义 ID |
| `title` | string | 对象标题 |
| `name` | string | 对象名称（人物/集体） |
| `description` | string | 描述 |
| `summary` | string | 简短摘要 |
| `tags` | string[] | 标签 |
| `date` | string | 日期（ISO 或 YYYY） |
| `status` | string | 状态 |

### 返回值

```json
{
  "id": "node:test-node-abc123",
  "object": { /* 创建的对象 */ }
}
```

### 使用示例

#### 创建一个新作品
```javascript
content_system_create({
  "type": "work",
  "fields": {
    "title": "New Art Piece",
    "description": "A description of the work",
    "tags": ["art", "new"],
    "date": "2026",
    "status": "published"
  }
})
```

#### 创建一个新人物
```javascript
content_system_create({
  "type": "person",
  "fields": {
    "name": "Jane Artist",
    "summary": "Multimedia artist based in NYC",
    "tags": ["artist", "multimedia"]
  }
})
```

---

## content_system_link

在两个对象之间建立双向关联关系。

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `source_id` | string | 是 | 源对象 Typed ID |
| `target_id` | string | 是 | 目标对象 Typed ID |
| `relation_type` | string | 否 | 关系类型，默认 "related" |
| `fields` | object | 否 | 额外关系字段 |

### 关系类型

- `author_of` - 作者
- `contributor_to` - 贡献者
- `featured_in` - 特色展示
- `part_of` - 属于
- `references` - 引用
- `related` - 相关（默认）
- 或自定义类型

### 返回值

```json
{
  "relation_id": "relation:source-target-abc123",
  "relation": { /* 关系对象 */ }
}
```

### 使用示例

#### 建立作者关系
```javascript
content_system_link({
  "source_id": "person:ewan-qian",
  "target_id": "work:drop-flow",
  "relation_type": "author_of",
  "fields": {
    "description": "Primary creator",
    "start_date": "2023"
  }
})
```

#### 建立从属关系
```javascript
content_system_link({
  "source_id": "work:timer",
  "target_id": "node:hangzhou-opening",
  "relation_type": "featured_in"
})
```

---

## content_system_export

导出内容为指定格式。

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `query` | string | 否 | 搜索关键词 |
| `type` | string | 否 | 内容类型过滤 |
| `tags` | string[] | 否 | 标签过滤 |
| `ids` | string[] | 否 | 指定 ID 列表导出（忽略其他过滤器） |
| `format` | string | 否 | 格式：json, csv, markdown（默认 json） |
| `limit` | integer | 否 | 导出数量限制，默认 100 |

### 返回值

```json
{
  "content": "导出的内容字符串",
  "format": "json",
  "count": 42
}
```

### 使用示例

#### 导出所有作品为 JSON
```javascript
content_system_export({
  "type": "work",
  "format": "json"
})
```

#### 导出特定对象为 Markdown
```javascript
content_system_export({
  "ids": ["work:drop-flow", "work:timer", "node:hangzhou-opening"],
  "format": "markdown"
})
```

#### 导出 2025 年的展览为 CSV
```javascript
content_system_export({
  "type": "node",
  "tags": ["exhibition"],
  "year": 2025,
  "format": "csv"
})
```

---

## content_system_list_types

列出所有可用的内容类型。

### 参数

无

### 返回值

```json
{
  "types": [
    "person",
    "collective",
    "work",
    "node",
    "asset",
    "writing",
    "venue",
    "spec",
    "relation"
  ]
}
```

### 使用示例

```javascript
content_system_list_types()
```

---

## 完整工作流示例

### 场景：创建一个新作品并关联到人物和展览

```javascript
// 1. 创建一个新作品
const workResult = content_system_create({
  "type": "work",
  "fields": {
    "title": "Digital Dreams",
    "description": "An interactive digital installation",
    "tags": ["digital", "installation", "interactive"],
    "date": "2026"
  }
});

// 2. 关联作品到作者
content_system_link({
  "source_id": "person:ewan-qian",
  "target_id": workResult.id,
  "relation_type": "author_of"
});

// 3. 关联作品到展览节点
content_system_link({
  "source_id": workResult.id,
  "target_id": "node:hangzhou-opening",
  "relation_type": "featured_in",
  "fields": {
    "description": "Premiered at Hangzhou opening"
  }
});

// 4. 获取完整信息
content_system_get({
  "id": workResult.id
});
```
