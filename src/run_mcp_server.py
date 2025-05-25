"""
MCP server for Guitar Pro file manipulation.
"""

import logging
import os
import sys

# Add necessary paths for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)  # Add script directory to path

from mcp.server.fastmcp import FastMCP
from mcp import StdioServerParameters

from controllers import GuitarProController
from mcp_tools import setup_mcp_tools

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    print("Starting MCP server for Guitar Pro...")
    
    try:
        # Create Guitar Pro controller
        print("Initializing GuitarProController...")
        controller = GuitarProController()
        print("GuitarProController initialized successfully.")

        # Create MCP server
        mcp = FastMCP("GuitarPro Control")
  
        # Setup MCP tools
        setup_mcp_tools(mcp, controller)
        
        # Run MCP server
        logger.info("Starting MCP server...")
        mcp.run()
        
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        raise

if __name__ == "__main__":
    main()