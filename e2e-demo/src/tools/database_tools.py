"""Database tools for telemetry storage and querying via MCP.

Provides tools for the Edge Operator Agent to store and query device telemetry
data using a local SQLite database accessed through the Model Context Protocol.
"""

from typing import Optional, List, Any
from datetime import datetime
from strands import tool
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters


class DatabaseTools:
    """MCP-based SQLite database tools for telemetry storage and querying.
    
    This class manages the connection to a local SQLite database via MCP,
    providing tools for logging device telemetry and querying historical data.
    
    Attributes:
        db_path: Path to the SQLite database file
        mcp_client: The MCP client for database operations
        _initialized: Whether the telemetry table has been created
    """
    
    TELEMETRY_TABLE_SCHEMA = """
        CREATE TABLE IF NOT EXISTS device_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            metric_type TEXT NOT NULL,
            value REAL NOT NULL,
            unit TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_device_id ON device_telemetry(device_id);
        CREATE INDEX IF NOT EXISTS idx_timestamp ON device_telemetry(timestamp);
    """
    
    def __init__(self, db_path: str = "./telemetry.db"):
        """Initialize the DatabaseTools with the specified database path.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._initialized = False
        self.mcp_client = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command="uvx",
                args=["mcp-server-sqlite", "--db-path", db_path]
            )
        ))
    
    def _ensure_initialized(self) -> None:
        """Ensure the telemetry table exists, creating it if necessary."""
        if not self._initialized:
            # Execute schema creation
            self.mcp_client.call_tool_sync(
                tool_use_id="init-schema",
                name="write_query",
                arguments={"query": self.TELEMETRY_TABLE_SCHEMA}
            )
            self._initialized = True
    
    def get_tools(self) -> List[Any]:
        """Get the list of database tools for use with an agent.
        
        Returns:
            List of tool functions for database operations
        """
        return [
            self.log_telemetry,
            self.query_telemetry,
            self.query_telemetry_aggregation
        ]
    
    @tool
    def log_telemetry(
        self,
        device_id: str,
        metric_type: str,
        value: float,
        unit: str,
        timestamp: Optional[str] = None
    ) -> str:
        """Log a telemetry record to the database.
        
        Args:
            device_id: The unique identifier of the device
            metric_type: The type of metric (e.g., 'temperature', 'humidity')
            value: The numeric value of the reading
            unit: The unit of measurement (e.g., 'celsius', 'percent')
            timestamp: Optional ISO format timestamp (defaults to current time)
            
        Returns:
            A confirmation message or error description
        """
        try:
            self._ensure_initialized()
            
            if timestamp is None:
                timestamp = datetime.now().isoformat()
            
            query = """
                INSERT INTO device_telemetry (device_id, metric_type, value, unit, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """
            
            result = self.mcp_client.call_tool_sync(
                tool_use_id=f"log-{device_id}-{timestamp}",
                name="write_query",
                arguments={
                    "query": f"""
                        INSERT INTO device_telemetry (device_id, metric_type, value, unit, timestamp)
                        VALUES ('{device_id}', '{metric_type}', {value}, '{unit}', '{timestamp}')
                    """
                }
            )
            
            return (
                f"Telemetry logged successfully:\n"
                f"  Device ID: {device_id}\n"
                f"  Metric: {metric_type}\n"
                f"  Value: {value} {unit}\n"
                f"  Timestamp: {timestamp}"
            )
        except Exception as e:
            return f"Error logging telemetry: {str(e)}"
    
    @tool
    def query_telemetry(
        self,
        device_id: Optional[str] = None,
        metric_type: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100
    ) -> str:
        """Query telemetry records from the database with optional filters.
        
        Args:
            device_id: Optional filter by device ID
            metric_type: Optional filter by metric type
            start_time: Optional start of time range (ISO format)
            end_time: Optional end of time range (ISO format)
            limit: Maximum number of records to return (default 100)
            
        Returns:
            Formatted query results or error description
        """
        try:
            self._ensure_initialized()
            
            # Build query with filters
            conditions = []
            if device_id:
                conditions.append(f"device_id = '{device_id}'")
            if metric_type:
                conditions.append(f"metric_type = '{metric_type}'")
            if start_time:
                conditions.append(f"timestamp >= '{start_time}'")
            if end_time:
                conditions.append(f"timestamp <= '{end_time}'")
            
            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
            
            query = f"""
                SELECT device_id, metric_type, value, unit, timestamp
                FROM device_telemetry
                {where_clause}
                ORDER BY timestamp DESC
                LIMIT {limit}
            """
            
            result = self.mcp_client.call_tool_sync(
                tool_use_id="query-telemetry",
                name="read_query",
                arguments={"query": query}
            )
            
            # Format the results
            content = result.get("content", [])
            if not content:
                return "No telemetry records found matching the criteria."
            
            # Extract text content from MCP response
            text_content = ""
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_content = item.get("text", "")
                    break
            
            if not text_content or text_content.strip() == "[]":
                return "No telemetry records found matching the criteria."
            
            return f"Telemetry Query Results:\n{text_content}"
            
        except Exception as e:
            return f"Error querying telemetry: {str(e)}"
    
    @tool
    def query_telemetry_aggregation(
        self,
        aggregation: str,
        device_id: Optional[str] = None,
        metric_type: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> str:
        """Perform aggregation queries on telemetry data.
        
        Args:
            aggregation: The aggregation function (AVG, MIN, MAX, COUNT, SUM)
            device_id: Optional filter by device ID
            metric_type: Optional filter by metric type
            start_time: Optional start of time range (ISO format)
            end_time: Optional end of time range (ISO format)
            
        Returns:
            Aggregation result or error description
        """
        try:
            self._ensure_initialized()
            
            # Validate aggregation function
            valid_aggregations = ["AVG", "MIN", "MAX", "COUNT", "SUM"]
            aggregation_upper = aggregation.upper()
            if aggregation_upper not in valid_aggregations:
                return f"Error: Invalid aggregation '{aggregation}'. Valid options: {', '.join(valid_aggregations)}"
            
            # Build query with filters
            conditions = []
            if device_id:
                conditions.append(f"device_id = '{device_id}'")
            if metric_type:
                conditions.append(f"metric_type = '{metric_type}'")
            if start_time:
                conditions.append(f"timestamp >= '{start_time}'")
            if end_time:
                conditions.append(f"timestamp <= '{end_time}'")
            
            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
            
            # For COUNT, we count all rows; for others, we aggregate the value column
            if aggregation_upper == "COUNT":
                select_expr = "COUNT(*)"
            else:
                select_expr = f"{aggregation_upper}(value)"
            
            query = f"""
                SELECT {select_expr} as result
                FROM device_telemetry
                {where_clause}
            """
            
            result = self.mcp_client.call_tool_sync(
                tool_use_id="query-aggregation",
                name="read_query",
                arguments={"query": query}
            )
            
            # Extract the result value
            content = result.get("content", [])
            text_content = ""
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_content = item.get("text", "")
                    break
            
            # Build filter description
            filter_desc = []
            if device_id:
                filter_desc.append(f"device_id='{device_id}'")
            if metric_type:
                filter_desc.append(f"metric_type='{metric_type}'")
            if start_time:
                filter_desc.append(f"from {start_time}")
            if end_time:
                filter_desc.append(f"to {end_time}")
            
            filter_str = ", ".join(filter_desc) if filter_desc else "all records"
            
            return (
                f"Aggregation Result:\n"
                f"  Function: {aggregation_upper}\n"
                f"  Filters: {filter_str}\n"
                f"  Result: {text_content}"
            )
            
        except Exception as e:
            return f"Error performing aggregation: {str(e)}"
    
    def __enter__(self):
        """Enter the context manager, starting the MCP client."""
        self.mcp_client.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager, stopping the MCP client."""
        return self.mcp_client.__exit__(exc_type, exc_val, exc_tb)
