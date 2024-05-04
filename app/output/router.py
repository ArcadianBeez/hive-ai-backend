import inject
from loguru import logger
from fastapi import APIRouter, Depends
from app.logic.assigner.assign_free_orders import AssignFreeOrdersUC
from security.key_validator import validate_apikey_request

order_assigner_router = APIRouter()


@order_assigner_router.post("")
async def get_data(query:dict,_=Depends(validate_apikey_request)):
    city_id = query.get("city_id")
    fast_order_radius = query.get("fast_order_radius")
    slow_order_radius = query.get("slow_order_radius")
    log_bind = {"SERVICE_NAME": "order-assigner", "VERSION": "v1", "router": "order-assigner"}
    logger.bind(**log_bind).info("request received")
    uc = inject.instance(AssignFreeOrdersUC)
    response = await uc.execute(city_id, fast_order_radius, slow_order_radius)
    return response
