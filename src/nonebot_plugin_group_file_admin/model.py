from .dataclass import data as Data
from nonebot.adapters.onebot.v11 import Bot

class DeleteFile:
    def __init__(self, group_id: int):
        self.group_id = group_id

    async def get_root_data(self, bot: Bot) -> Data:
        data = Data(**await bot.call_api("get_group_root_files", group_id=self.group_id))
        return data
    
    async def get_folder_data(self, bot: Bot, folder_id: str) -> Data:
        data = Data(**await bot.call_api("get_group_files_by_folder", group_id=self.group_id, folder_id=folder_id))
        return data
    
    async def del_file(self, bot: Bot, file_id):
        await bot.call_api(
            "delete_group_file",
            group_id= self.group_id,
            file_id= file_id
        )

    async def del_folder(self, bot: Bot, folder_id: str):
            await bot.call_api(
                "delete_group_file_folder",
                group_id= self.group_id,
                folder_id= folder_id
            )
