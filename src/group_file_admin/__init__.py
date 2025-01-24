from nonebot import (
    on_command,
    require,
    logger
)

plugins = [
    "nonebot_plugin_localstore",
    "nonebot_plugin_waiter"
]

for plugin in plugins:
    require(plugin)

from pathlib import Path
from .config import plugin_config as _config
from .model import DeleteFile
from nonebot.permission import SUPERUSER
from nonebot_plugin_waiter import suggest
from nonebot_plugin_localstore import get_plugin_data_dir
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Bot
)


from nonebot.plugin import PluginMetadata
__plugin_meta__ = PluginMetadata(
    name="群文件管理",
    description="基于Lagrange.OneBot & NoneBot2的群文件管理插件",
    usage="清理群文件：清理群文件\n备份群文件：备份群文件\n恢复群文件：恢复群文件\n文件整理：文件整理",
    type="application",
    homepage="https://github.com/zhongwen-4/nonebot-plugin-group-file-admin",
    supported_adapters={"~onebot.v11"}
)


del_file = on_command(
    "清理群文件",
    permission= SUPERUSER
)

copy_file = on_command(
    "备份群文件",
    permission= SUPERUSER
)

del_local_file = on_command(
    "清理本地文件",
    permission= SUPERUSER
)

recover_flie = on_command(
    "恢复群文件",
    permission= SUPERUSER
)

file_arrange = on_command(
    "文件整理",
    permission= SUPERUSER
)


@del_file.handle()
async def del_flie_handle(bot: Bot, event: GroupMessageEvent):
    option = await suggest(
        message= "注意！！！\n数据无价，请谨慎操作！\n是否确认删除群文件？",
        expect=["y", "n"]
    )
    option = str(option)
    delfile = DeleteFile(event.group_id)

    if option == "n":
        await del_file.finish("已取消")

    if option == "y":
        await del_file.send("开始删除群文件...")
        if _config.fa_del_model == 1:
            datas = await delfile.get_root_data(bot)

            for i in datas.files:
                await delfile.del_file(bot, i.file_id)
            await del_file.finish("删除完成！")
    
        if _config.fa_del_model == 2:
            if not _config.fa_expand_name:
                await del_file.finish("请配置需要删除的文件后缀！")

            datas = await delfile.get_root_data(bot)

            for i in datas.files:
                if i.file_name.endswith(tuple(i for i in _config.fa_expand_name)):
                    await delfile.del_file(bot, i.file_id)
            
            for i in datas.folders:
                datas_ = await delfile.get_folder_data(bot, i.folder_id)

                for file in datas_.files:
                    if file.file_name.endswith(tuple(i for i in _config.fa_expand_name)):
                        await delfile.del_file(bot, file.file_id)
            
            await del_file.finish("删除完成！")

        if _config.fa_del_model == 3:
            confirm = await suggest(
                "再次确认：你正在删除所有群文件，是否继续？",
                expect=["y", "n"]
            )
            confirm = str(confirm)

            if confirm == "n":
                await del_file.finish("已取消")

            if confirm == "y":
                await del_file.send("开始删除群文件...")

                files = await delfile.get_root_data(bot)
                for i in files.files:
                    await delfile.del_file(bot, i.file_id)
                
                for i in files.folders:
                    await delfile.del_folder(bot, i.folder_id)
                
                await del_file.finish("删除完成！")


@copy_file.handle()
async def copy_file_handle(bot: Bot, event: GroupMessageEvent):
    import httpx

    get_file_and_foler = DeleteFile(event.group_id)
    path = get_plugin_data_dir()

    await copy_file.send("开始备份群文件...")
    copys = await get_file_and_foler.get_root_data(bot)
    for i in copys.files:
        logger.info(f"正在备份文件：{i.file_name}")

        async with httpx.AsyncClient() as client:
            file_url = await bot.call_api(
                "get_group_file_url", group_id= event.group_id, file_id= i.file_id
            )
            
            file = await client.get(file_url["url"])
            file_dir = Path(f"{path}/{event.group_id}")
            file_dir.mkdir(parents= True, exist_ok= True)
            file_path = file_dir / i.file_name
            
            with open(file_path, "wb") as f:
                f.write(file.content)
                logger.info(f"备份完成：{i.file_name}")
    
    for i in copys.folders:
        logger.info(f"正在备份文件夹：{i.folder_name}")
        folder_data = await get_file_and_foler.get_folder_data(bot, i.folder_id)
        for files in folder_data.files:
            logger.info(f"正在备份文件：{i.folder_name}/{files.file_name}")

            async with httpx.AsyncClient() as client:
                file_url = await bot.call_api(
                    "get_group_file_url", group_id= event.group_id, file_id= files.file_id
                )

                file = await client.get(file_url["url"])
                file_dir = Path(f"{path}/{event.group_id}/{i.folder_name}")
                file_dir.mkdir(parents= True, exist_ok= True)
                file_path = file_dir / files.file_name

                with open(file_path, "wb") as f:
                    f.write(file.content)
                    logger.info(f"备份完成：{i.folder_name}/{files.file_name}")
    
    await copy_file.finish("备份完成！")


@recover_flie.handle()
async def recover_flie_handle(bot: Bot, event: GroupMessageEvent):
    path = Path(f"{get_plugin_data_dir()}/{event.group_id}")
    files= DeleteFile(event.group_id)
    data= await files.get_root_data(bot)
    folder_names = [i.folder_name for i in data.folders]

    confirm= await suggest(
        "你正在恢复所有群文件，是否继续？",
        expect=["y", "n"]
    )

    if confirm == "n":
        await recover_flie.finish("已取消")

    if confirm == "y":
        await recover_flie.send("开始恢复群文件...")

    if not path.exists():
        await recover_flie.finish("没有备份文件！")

    for item in path.iterdir():
        if item.is_dir():
            if item.name not in folder_names:
                logger.debug(f"文件夹不存在，正在创建文件夹：{item.name}")
                await bot.call_api(
                    "create_group_file_folder", group_id= event.group_id, name= item.name
                )
                logger.debug(f"创建文件夹成功：{item.name}")
            
            data= await files.get_root_data(bot)
            folder_id = [i.folder_id for i in data.folders if i.folder_name == item.name]
            logger.debug(f"获取文件夹ID | {item} : {folder_id}")

            for file in item.glob("*"):
                logger.info(f"正在恢复{file}")
                print(file)
                await bot.call_api(
                    "upload_group_file", group_id= event.group_id, file= str(file), name= file.name, folder= folder_id[0]
                )
                logger.info(f"恢复完成：{file}")
        
        if item.is_file():
            logger.info(f"正在恢复文件：{item}")
            await bot.call_api(
                "upload_group_file", group_id= event.group_id, file= str(item), name= item.name
            )
            logger.info(f"恢复完成：{item}")

    await recover_flie.finish("恢复完成！")


@del_local_file.handle()
async def del_local_file_handle(event: GroupMessageEvent):
    import shutil

    path = Path(f"{get_plugin_data_dir()}/{event.group_id}")
    if not path.exists():
        await del_local_file.finish("没有备份文件！")

    await del_local_file.send("开始删除本地备份文件...")

    for item in path.iterdir():
        if item.is_dir():
            logger.info(f"正在删除文件夹：{item}")
            shutil.rmtree(item)
            logger.info(f"删除完成：{item}")
        
        if item.is_file():
            logger.info(f"正在删除文件：{item}")
            item.unlink()
            logger.info(f"删除完成：{item}")
            
    await del_local_file.finish("删除完成！")


@file_arrange.handle()
async def file_arrange_handle(bot: Bot, event: GroupMessageEvent):
    import re, time
    from collections import OrderedDict
    from nonebot.adapters.onebot.v11.exception import ActionFailed

    await file_arrange.send("开始整理群文件...")

    t = time.time()
    file = DeleteFile(event.group_id)
    data = await file.get_root_data(bot)
    file_expand = [re.findall(r"\.[^\.]+$", i.file_name)[0] for i in data.files]
    file_expand = list(OrderedDict.fromkeys(file_expand))

    for expand in file_expand:
        try:
            logger.info(f"创建文件夹：{expand[1:]}")
            await bot.call_api(
                "create_group_file_folder", group_id= event.group_id, name= expand[1:]
            )
            logger.info(f"文件夹 {expand[1:]} 创建完成")
        except ActionFailed:
            logger.info(f"文件夹 {expand[1:]} 已存在，跳过创建文件夹")
            continue

    for files in data.files:
        file_names = re.findall(r'(\S+)\.(\w+)', files.file_name)
        logger.info(f"获取文件名：{files.file_name}")
        for expand_name in file_names:
            folder = await file.get_root_data(bot)
            for folder_name in folder.folders:
                if folder_name.folder_name == expand_name[1]:
                    logger.info(f"匹配文件夹完成: {files.file_name} -> {folder_name.folder_name}")
                    logger.debug(f"文件夹ID：{folder_name.folder_id} | 文件ID：{files.file_id}")
                    await bot.call_api(
                        "move_group_file", group_id= event.group_id, file_id= files.file_id, target_directory= folder_name.folder_id
                    )
                    logger.info(f"移动文件完成: {files.file_name} -> {folder_name.folder_name}")
    
    logger.info(f"整理完成，耗时：{time.time() - t}s")
    await file_arrange.finish("整理完成！")