from astrbot.api.star import Star, Context
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.event.filter import EventMessageType
from astrbot.api.message_components import Image
import logging


class ImageKill(Star):
    """
    拦截圖檔訊息，阻止其發送給 LLM。
    """

    def __init__(self, context: Context):
        super().__init__(context)
        self.logger = logging.getLogger(__name__)

    @filter.event_message_type(EventMessageType.ALL, priority=1)
    async def handle_image_message(self, event: AstrMessageEvent):
        """
        處理訊息事件，如果包含圖片則攔截。
        """
        if any(isinstance(segment, Image) for segment in event.message_obj.message):
            event.stop_event()
            self.logger.info(
                f"Image message from {event.get_sender_id()} intercepted by ImageKill plugin."
            )

    async def terminate(self):
        """
        插件終止時調用。
        """
        pass
