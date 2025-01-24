from pydantic import BaseModel
from typing import Optional
from nonebot import get_plugin_config

class Config(BaseModel):
    fa_del_model: int = 1
    fa_expand_name: Optional[list] = None

plugin_config = get_plugin_config(Config)