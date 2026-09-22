"""Minimaler MCP-Client zum Testen ohne Node/Inspector.

Start: python mcp_server/smoke_test.py   (App auf :8000 und MCP-Server auf :8001 müssen laufen)
"""
import asyncio
import json
import os
import sys

from mcp import Client

URL = os.environ.get("TOOLSHED_MCP_URL", "http://127.0.0.1:8001/mcp")


async def main() -> int:
    async with Client(URL) as client:
        tools = await client.list_tools()
        names = [t.name for t in tools.tools]
        print("Tools:", ", ".join(names))
        assert "list_overdue_loans" in names, "Tool list_overdue_loans fehlt"

        result = await client.call_tool("list_overdue_loans", {})
        payload = result.structured_content if result.structured_content is not None else [c.text for c in result.content]
        print("list_overdue_loans →", json.dumps(payload, ensure_ascii=False)[:400])

        resources = await client.list_resources()
        print("Resources:", ", ".join(str(r.uri) for r in resources.resources))
        prompts = await client.list_prompts()
        print("Prompts:", ", ".join(p.name for p in prompts.prompts))
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
