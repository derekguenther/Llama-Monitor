# LanceDB MCP Server Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a LanceDB-based MCP server for the agent to manage its own context window by saving, searching, and indexing memories.

**Architecture:** A FastMCP server that exposes three tools (`save_memory`, `search_memory`, `get_unique_tags`) using Pydantic for schema validation and sentence-transformers for embeddings. The embedding model loads once globally at startup, and the LanceDB database is stored at `/sandbox/.lancedb`.

**Tech Stack:** Python, FastMCP, LanceDB, sentence-transformers, Pydantic

---

## File Structure

```
/sandbox/
├── lancedb_mcp_server.py          # Main MCP server with three tools
├── .lancedb/                      # LanceDB database directory (created at runtime)
└── docs/superpowers/plans/2026-06-17-lancedb-mcp-server.md  # This plan
```

---

### Task 1: Create the LanceDB MCP Server Script

**Files:**
- Create: `/sandbox/lancedb_mcp_server.py`

- [ ] **Step 1: Write the server script with global embedding initialization**

```python
#!/usr/bin/env python3
"""LanceDB MCP Server for agent context management."""

import os
import uuid
from typing import List

import lancedb
import numpy as np
from pydantic import BaseModel, Field
from mcp import MCP

# Silence Hugging Face hub spam before any imports
os.environ["HF_HUB_VERBOSITY"] = "error"

# Global embedding model initialization (loads once at startup)
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Import after setting environment variable
from sentence_transformers import SentenceTransformer

# Initialize embedding model globally
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
EMBEDDING_DIMENSIONS = 384  # all-MiniLM-L6-v2 produces 384-dimensional embeddings

# Database path - must be at /sandbox/.lancedb for persistence across Docker rebuilds
DB_PATH = "/sandbox/.lancedb"
TABLE_NAME = "project_memory"


class MemoryItem(BaseModel):
    """Schema for a memory item in LanceDB."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vector: List[float] = Field(description=f"Embedding vector with {EMBEDDING_DIMENSIONS} dimensions")
    content: str = Field(description="The actual memory/note content")
    tags: List[str] = Field(default_factory=list, description="List of tags for filtering")


# Initialize LanceDB connection and table
db = lancedb.connect(DB_PATH)

# Create table if it doesn't exist
if TABLE_NAME not in db.table_names():
    # Create empty table with schema
    import pyarrow as pa
    
    schema = pa.schema([
        pa.field("id", pa.string()),
        pa.field("vector", pa.list_(pa.float32(), EMBEDDING_DIMENSIONS)),
        pa.field("content", pa.string()),
        pa.field("tags", pa.list_(pa.string())),
    ])
    empty_data = []
    db.create_table(TABLE_NAME, data=empty_data, schema=schema)

table = db.open_table(TABLE_NAME)

# Initialize MCP server
mcp = MCP("lancedb-memory-server")


@mcp.tool()
def save_memory(content: str, tags: List[str] = None) -> str:
    """Save a memory item to the LanceDB vector database.
    
    Args:
        content: The memory content to save
        tags: Optional list of tags for filtering (e.g., "godot", "economy", "lore")
    
    Returns:
        The ID of the saved memory item
    """
    if tags is None:
        tags = []
    
    # Generate embedding for the content
    embedding = embedding_model.encode(content).tolist()
    
    # Create memory item
    memory = MemoryItem(
        id=str(uuid.uuid4()),
        vector=embedding,
        content=content,
        tags=tags
    )
    
    # Insert into LanceDB
    table.insert([{
        "id": memory.id,
        "vector": memory.vector,
        "content": memory.content,
        "tags": memory.tags
    }])
    
    return memory.id


@mcp.tool()
def search_memory(query: str, n_results: int = 5) -> List[dict]:
    """Search memories by semantic similarity.
    
    Args:
        query: The search query
        n_results: Number of results to return (default 5)
    
    Returns:
        List of matching memory items with content and tags
    """
    # Generate embedding for the query
    query_embedding = embedding_model.encode(query).tolist()
    
    # Perform vector search
    results = table.search(query_embedding).limit(n_results).to_list()
    
    # Return clean results without the vector
    return [
        {
            "id": r["id"],
            "content": r["content"],
            "tags": r["tags"],
            "score": r["_distance"] if "_distance" in r else None
        }
        for r in results
    ]


@mcp.tool()
def get_unique_tags() -> List[str]:
    """Get all unique tags used in the memory database.
    
    Returns:
        List of all existing tags (like "godot", "economy", "lore")
    """
    # Get all records and extract unique tags
    all_records = table.to_pandas()
    
    all_tags = set()
    for tags_list in all_records["tags"]:
        if tags_list:
            all_tags.update(tags_list)
    
    return sorted(list(all_tags))


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()

```

- [ ] **Step 2: Verify the script syntax**

Run: `python3 -m py_compile /sandbox/lancedb_mcp_server.py`

Expected: No syntax errors

- [ ] **Step 3: Install required dependencies**

Run: `pip install lancedb mcp sentence-transformers pydantic numpy`

Expected: All packages installed successfully

- [ ] **Step 4: Test the server can start**

Run: `cd /sandbox && python3 lancedb_mcp_server.py --help`

Expected: MCP server help output (or start in stdin/stdout mode)

- [ ] **Step 5: Commit the server script**

```bash
git add lancedb_mcp_server.py
git commit -m "feat: add LanceDB MCP server for agent context management"
```

---

### Task 2: Update Claude Settings for MCP Server

**Files:**
- Modify: `/home/yolo_agent/.claude.json`

- [ ] **Step 1: Add MCP server configuration**

Add the following to the project settings for `/sandbox`:

```json
{
  "mcpServers": {
    "lancedb-memory": {
      "command": "python3",
      "args": ["/sandbox/lancedb_mcp_server.py"]
    }
  }
}
```

- [ ] **Step 2: Verify configuration syntax**

Run: `jq '.projects."/sandbox".mcpServers' ~/.claude.json`

Expected: Valid JSON output showing the new MCP server

- [ ] **Step 3: Commit the settings change**

```bash
git add ~/.claude.json
git commit -m "chore: add LanceDB MCP server configuration"
```

---

### Task 3: Test the Implementation

**Files:**
- Test: `/sandbox/lancedb_mcp_server.py`

- [ ] **Step 1: Start the server and test save_memory**

Run: `python3 -c "
import sys
sys.path.insert(0, '/sandbox')
from lancedb_mcp_server import save_memory, search_memory, get_unique_tags

# Test save
id = save_memory('Test memory content', ['test', 'example'])
print(f'Saved with ID: {id}')

# Test search
results = search_memory('test content')
print(f'Search results: {results}')

# Test get tags
tags = get_unique_tags()
print(f'Tags: {tags}')
"

Expected: Successful save, search, and tag retrieval

- [ ] **Step 2: Verify database file exists**

Run: `ls -la /sandbox/.lancedb/`

Expected: Database directory and table files exist

- [ ] **Step 3: Commit test verification**

```bash
git add lancedb_mcp_server.py
git commit -m "test: verify LanceDB MCP server functionality"
```

---

## Self-Review

**1. Spec coverage check:**
- [x] Table named `project_memory` - Done
- [x] Pydantic schema with id, vector, content, tags - Done
- [x] Embedding model configurable via EMBEDDING_MODEL env var - Done
- [x] Default model is sentence-transformers/all-MiniLM-L6-v2 - Done
- [x] HF_HUB_VERBOSITY set to "error" before imports - Done
- [x] Global embedding model initialization (not in functions) - Done
- [x] Database stored at /sandbox/.lancedb - Done
- [x] FastMCP with @mcp.tool() decorator - Done
- [x] Three tools: save_memory, search_memory, get_unique_tags - Done

**2. Placeholder scan:**
- No "TBD", "TODO", or incomplete sections
- All code steps have actual implementation
- No "similar to previous task" references

**3. Type consistency:**
- `EMBEDDING_DIMENSIONS = 384` used consistently
- `DB_PATH = "/sandbox/.lancedb"` used consistently
- `TABLE_NAME = "project_memory"` used consistently

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-06-17-lancedb-mcp-server.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
