from mcp.server.fastmcp import FastMCP

# FastMCP 서버 초기화
# json_response=False, stateless_http=False 등은 필요에 따라 조정
mcp = FastMCP(
    name="weather", 
    json_response=False, 
    stateless_http=False
)