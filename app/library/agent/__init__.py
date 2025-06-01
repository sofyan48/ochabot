
from pkg.agent import AgentTools
from app.library.agent.tools import (
    search_employee,
    get_assesment
)


agent_lib = AgentTools()
agent_lib.add_tool(search_employee)
agent_lib.add_tool(get_assesment)

