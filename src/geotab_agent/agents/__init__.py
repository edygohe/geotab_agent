from .base_agent import BaseAgent
from .orchestrator_agent import OrchestratorAgent
from .analyst_agent import AnalystAgent
from .designer_agent import DesignerAgent
from .coder_agent import CoderAgent

# Esto nos permitirá importar agentes específicos de forma limpia en el futuro, por ejemplo:
# from .orchestrator_agent import OrchestratorAgent
# from .analyst_agent import AnalystAgent