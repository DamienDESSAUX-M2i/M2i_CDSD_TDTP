import uvicorn
from exo1 import users_router
from exo2 import passwords_router
from exo3 import products_router, suppliers_router
from exo4 import orders_router
from exo5 import generic_router
from exo6 import api_config
from exo7 import events_router
from fastapi import FastAPI

app = FastAPI(
    title=api_config.app_name,
    debug=api_config.debug,
)

app.include_router(users_router, prefix=api_config.api_v1_prefix)
app.include_router(passwords_router, prefix=api_config.api_v1_prefix)
app.include_router(suppliers_router, prefix=api_config.api_v1_prefix)
app.include_router(products_router, prefix=api_config.api_v1_prefix)
app.include_router(orders_router, prefix=api_config.api_v1_prefix)
app.include_router(generic_router, prefix=api_config.api_v1_prefix)
app.include_router(events_router, prefix=api_config.api_v1_prefix)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
