from logging import raiseExceptions
import chatterbot

from chatterbot.trainers import ChatterBotCorpusTrainer
from utils.decorators import with_executor

class ChatBot:
    def __init__(self, train: bool = True):
        self.chatbot = chatterbot.ChatBot("LunarAPI")
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        if train:
            trainer.train("chatterbot.corpus.english.conversations")
            trainer.train("chatterbot.corpus.english.greetings")
        self.identifiers = "he/him" # :^)

    @with_executor
    def get_response(self, text: str) -> str:
        response = self.chatbot.get_response(text)
        response = response.text
        return response

    

