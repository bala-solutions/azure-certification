from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Calculator",
    stateless_http=True,
    json_response=True
)

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

# ASGI app (EXACTLY this)
app = mcp.streamable_http_app