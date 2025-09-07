from fastapi import FastAPI 
from app.infra.web_util import WebUtil
 
# API
app = FastAPI( title="Adaptive Question Generation API")

# Configure Cors
WebUtil.configure_cors(app)

# Logging
WebUtil.setup_logging()

# Middlewares
WebUtil.register_middlewares(app)

# Exception handlers
WebUtil.register_exceptionhandlers(app)

# Register routers  
WebUtil.register_routers(app)