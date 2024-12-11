from abc import ABC, abstractmethod

from aiogram.enums import ContentType
from aiogram.types import Message


class Exchange(ABC):

    def __init__(self, message: Message, receiver_id: int):
        self.message = message
        self.receiver_id = receiver_id

    @abstractmethod
    async def exchange(self):
        raise NotImplementedError


class TextExchange(Exchange):

    async def exchange(self):
        await self.message.bot.send_message(self.receiver_id, f"🗣️ Аноним: {self.message.text}")


class PhotoExchange(Exchange):
    async def exchange(self):
        await self.message.bot.send_photo(self.receiver_id, photo=self.message.photo[-1].file_id, caption="️🗣️ Аноним")


class VoiceExchange(Exchange):

    async def exchange(self):
        await self.message.bot.send_voice(self.receiver_id, voice=self.message.voice.file_id, caption="🗣️ Аноним")


class VideoNoteExchange(Exchange):
    async def exchange(self):
        await self.message.bot.send_video_note(self.receiver_id, video_note=self.message.video_note.file_id)


class VideoExchange(Exchange):

    async def exchange(self):
        await self.message.bot.send_video(self.receiver_id, video=self.message.video.file_id, caption="🗣️ Аноним")


class FileExchange(Exchange):

    async def exchange(self):
        await self.message.bot.send_document(self.receiver_id, document=self.message.document.file_id)


class StickerExchange(Exchange):

    async def exchange(self):
        await self.message.bot.send_sticker(self.receiver_id, sticker=self.message.sticker.file_id)


class AudioExchange(Exchange):

    async def exchange(self):
        await self.message.bot.send_audio(self.receiver_id, audio=self.message.audio.file_id)


exchanges = {
    ContentType.TEXT: TextExchange,
    ContentType.PHOTO: PhotoExchange,
    ContentType.VOICE: VoiceExchange,
    ContentType.VIDEO_NOTE: VideoNoteExchange,
    ContentType.VIDEO: VideoExchange,
    ContentType.DOCUMENT: FileExchange,
    ContentType.STICKER: StickerExchange,
    ContentType.AUDIO: AudioExchange
}
