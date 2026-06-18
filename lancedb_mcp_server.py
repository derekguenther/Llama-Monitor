#!/usr/bin/env python3
"""LanceDB MCP Server for agent context management."""

import os
import uuid
from typing import List

import lancedb
import numpy as np
from pydantic import BaseModel, Field
from fastmcp import FastMCP

# Silence Hugging Face hub spam before any imports
os.environ["HF_HUB_VERBOSITY"] = "error"

# Global embedding model initialization (loads once at startup)
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

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

# Initialize FastMCP server
mcp = FastMCP("lancedb-memory-server")


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

    # Add to LanceDB
    table.add([{
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
        # Handle both list and array types
        if tags_list is not None and len(tags_list) > 0:
            all_tags.update(tags_list)

    return sorted(list(all_tags))


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
